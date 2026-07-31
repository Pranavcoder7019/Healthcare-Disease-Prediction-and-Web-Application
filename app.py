import os
import datetime
import pandas as pd
import numpy as np
import joblib
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = 'healthcare_prediction_secret_key'  # Used for session storage

# Global variables for model and preprocessors
model = None
scaler = None
encoders = None

def load_ml_artifacts():
    global model, scaler, encoders
    try:
        model = joblib.load('healthcare_model.pkl')
        scaler = joblib.load('scaler.pkl')
        encoders = joblib.load('encoder.pkl')
        print("ML artifacts loaded successfully.")
    except Exception as e:
        print(f"Error loading ML artifacts: {e}")

# Load ML artifacts at startup
load_ml_artifacts()

def get_session_history():
    """Get history from session, or initialize with mock data if empty."""
    if 'history' not in session:
        # Seed with realistic mock history data to populate charts on first load
        session['history'] = [
            {'id': 1, 'date': '2026-07-01', 'age': 45, 'gender': 'Male', 'bmi': 28.4, 'risk': 'Medium', 'confidence': 82.5, 'symptoms': 'Fatigue, Headaches'},
            {'id': 2, 'date': '2026-07-02', 'age': 62, 'gender': 'Female', 'bmi': 31.2, 'risk': 'High', 'confidence': 96.0, 'symptoms': 'Chest Tightness, Shortness of breath'},
            {'id': 3, 'date': '2026-07-02', 'age': 28, 'gender': 'Male', 'bmi': 21.5, 'risk': 'Low', 'confidence': 94.3, 'symptoms': 'None'},
            {'id': 4, 'date': '2026-07-03', 'age': 54, 'gender': 'Female', 'bmi': 24.8, 'risk': 'Medium', 'confidence': 78.1, 'symptoms': 'Joint Pain'},
            {'id': 5, 'date': '2026-07-03', 'age': 35, 'gender': 'Male', 'bmi': 19.1, 'risk': 'Low', 'confidence': 91.5, 'symptoms': 'Mild Cough'}
        ]
    return session['history']

def add_to_session_history(record):
    history = get_session_history()
    record['id'] = len(history) + 1
    record['date'] = datetime.date.today().strftime('%Y-%m-%d')
    history.append(record)
    # Keep the last 15 entries to prevent cookie overflow (4KB limit)
    if len(history) > 15:
        history = history[-15:]
    session['history'] = history
    session.modified = True

