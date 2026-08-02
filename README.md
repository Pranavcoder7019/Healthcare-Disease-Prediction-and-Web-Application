# Healthcare Disease Prediction & Analytics Web Application

An AI-powered, modern, responsive clinical decision support system built with a Python Flask backend and a premium HTML/CSS/JavaScript frontend utilizing glassmorphic aesthetics. 

The application utilizes a machine learning model trained on patient vitals and health indicators to evaluate potential chronic disease risk levels. It includes a health statistics dashboard, patient vitals tracking form, customized clinical recommendations, and printable diagnostic PDF reports.

## Project Structure

```text
Healthcare-Prediction/
│
├── app.py                  # Core Flask backend with prediction routes
├── train_model.py          # Model training and serialization script
├── healthcare_model.pkl    # Trained RandomForestClassifier model
├── scaler.pkl              # Pre-fitted StandardScaler object
├── encoder.pkl             # Pre-fitted LabelEncoder dictionary
├── requirements.txt        # Python package dependencies
├── Procfile                # WSGI execution process descriptor
├── runtime.txt             # Deployment Python runtime specification
│
├── static/
│   ├── style.css           # Premium glassmorphic styling system
│   └── script.js           # Client-side logics, calculators, and Chart.js
│
├── templates/
│   ├── index.html          # Main landing, dashboard, and diagnostic form
│   ├── result.html         # Diagnostic report with customized recommendations
│   ├── about.html          # Model metrics, details, and health glossary
│   ├── 404.html            # Custom page-not-found error page
│   └── 500.html            # Custom internal server error page
│
└── README.md               # Project documentation (this file)
```

## Features

1. **AI-Powered Diagnostics**: Runs a pre-trained RandomForest Classifier model (Accuracy: **96.50%**) to predict High, Medium, or Low chronic risk categories.
2. **Interactive Clinical Dashboard**: Features three interactive charts using Chart.js plotting prediction histories, risk distributions, and concern categories.
3. **Smart Clinical Recommendation Engine**: Evaluates patient physiological vitals (BMI, Blood Pressure, Sugar, Cholesterol) to output detailed dietary, activity, and medical suggestions.
4. **Fluid Glassmorphism UI**: Beautiful healthcare theme with responsive grids, micro-animations, and full dark-mode toggle support.
5. **Printable Medical Reports**: Specifically styled printing layouts allowing patients to download clean clinical reports as PDF via browser print hooks.
6. **Robust Input Validation**: Strict checks for numeric ranges and complete client/server-side error handling (with custom 404/500 pages).

## Getting Started (Local Setup)

### Prerequisites
- Python 3.10, 3.11, or 3.12+
- `pip` package installer

### Installation
1. Clone or extract the project files into your workspace directory.
2. Open a terminal in the project folder.
3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Training the Model (Optional)
If you need to re-train the machine learning model and regenerate the pickle files (`healthcare_model.pkl`, `scaler.pkl`, `encoder.pkl`):
```bash
python train_model.py
```

### Running the Application
To run the local Flask development web server:
```bash
python app.py
```
After the server initializes, navigate to `http://127.0.0.1:5000` in your web browser.

## Deployment Ready
The application is pre-configured with the files needed for direct deployment on various cloud services:
- **Heroku / Render / Railway**: Configured via the `Procfile` utilizing Gunicorn and `runtime.txt` configuring Python version compatibility.
- **Render Setup**:
  1. Link your GitHub repository.
  2. Select **Web Service**.
  3. Environment: `Python`.
  4. Build Command: `pip install -r requirements.txt`.
  5. Start Command: `gunicorn app:app`.

---
*Disclaimer: This system is designed as an educational clinical decision support demonstration. All outcomes must be evaluated by a certified medical practitioner.*
