import os
import pandas as pd

def train_and_save():
    csv_path = 'synthetic_health_data (1).csv'
    if not os.path.exists(csv_path):
        print(f"Error: {csv_path} not found.")
        return
    print("Loading dataset...")
    df = pd.read_csv(csv_path)
    print(f"Loaded dataset with shape {df.shape}")

if __name__ == '__main__':
    train_and_save()