def generate_recommendations(data, risk_level):
    """
    Generate personalized clinical recommendations based on risk level and clinical parameters.
    """
    lifestyle = []
    diet = []
    medical = []

    # 1. Base on Risk Level
    if risk_level == 'High':
        medical.append("Immediate clinical evaluation is recommended. Please schedule an appointment with a primary care physician or specialist as soon as possible.")
        lifestyle.append("Minimize physical exertion and high-stress activities until you receive a physician's clearance.")
    elif risk_level == 'Medium':
        medical.append("Schedule a routine physical check-up to review your vital trends with a doctor.")
        lifestyle.append("Incorporate stress-reduction techniques such as mindfulness, meditation, or light yoga into your routine.")
    else:
        medical.append("Continue with your periodic annual health screenings to maintain active monitoring.")
        lifestyle.append("Maintain your current active lifestyle. Aim for consistency in your routine.")

    # 2. Base on BMI
    bmi = data.get('bmi', 22.0)
    if bmi >= 30.0:
        lifestyle.append(f"Your BMI is {bmi:.1f} (Obese). Engage in at least 150 minutes of moderate-intensity exercise per week, as tolerated.")
        diet.append("Adopt a calorie-restricted diet focusing on high-fiber vegetables, lean proteins, and complex carbohydrates while minimizing simple sugars.")
    elif bmi >= 25.0:
        lifestyle.append(f"Your BMI is {bmi:.1f} (Overweight). Consider integrating daily 30-minute walks and strength training to manage weight.")
        diet.append("Limit portion sizes, reduce intake of refined fats, and increase consumption of fresh greens and whole grains.")
    elif bmi < 18.5:
        lifestyle.append(f"Your BMI is {bmi:.1f} (Underweight). Consult a clinical nutritionist about healthy weight gain strategies.")
        diet.append("Focus on nutrient-dense foods: nuts, avocados, dairy, eggs, lean meats, and frequent balanced small meals.")

    # 3. Base on Blood Pressure
    systolic = data.get('bp_systolic')
    diastolic = data.get('bp_diastolic')
    if systolic and diastolic:
        if systolic >= 140 or diastolic >= 90:
            medical.append(f"Your BP ({systolic}/{diastolic} mmHg) indicates Stage 2 Hypertension. Consult a physician for blood pressure management.")
            diet.append("Restrict daily sodium intake to under 1,500 mg. Follow the DASH (Dietary Approaches to Stop Hypertension) diet plan.")
            lifestyle.append("Avoid stimulants, manage emotional stress, and check your blood pressure twice daily.")
        elif systolic >= 120 or diastolic >= 80:
            medical.append(f"Your BP ({systolic}/{diastolic} mmHg) is elevated/pre-hypertensive. Monitor it weekly.")
            diet.append("Limit sodium intake, avoid processed foods, and increase intake of potassium-rich foods (bananas, spinach).")

    # 4. Base on Blood Sugar
    sugar = data.get('blood_sugar')
    if sugar:
        if sugar >= 140:
            medical.append(f"Elevated blood sugar ({sugar} mg/dL) detected. Discuss this with an endocrinologist and check HbA1c levels.")
            diet.append("Strictly limit processed sugars, white flour, sweetened beverages, and high-glycemic carbohydrates.")
        elif sugar < 70:
            medical.append(f"Low blood sugar ({sugar} mg/dL) detected. Ensure you are consuming regular meals.")
            diet.append("Carry a fast-acting source of carbohydrates (e.g., fruit juice) in case of sudden symptoms of hypoglycemia.")

    # 5. Base on Cholesterol
    cholesterol = data.get('cholesterol')
    if cholesterol and cholesterol >= 200:
        diet.append(f"Your cholesterol ({cholesterol} mg/dL) is elevated. Limit saturated fats, trans-fats, and cholesterol-dense foods like red meat.")
        diet.append("Incorporate foods high in soluble fiber (oats, legumes, fruits) and healthy fats containing Omega-3.")
        lifestyle.append("Regular aerobic exercises (brisk walking, swimming) can help improve your lipid profile.")

    # 6. Smoking & Alcohol
    if data.get('smoking') == 'Yes':
        lifestyle.append("Smoking significantly increases risk of cardiovascular disease. Consider speaking with a professional about smoking cessation resources.")
    if data.get('alcohol') == 'High':
        lifestyle.append("High alcohol intake affects liver and heart health. Limit consumption to standard medical guidelines (1 drink/day for women, 2/day for men).")

    # Fill defaults if lists are empty
    if not lifestyle:
        lifestyle.append("Maintain 7-8 hours of quality sleep daily and engage in regular physical activity.")
    if not diet:
        diet.append("Consume a balanced diet rich in whole foods, vegetables, lean protein, and drink plenty of water.")
    if not medical:
        medical.append("Discuss these results at your next regular medical check-up.")

    return {
        'lifestyle': lifestyle,
        'diet': diet,
        'medical': medical,
        'disclaimer': "Disclaimer: This prediction is generated by an artificial intelligence model and is intended for informational and educational purposes only. It does NOT constitute professional clinical advice, diagnosis, or treatment. Always consult a qualified physician or healthcare provider regarding any medical concern. Never disregard professional medical advice or delay seeking it because of information read here."
    }

@app.route('/')
def index():
    # Make sure history is seeded
    get_session_history()
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/api/history')
def api_history():
    history = get_session_history()
    return jsonify(history)

@app.route('/api/reset-history', methods=['POST'])
def api_reset_history():
    session.pop('history', None)
    get_session_history()  # Re-initialize empty
    return jsonify({'status': 'success', 'message': 'History reset to default mock data.'})

