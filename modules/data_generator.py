import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta

# ==========================================
# SYMBIOME DATA GENERATION ENGINE
# ==========================================
# This script generates realistic synthetic physiological data for the Symbiome app.
# It simulates:
# 1. HRV (Heart Rate Variability): Using sine waves to mimic Respiratory Sinus Arrhythmia (RSA).
# 2. GSR (Galvanic Skin Response): Using a random walk model with phasic spikes for stress events.
# 3. Facial Calmness: A bounded random process correlated with HRV.
# ==========================================

def generate_session_data(duration_minutes=10, sampling_rate_hz=1):
    """
    Generates a time-series dataset for a single monitoring session.
    
    Args:
        duration_minutes: Length of the session.
        sampling_rate_hz: Data points per second.
        
    Returns:
        DataFrame containing Timestamp, HRV, GSR, Facial_Calm, Stress_Label.
    """
    total_points = duration_minutes * 60 * sampling_rate_hz
    timestamps = [datetime.now() + timedelta(seconds=i) for i in range(total_points)]
    
    # --- 1. HRV Simulation (The Science) ---
    # We simulate R-R intervals (time between heartbeats).
    # Healthy HRV has a wave-like pattern due to breathing (RSA).
    # Formula: Base_RR + (Breathing_Amplitude * sin(time)) + Noise
    base_hr = 70  # Average Heart Rate
    base_rr = 60000 / base_hr  # Base R-R interval in ms
    
    # Simulate breathing effect (0.25 Hz = 15 breaths/min)
    time_steps = np.arange(total_points)
    breathing_effect = 50 * np.sin(2 * np.pi * 0.25 * (time_steps / sampling_rate_hz))
    
    # Add random noise (autonomic nervous system fluctuations)
    noise = np.random.normal(0, 10, total_points)
    
    rr_intervals = base_rr + breathing_effect + noise
    
    # Calculate HRV (RMSSD approximation for a rolling window would be done in analysis, 
    # here we just store the raw RR or a smoothed "Instantaneous HRV" metric)
    # For the dashboard, we'll generate a "Live HRV Score" (0-100)
    # Higher variance = Higher HRV = Better Resilience
    hrv_score = 50 + (breathing_effect / 2) + np.random.normal(0, 5, total_points)
    hrv_score = np.clip(hrv_score, 0, 100)

    # --- 2. GSR Simulation (The Science) ---
    # GSR (Skin Conductance) has two components:
    # - Tonic (Baseline): Slowly drifting.
    # - Phasic (Spikes): Rapid increases due to stress stimuli.
    
    # Random walk for Tonic
    tonic = np.cumsum(np.random.normal(0, 0.05, total_points)) + 5  # Start at 5 uS
    
    # Add Phasic Spikes (Stress Events)
    phasic = np.zeros(total_points)
    # Inject 3 random stress events
    for _ in range(3):
        event_start = random.randint(0, total_points - 50)
        # Spike shape: Fast rise, slow decay
        spike = np.concatenate([np.linspace(0, 2, 10), np.linspace(2, 0, 40)])
        if event_start + 50 < total_points:
            phasic[event_start:event_start+50] += spike
            
    gsr_raw = tonic + phasic
    # Normalize to 0-100 scale for UI (Inverse: Lower GSR = Calmer)
    gsr_score = 100 - (gsr_raw * 10) 
    gsr_score = np.clip(gsr_score, 0, 100)

    # --- 3. Facial Calmness Simulation ---
    # Correlated with HRV (High HRV usually means calmer face)
    facial_calm = hrv_score * 0.6 + np.random.normal(0, 10, total_points) + 20
    facial_calm = np.clip(facial_calm, 0, 100)

    # --- Create DataFrame ---
    df = pd.DataFrame({
        'Timestamp': timestamps,
        'HRV_Score': hrv_score,
        'GSR_Score': gsr_score,
        'Facial_Calm': facial_calm
    })
    
    return df

def generate_user_history(days=30):
    """
    Generates daily summary data for the 'Resilience Trend' chart.
    """
    dates = [datetime.now().date() - timedelta(days=i) for i in range(days)]
    dates.reverse()
    
    data = []
    current_resilience = 60
    
    for date in dates:
        # Random daily fluctuation
        change = np.random.normal(0, 5)
        
        # Trend: Slowly improving (Learning effect)
        change += 0.5 
        
        current_resilience += change
        current_resilience = np.clip(current_resilience, 30, 95)
        
        data.append({
            'Date': date,
            'Avg_HRV': np.random.randint(40, 80),
            'Avg_GSR': np.random.randint(20, 60),
            'Sleep_Hours': np.random.uniform(5.5, 9.0),
            'Symbiome_Resilience_Score': current_resilience
        })
        
    return pd.DataFrame(data)

if __name__ == "__main__":
    print("Generating Symbiome Datasets...")
    
    # 1. Generate a Live Session (for Monitoring Screen)
    session_df = generate_session_data(duration_minutes=10)
    session_df.to_csv("symbiome/data/simulated_session.csv", index=False)
    print(" - Generated 'simulated_session.csv' (Live Data)")
    
    # 2. Generate User History (for Dashboard Trends)
    history_df = generate_user_history(days=30)
    history_df.to_csv("symbiome/data/user_history.csv", index=False)
    print(" - Generated 'user_history.csv' (Trend Data)")
    
    print("Data Generation Complete. You can edit these CSVs to test different scenarios.")
