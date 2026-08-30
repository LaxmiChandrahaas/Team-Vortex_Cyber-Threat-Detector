"""
model_inference.py - Real-time threat detection using trained models
"""

import joblib
import numpy as np
import pandas as pd
import warnings
warnings.filterwarnings('ignore')

class ThreatDetector:
    def __init__(self):
        """Load trained models"""
        print("🔧 Loading trained models...")
        try:
            self.rf_model = joblib.load('models/random_forest.pkl')
            self.iso_model = joblib.load('models/isolation_forest.pkl')
            self.scaler = joblib.load('models/scaler.pkl')
            # Get the expected feature names from the scaler
            self.feature_names = self.scaler.feature_names_in_
            print(f"✅ Models loaded successfully!")
            print(f"   Expected features: {len(self.feature_names)} columns")
        except FileNotFoundError as e:
            print(f"❌ Model file not found: {e}")
            print("   Please run model_trainer.py first!")
            raise
    
    def predict(self, features_df):
        """
        Predict threat for each flow
        
        Args:
            features_df: DataFrame with numeric features
        
        Returns:
            DataFrame with predictions and confidence scores
        """
        # Ensure all required features are present
        missing_cols = set(self.feature_names) - set(features_df.columns)
        if missing_cols:
            print(f"⚠️ Missing columns: {missing_cols}")
            print(f"   Adding them with default values (0)")
            for col in missing_cols:
                features_df[col] = 0
        
        # Reorder columns to match training data
        X = features_df[self.feature_names].fillna(0)
        
        # Scale features
        X_scaled = self.scaler.transform(X)
        
        # Get Random Forest predictions
        rf_pred = self.rf_model.predict(X_scaled)
        rf_probs = self.rf_model.predict_proba(X_scaled)
        
        # Get Isolation Forest predictions
        iso_pred = self.iso_model.predict(X_scaled)
        iso_scores = self.iso_model.decision_function(X_scaled)
        
        # Combine predictions
        results = []
        for i in range(len(features_df)):
            # If either model flags it, mark as malicious
            is_malicious = (rf_pred[i] == 1) or (iso_pred[i] == -1)
            
            # Calculate combined confidence
            if is_malicious:
                rf_confidence = rf_probs[i][1] if len(rf_probs[i]) > 1 else 0.5
                iso_confidence = abs(iso_scores[i]) / 2
                confidence = (rf_confidence + iso_confidence) / 2
                threat_class = 'MALICIOUS'
            else:
                confidence = rf_probs[i][0] if len(rf_probs[i]) > 1 else 0.9
                threat_class = 'BENIGN'
            
            results.append({
                'threat_class': threat_class,
                'confidence_score': min(confidence * 100, 99.9)
            })
        
        return pd.DataFrame(results)

# Quick test
if __name__ == "__main__":
    print("🧪 Testing inference pipeline...")
    detector = ThreatDetector()
    
    # Get the actual feature names from the model
    feature_names = detector.feature_names
    print(f"📋 Model expects these features: {feature_names[:5]}... (and {len(feature_names)-5} more)")
    
    # Create test data with ALL expected features
    test_data_dict = {}
    
    # First, try to load synthetic data if it exists
    try:
        synth_data = pd.read_csv('data/raw/synthetic_traffic.csv')
        # Select only the features the model expects
        available_cols = [col for col in feature_names if col in synth_data.columns]
        if available_cols:
            test_data = synth_data[available_cols].head(5)
            print(f"📊 Using synthetic data with {len(available_cols)} matching features")
        else:
            raise ValueError("No matching columns found")
    except (FileNotFoundError, ValueError):
        print("🔄 No synthetic data found. Creating sample data with all features...")
        # Create sample data with ALL expected features (use 0 as default)
        test_data_dict = {col: [0] * 5 for col in feature_names}
        
        # Override with some meaningful values for known features
        meaningful_features = {
            'packet_count': [10, 5000, 5, 100, 2000],
            'byte_count': [1000, 500000, 200, 8000, 300000],
            'unique_src_ports': [2, 1, 15, 3, 1],
            'avg_packet_size': [100, 100, 40, 80, 150],
            'flow_duration': [60, 5, 120, 30, 10]
        }
        
        # Only override if the feature exists in the model's expected features
        for col, values in meaningful_features.items():
            if col in feature_names:
                test_data_dict[col] = values
        
        test_data = pd.DataFrame(test_data_dict)
    
    # Ensure all columns are in the right order
    test_data = test_data[feature_names]
    
    # Make predictions
    predictions = detector.predict(test_data)
    
    print("\n📊 Prediction Results:")
    result_df = pd.DataFrame({
        'Features': ['Sample 1', 'Sample 2', 'Sample 3', 'Sample 4', 'Sample 5'],
        'Threat Class': predictions['threat_class'],
        'Confidence %': predictions['confidence_score'].round(1)
    })
    print(result_df.to_string(index=False))