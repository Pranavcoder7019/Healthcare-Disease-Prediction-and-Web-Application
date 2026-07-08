import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler

def train_and_save():
    csv_path = 'synthetic_health_data (1).csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
    print("Loading dataset...")
    df = pd.read_csv(csv_path)

    # Categorical columns
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
    print("Data preprocessed and split.")

if __name__ == '__main__':
    train_and_save()
