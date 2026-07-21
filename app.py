import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request

app = Flask(__name__)

model = joblib.load('healthcare_model.pkl')
scaler = joblib.load('scaler.pkl')
encoders = joblib.load('encoder.pkl')

def get_recommendations(data):
    recs = []
    if data['bmi'] >= 25.0:
        recs.append("Dietary guidance for calorie deficit; exercise 150 mins weekly.")
    if data['systolic_bp'] >= 130 or data['diastolic_bp'] >= 80:
        recs.append("Reduce sodium intake; monitor blood pressure daily.")
    if not recs:
        recs.append("Vitals look great. Keep up a balanced diet and regular exercise.")
    return recs

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = {
            'age': float(request.form.get('age')),
            'bmi': float(request.form.get('bmi')),
            'cholesterol': float(request.form.get('cholesterol', 180)),
            'glucose': float(request.form.get('glucose', 90)),
            'hdl': float(request.form.get('hdl', 50)),
            'ldl': float(request.form.get('ldl', 100)),
            'systolic_bp': float(request.form.get('systolic_bp', 120)),
            'diastolic_bp': float(request.form.get('diastolic_bp', 80)),
            'heart_rate': float(request.form.get('heart_rate', 72)),
            'diet': request.form.get('diet'),
            'stress': request.form.get('stress'),
            'alcohol': request.form.get('alcohol'),
            'family_history': request.form.get('family_history'),
            'smoking': request.form.get('smoking')
        }
        df_input = pd.DataFrame([data])
        for col, encoder in encoders.items():
            if col != 'risk_level' and col in df_input.columns:
                df_input[col] = encoder.transform(df_input[col])
        scaled_features = scaler.transform(df_input)
        prediction = model.predict(scaled_features)[0]
        predicted_risk = encoders['risk_level'].classes_[prediction]
        recs = get_recommendations(data)
        return render_template('result.html', prediction=predicted_risk, input_data=data, recommendations=recs)
    except Exception as e:
        return render_template('500.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
