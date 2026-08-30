"""
model_trainer.py - Trains Random Forest and Isolation Forest models
Uses the downloaded CIC-IDS2017 dataset
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier, IsolationForest
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
import joblib
import os
import warnings
warnings.filterwarnings('ignore')

def load_dataset(file_path):
    """
    Load the CIC-IDS2017 CSV dataset
    """
    print(f"📥 Loading dataset from: {file_path}")
    
    # Try different encodings if the first fails
    try:
        df = pd.read_csv(file_path)
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='latin1')
    
    print(f"✅ Loaded {len(df)} rows with {len(df.columns)} columns")
    return df

def preprocess_data(df):
    """
    Clean and prepare the data for ML training
    """
    print("🔄 Preprocessing data...")
    
    # 1. Remove duplicate rows
    df = df.drop_duplicates()
    print(f"   After removing duplicates: {len(df)} rows")
    
    # 2. Remove infinite values (replace with NaN)
    df = df.replace([np.inf, -np.inf], np.nan)
    
    # 3. Drop rows with NaN values (simplest approach for hackathon)
    df = df.dropna()
    print(f"   After dropping NaN: {len(df)} rows")
    
    # 4. Map labels to binary (0 = Benign, 1 = Attack)
    # CIC-IDS labels: 'BENIGN' is normal, everything else is attack
    if 'Label' in df.columns:
        df['label'] = df['Label'].apply(lambda x: 0 if x == 'BENIGN' else 1)
    elif 'label' in df.columns:
        # Already has label column
        pass
    else:
        # Try to find the label column (common names in CIC-IDS)
        label_cols = [col for col in df.columns if 'label' in col.lower() or 'class' in col.lower()]
        if label_cols:
            df['label'] = df[label_cols[0]].apply(lambda x: 0 if str(x).upper() == 'BENIGN' else 1)
        else:
            print("⚠️ No label column found! Using synthetic labels.")
            # If no labels, assume last column is label
            df['label'] = df.iloc[:, -1].apply(lambda x: 0 if str(x).upper() == 'BENIGN' else 1)
    
    # 5. Count attack vs benign
    attack_count = df[df['label'] == 1].shape[0]
    benign_count = df[df['label'] == 0].shape[0]
    print(f"   Benign: {benign_count}, Attack: {attack_count}")
    
    # 6. Drop non-numeric columns (like IP addresses, timestamps)
    # Keep only numeric columns for ML
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    # Remove label from features (we'll keep it separate)
    if 'label' in numeric_cols:
        numeric_cols.remove('label')
    
    # Also remove any other label variants
    for col in numeric_cols[:]:
        if 'label' in col.lower() or 'class' in col.lower():
            numeric_cols.remove(col)
    
    print(f"   Using {len(numeric_cols)} numeric features")
    
    # 7. Separate features and labels
    X = df[numeric_cols].copy()
    y = df['label'].copy()
    
    # 8. Fill any remaining NaN with 0 (just in case)
    X = X.fillna(0)
    
    return X, y

def train_models(X, y):
    """
    Train Random Forest (supervised) and Isolation Forest (unsupervised)
    """
    print("🧠 Training ML models...")
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    
    print(f"   Training set: {len(X_train)} samples")
    print(f"   Test set: {len(X_test)} samples")
    
    # Scale features (important for Isolation Forest)
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    # ---------- Model 1: Random Forest (Supervised) ----------
    print("\n🤖 Training Random Forest...")
    rf_model = RandomForestClassifier(
        n_estimators=100,
        max_depth=15,
        min_samples_split=10,
        min_samples_leaf=4,
        random_state=42,
        n_jobs=-1,
        class_weight='balanced'  # Helps with imbalanced data
    )
    rf_model.fit(X_train_scaled, y_train)
    
    # Evaluate Random Forest
    rf_train_acc = rf_model.score(X_train_scaled, y_train)
    rf_test_acc = rf_model.score(X_test_scaled, y_test)
    print(f"   Random Forest - Train Accuracy: {rf_train_acc:.4f}")
    print(f"   Random Forest - Test Accuracy: {rf_test_acc:.4f}")
    
    # ---------- Model 2: Isolation Forest (Unsupervised) ----------
    print("\n🤖 Training Isolation Forest...")
    iso_model = IsolationForest(
        contamination=0.1,  # Expected proportion of outliers
        random_state=42,
        n_estimators=100
    )
    iso_model.fit(X_train_scaled)
    
    # Evaluate Isolation Forest
    # For Isolation Forest: -1 = anomaly, 1 = normal
    iso_pred_train = iso_model.predict(X_train_scaled)
    iso_pred_test = iso_model.predict(X_test_scaled)
    
    # Convert to binary (0 = normal, 1 = anomaly)
    iso_train_binary = [0 if x == 1 else 1 for x in iso_pred_train]
    iso_test_binary = [0 if x == 1 else 1 for x in iso_pred_test]
    
    # Calculate accuracy against true labels (as a rough measure)
    iso_train_acc = np.mean(iso_train_binary == y_train)
    iso_test_acc = np.mean(iso_test_binary == y_test)
    print(f"   Isolation Forest - Train Accuracy: {iso_train_acc:.4f}")
    print(f"   Isolation Forest - Test Accuracy: {iso_test_acc:.4f}")
    
    # ---------- Save Models ----------
    os.makedirs('models', exist_ok=True)
    joblib.dump(rf_model, 'models/random_forest.pkl')
    joblib.dump(iso_model, 'models/isolation_forest.pkl')
    joblib.dump(scaler, 'models/scaler.pkl')
    
    print("\n✅ Models saved to 'models/' folder!")
    print(f"   - models/random_forest.pkl")
    print(f"   - models/isolation_forest.pkl")
    print(f"   - models/scaler.pkl")
    
    return rf_model, iso_model, scaler

def main():
    """Main execution function"""

    # Ensure the data directory exists
    os.makedirs('data/raw', exist_ok=True)
    
    # Find the dataset file
    data_dir = 'data/raw/'
    csv_files = [f for f in os.listdir(data_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print("❌ No CSV files found in data/raw/")
        print("Please download a dataset first!")
        return
    
    # Use the first CSV found
    file_path = os.path.join(data_dir, csv_files[0])
    
    print("=" * 60)
    print("🛡️ TEAM VORTEX - AI Threat Detection Model Trainer")
    print("=" * 60)
    
    # Load and preprocess
    df = load_dataset(file_path)
    X, y = preprocess_data(df)
    
    # Train models
    rf_model, iso_model, scaler = train_models(X, y)
    
    print("\n" + "=" * 60)
    print("🎉 TRAINING COMPLETE!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run the inference pipeline: python backend/model_inference.py")
    print("2. Or start the dashboard: streamlit run frontend/dashboard.py")

if __name__ == "__main__":
    main()