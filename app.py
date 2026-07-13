import os
import joblib
from flask import Flask, request, jsonify

app = Flask(__name__)

model = joblib.load('healthcare_model.pkl')
scaler = joblib.load('scaler.pkl')
encoders = joblib.load('encoder.pkl')

@app.route('/')
def index():
    return "Clinical decision system is ready."

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Extract and validate inputs
        age = float(request.form.get('age', 0))
        bmi = float(request.form.get('bmi', 0))
        # Basic boundary checks
        if age <= 0 or bmi <= 0:
            return jsonify({"error": "Invalid age or BMI"}), 400
        return jsonify({"status": "Inputs validated"})
    except ValueError:
        return jsonify({"error": "Invalid numeric format"}), 400

if __name__ == '__main__':
    app.run(debug=True)
