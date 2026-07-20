import os
import joblib
import pandas as pd
import numpy as np
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

model = joblib.load('healthcare_model.pkl')
scaler = joblib.load('scaler.pkl')
encoders = joblib.load('encoder.pkl')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Collect raw values
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
        
        # Categorical Encoders
        for col, encoder in encoders.items():
            if col != 'risk_level' and col in df_input.columns:
                df_input[col] = encoder.transform(df_input[col])
                
        # Scale & predict (Buggy column order check here - fixed on Day 27!)
        scaled_features = scaler.transform(df_input)
        prediction = model.predict(scaled_features)[0]
        
        risk_labels = encoders['risk_level'].classes_
        predicted_risk = risk_labels[prediction]
        
        return render_template('result.html', prediction=predicted_risk, input_data=data)
    except Exception as e:
        return render_template('500.html', error=str(e)), 500

if __name__ == '__main__':
    app.run(debug=True)
