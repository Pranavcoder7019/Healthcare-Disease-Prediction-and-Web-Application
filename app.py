import os
import joblib
from flask import Flask

app = Flask(__name__)

# Load models
model = joblib.load('healthcare_model.pkl')
scaler = joblib.load('scaler.pkl')
encoders = joblib.load('encoder.pkl')

@app.route('/')
def index():
    return "Models loaded. Server ready."

@app.route('/predict', methods=['POST'])
def predict():
    return "Predict placeholder"

if __name__ == '__main__':
    app.run(debug=True)
