import os
import pandas as pd
import joblib
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier

def train_and_save():
    csv_path = 'synthetic_health_data (1).csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
    print("Loading dataset...")
    df = pd.read_csv(csv_path)

    categorical_col = ['diet', 'stress', 'alcohol', 'family_history', 'smoking']
    target_col = 'risk_level'

    print("Encoding categorical features...")
    encoders = {}
    for col in categorical_col:
        le = LabelEncoder()
        df[col] = le.fit_transform(df[col])
        encoders[col] = le

    le_target = LabelEncoder()
    df[target_col] = le_target.fit_transform(df[target_col])
    encoders[target_col] = le_target

    X = df.drop(target_col, axis=1)
    y = df[target_col]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print("Scaling features...")
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    print("Training Random Forest Classifier...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train_scaled, y_train)

    train_acc = model.score(X_train_scaled, y_train)
    test_acc = model.score(X_test_scaled, y_test)
    print(f"Model Training Accuracy: {train_acc:.4f}")
    print(f"Model Testing Accuracy: {test_acc:.4f}")

    print("Saving model and preprocessors to pickle files...")
    joblib.dump(model, 'healthcare_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    joblib.dump(encoders, 'encoder.pkl')

if __name__ == '__main__':
    train_and_save()
