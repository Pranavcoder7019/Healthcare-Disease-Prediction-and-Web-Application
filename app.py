import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

# Load clinical model serialized artifacts
model = joblib.load('healthcare_model.pkl')
scaler = joblib.load('scaler.pkl')
encoders = joblib.load('encoder.pkl')

def evaluate_vitals_recommendations(data: dict) -> list:
    """
    Evaluates patient vitals and yields clinical suggestions.
    """
    recommendations = []
    if data.get('bmi', 0) >= 25.0:
        recommendations.append("Dietary guidance for calorie deficit; exercise 150 mins weekly.")
    if data.get('systolic_bp', 0) >= 130 or data.get('diastolic_bp', 0) >= 80:
        recommendations.append("Reduce sodium intake; monitor blood pressure daily.")
    if not recommendations:
        recommendations.append("Vitals look great. Keep up a balanced diet and regular exercise.")
    return recommendations

@app.route('/')
def index():
    """Renders landing interface and statistics dashboard."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Executes ML predictions and outputs recommendations."""
    try:
        data = {
            'age': float(request.form.get('age', 0)),
            'bmi': float(request.form.get('bmi', 0)),
            'cholesterol': float(request.form.get('cholesterol', 180)),
            'glucose': float(request.form.get('glucose', 90)),
            'hdl': float(request.form.get('hdl', 50)),
            'ldl': float(request.form.get('ldl', 100)),
            'systolic_bp': float(request.form.get('systolic_bp', 120)),
            'diastolic_bp': float(request.form.get('diastolic_bp', 80)),
            'heart_rate': float(request.form.get('heart_rate', 72)),
            'diet': request.form.get('diet', 'Average'),
            'stress': request.form.get('stress', 'Medium'),
            'alcohol': request.form.get('alcohol', 'None'),
            'family_history': request.form.get('family_history', 'No'),
            'smoking': request.form.get('smoking', 'No')
        }
        df_input = pd.DataFrame([data])
        for col, encoder in encoders.items():
            if col != 'risk_level' and col in df_input.columns:
                df_input[col] = encoder.transform(df_input[col])
                
        # Scaled parameters (column matching bug here - fixed on Day 27!)
        scaled_features = scaler.transform(df_input)
        prediction = model.predict(scaled_features)[0]
        
        predicted_risk = encoders['risk_level'].classes_[prediction]
        recs = evaluate_vitals_recommendations(data)
        
        return render_template('result.html', prediction=predicted_risk, input_data=data, recommendations=recs)
    except Exception as e:
        return render_template('500.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
