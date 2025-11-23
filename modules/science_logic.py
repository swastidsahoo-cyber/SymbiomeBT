import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
import os

# ==========================================
# SYMBIOME SCIENCE LOGIC & AI ENGINE
# ==========================================
# This module handles:
# 1. Feature Engineering: Calculating RMSSD, SCL, SCR.
# 2. AI Modeling: Training and predicting Recovery Time.
# 3. Digital Twin Logic: Simple adaptive prediction.
# ==========================================

# --- 1. Feature Engineering Formulas ---

def calculate_rmssd(rr_intervals):
    """
    Calculates the Root Mean Square of Successive Differences (RMSSD).
    This is the gold-standard time-domain measure for HRV.
    
    Formula: sqrt(mean(diff(RR)^2))
    """
    diffs = np.diff(rr_intervals)
    squared_diffs = diffs ** 2
    mean_squared_diff = np.mean(squared_diffs)
    rmssd = np.sqrt(mean_squared_diff)
    return rmssd

def calculate_sri(hrv, gsr, facial):
    """
    Calculates the Symbiome Resilience Index (SRI).
    Weighted average of the three biosignals.
    
    Weights:
    - HRV: 50% (Most reliable indicator of vagal tone)
    - GSR: 30% (Acute stress response)
    - Facial: 20% (Behavioral/Emotional proxy)
    """
    sri = (hrv * 0.5) + (gsr * 0.3) + (facial * 0.2)
    return sri

# --- 2. AI Model Engine ---

MODEL_PATH = "symbiome/data/recovery_model.pkl"

def train_recovery_model():
    """
    Trains a Random Forest model to predict 'Recovery Time' (minutes).
    
    Features:
    - Baseline HRV
    - Stress Peak Magnitude (GSR)
    - Sleep Hours (Context)
    
    Target:
    - Recovery Time (Time to return to baseline)
    """
    # Generate Synthetic Training Data for the Model
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'Baseline_HRV': np.random.uniform(30, 90, n_samples),
        'Stress_Peak_GSR': np.random.uniform(5, 20, n_samples), # uS increase
        'Sleep_Hours': np.random.uniform(4, 10, n_samples),
        'Caffeine_Intake': np.random.randint(0, 5, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    # The "Ground Truth" Formula (Simulation of Physiology)
    # More Sleep = Faster Recovery
    # Higher HRV = Faster Recovery
    # Higher Stress Peak = Slower Recovery
    # Caffeine = Slower Recovery
    df['Recovery_Time_Min'] = (
        10 
        - (df['Baseline_HRV'] * 0.05) 
        + (df['Stress_Peak_GSR'] * 0.5) 
        - (df['Sleep_Hours'] * 0.8) 
        + (df['Caffeine_Intake'] * 1.2)
    )
    # Add some noise
    df['Recovery_Time_Min'] += np.random.normal(0, 1, n_samples)
    df['Recovery_Time_Min'] = df['Recovery_Time_Min'].clip(1, 30)
    
    # Train Model
    X = df[['Baseline_HRV', 'Stress_Peak_GSR', 'Sleep_Hours', 'Caffeine_Intake']]
    y = df['Recovery_Time_Min']
    
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save Model
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)
        
    print(f"AI Model trained and saved to {MODEL_PATH}")
    return model

def load_model():
    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, 'rb') as f:
            return pickle.load(f)
    else:
        return train_recovery_model()

def predict_recovery(hrv, gsr_peak, sleep, caffeine):
    model = load_model()
    input_data = pd.DataFrame([[hrv, gsr_peak, sleep, caffeine]], 
                              columns=['Baseline_HRV', 'Stress_Peak_GSR', 'Sleep_Hours', 'Caffeine_Intake'])
    prediction = model.predict(input_data)[0]
    return round(prediction, 1)

# --- 3. Digital Twin Logic ---

def get_digital_twin_insight(history_df):
    """
    Analyzes user history to generate a 'Digital Twin' prediction.
    """
    if history_df.empty:
        return "Not enough data to generate Digital Twin insights."
        
    avg_resilience = history_df['Symbiome_Resilience_Score'].mean()
    trend = history_df['Symbiome_Resilience_Score'].iloc[-1] - history_df['Symbiome_Resilience_Score'].iloc[0]
    
    if trend > 5:
        return f"Your Digital Twin is evolving. Resilience is up {trend:.1f}% this month. Keep optimizing sleep."
    elif trend < -5:
        return f"Warning: Your Digital Twin detects a downward trend. Recommended: 5 min breathing session."
    else:
        return f"Your system is stable. Average Resilience: {avg_resilience:.1f}. Maintain current routine."

if __name__ == "__main__":
    # Test the logic
    train_recovery_model()
    print("Test Prediction (HRV=60, GSR=10, Sleep=7, Caff=2):", predict_recovery(60, 10, 7, 2), "min")