@app.route('/predict', methods=['POST'])
def predict():
    if model is None or scaler is None or encoders is None:
        return render_template('500.html', error="Machine learning model assets are not loaded on server. Please try again later."), 500

    try:
        # Collect and validate form inputs
        name = request.form.get('name', 'Patient').strip()
        gender = request.form.get('gender', 'Male')
        
        # Numeric inputs with fallbacks and validations
        try:
            age = int(request.form.get('age', 0))
            if age <= 0 or age > 120:
                raise ValueError("Age must be between 1 and 120.")
            
            height = float(request.form.get('height', 0))
            if height <= 0 or height > 250:
                raise ValueError("Height must be positive and realistic (up to 250 cm).")
            
            weight = float(request.form.get('weight', 0))
            if weight <= 0 or weight > 500:
                raise ValueError("Weight must be positive and realistic (up to 500 kg).")
            
            sleep_hours = int(request.form.get('sleep_hours', 7))
            if sleep_hours < 0 or sleep_hours > 24:
                raise ValueError("Sleep hours must be between 0 and 24.")
        except ValueError as ve:
            return render_template('index.html', error=f"Invalid Input: {str(ve)}"), 400

        # Optional medical inputs
        def get_optional_float(field):
            val = request.form.get(field)
            return float(val) if val and val.strip() else None

        bp_systolic = get_optional_float('bp_systolic')
        bp_diastolic = get_optional_float('bp_diastolic')
        heart_rate = get_optional_float('heart_rate')
        temperature = get_optional_float('temperature')
        blood_sugar = get_optional_float('blood_sugar')
        cholesterol = get_optional_float('cholesterol')
        
        # Categorical form inputs
        diet_quality = request.form.get('diet', 'Average')
        stress_level = request.form.get('stress', 'Medium')
        smoking = request.form.get('smoking', 'No')
        alcohol = request.form.get('alcohol', 'Low')
        family_history = request.form.get('family_history', 'No')
        
        exercise_level = request.form.get('exercise_level', 'Medium')
        # Map exercise level to exercise_days (0 to 7)
        exercise_mapping = {'None': 0, 'Low': 2, 'Medium': 4, 'High': 6}
        exercise_days = exercise_mapping.get(exercise_level, 3)

        existing_diseases = request.form.get('existing_diseases', '').strip()
        symptoms = request.form.get('symptoms', '').strip()

        # Compute BMI: Weight (kg) / Height (m)^2
        bmi = weight / ((height / 100.0) ** 2)
        bmi = round(bmi, 2)

        # Assemble DataFrame for model
        input_data = {
            'age': age,
            'diet': diet_quality,
            'exercise_days': exercise_days,
            'sleep_hours': sleep_hours,
            'stress': stress_level,
            'bmi': bmi,
            'smoking': smoking,
            'alcohol': alcohol,
            'family_history': family_history
        }

        input_df = pd.DataFrame([input_data])

        # Preprocess features using LabelEncoder
        for col in ['diet', 'stress', 'alcohol', 'family_history', 'smoking']:
            le = encoders[col]
            # Handle unseen labels by mapping to default if needed, though they match training
            try:
                input_df[col] = le.transform(input_df[col])
            except Exception:
                # Fallback to closest class
                input_df[col] = le.transform([le.classes_[0]])[0]

        # Scale features
        input_scaled = scaler.transform(input_df)
        input_scaled_df = pd.DataFrame(input_scaled, columns=input_df.columns)

        # Predict disease risk
        pred_class_encoded = model.predict(input_scaled_df)[0]
        pred_proba = model.predict_proba(input_scaled_df)[0]

        # Decode risk level
        target_le = encoders['risk_level']
        risk_level = target_le.inverse_transform([pred_class_encoded])[0] # High, Low, Medium
        
        # Get index of risk level in classes
        class_idx = list(target_le.classes_).index(risk_level)
        confidence = float(pred_proba[class_idx]) * 100
        confidence = round(confidence, 2)

        # Gather patient info for report
        patient_info = {
            'name': name,
            'age': age,
            'gender': gender,
            'height': height,
            'weight': weight,
            'bmi': bmi,
            'bp_systolic': int(bp_systolic) if bp_systolic else 'Not provided',
            'bp_diastolic': int(bp_diastolic) if bp_diastolic else 'Not provided',
            'heart_rate': int(heart_rate) if heart_rate else 'Not provided',
            'temperature': temperature if temperature else 'Not provided',
            'blood_sugar': blood_sugar if blood_sugar else 'Not provided',
            'cholesterol': cholesterol if cholesterol else 'Not provided',
            'smoking': smoking,
            'alcohol': alcohol,
            'exercise_level': exercise_level,
            'family_history': family_history,
            'existing_diseases': existing_diseases if existing_diseases else 'None',
            'symptoms': symptoms if symptoms else 'None'
        }

        # Generate intelligent recommendations
        recs = generate_recommendations(patient_info, risk_level)

        # Record prediction to session history
        history_record = {
            'age': age,
            'gender': gender,
            'bmi': bmi,
            'risk': risk_level,
            'confidence': confidence,
            'symptoms': symptoms if symptoms else 'None'
        }
        add_to_session_history(history_record)

        # Render result template
        return render_template(
            'result.html',
            patient=patient_info,
            risk_level=risk_level,
            confidence=confidence,
            recs=recs
        )

    except Exception as e:
        import traceback
        traceback.print_exc()
        return render_template('500.html', error=f"Internal prediction server error: {str(e)}"), 500

# Error Handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html', error="An unexpected internal server error occurred."), 500

if __name__ == '__main__':
    # Start the Flask app in a stable single-process mode
    app.run(debug=False, host='0.0.0.0', port=5000, use_reloader=False)
