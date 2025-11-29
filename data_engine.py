import time
import math
import random
import pandas as pd
import numpy as np
import streamlit as st

class DataEngine:
    """
    Handles all physiological data generation, simulation, and external data loading.
    Designed for transparency in scientific competitions.
    """
    
    def __init__(self):
        self.start_time = None
        self.is_running = False
        self.events = []
        
        # Baseline values (Physiological Norms)
        self.baselines = {
            'hrv': 65.0,    # ms (RMSSD)
            'gsr': 45.0,    # µS (Skin Conductance)
            'facial': 15.0, # % (Stress Detection)
            'ph': 7.35,     # pH (Salivary)
            'temp': 36.6    # °C (Skin Temp)
        }
        
        # Simulation State
        self.stress_active = False
        self.recovery_active = False
        
    def start_session(self):
        """Starts a new monitoring session."""
        self.start_time = time.time()
        self.is_running = True
        self.events = []
        self.log_event("Session Started", "Monitoring initiated")
        
    def stop_session(self):
        """Stops the current session."""
        self.is_running = False
        self.log_event("Session Stopped", "Monitoring ended")
        
    def log_event(self, event_type, description):
        """Logs a timestamped event."""
        timestamp = time.strftime("%H:%M:%S", time.localtime())
        self.events.append({
            "time": timestamp,
            "type": event_type,
            "desc": description
        })
        # Keep only last 50 events
        if len(self.events) > 50:
            self.events.pop(0)
            
    def trigger_stress(self):
        """Simulates an acute stress response."""
        self.stress_active = True
        self.recovery_active = False
        self.log_event("Stress Spike", "Simulated acute stressor")
        
    def trigger_recovery(self):
        """Simulates a recovery/calming response."""
        self.stress_active = False
        self.recovery_active = True
        self.log_event("Recovery Marker", "User initiated recovery protocol")

    def get_live_data(self):
        """
        Generates live data point based on time and current state.
        Returns a dictionary of metrics.
        """
        if not self.is_running:
            return {k: v for k, v in self.baselines.items()}
            
        elapsed = time.time() - self.start_time
        
        # 1. Heart Rate Variability (HRV) - Sine Wave Model
        # Formula: Base + (Amplitude * sin(frequency * time)) + Noise
        hrv_amp = 10
        if self.stress_active:
            hrv_target = 45.0 # Low HRV = High Stress
            hrv_amp = 5
        elif self.recovery_active:
            hrv_target = 85.0 # High HRV = Recovery
            hrv_amp = 15
        else:
            hrv_target = 65.0 # Baseline
            
        # Smooth transition to target (Simple Low-pass filter)
        self.baselines['hrv'] += (hrv_target - self.baselines['hrv']) * 0.05
        
        hrv_val = self.baselines['hrv'] + (hrv_amp * math.sin(elapsed / 3.0)) + random.uniform(-2, 2)
        
        # 2. Galvanic Skin Response (GSR) - Inverse Correlation to HRV
        # Formula: Base + (Amplitude * cos(frequency * time)) + Trend
        if self.stress_active:
            gsr_target = 12.0 # High Conductivity = Sweat/Stress
        elif self.recovery_active:
            gsr_target = 4.0 # Low Conductivity = Calm
        else:
            gsr_target = 8.0
            
        self.baselines['gsr'] += (gsr_target - self.baselines['gsr']) * 0.05
        gsr_val = self.baselines['gsr'] + (0.5 * math.cos(elapsed / 5.0)) + random.uniform(-0.2, 0.2)
        
        # 3. Facial Stress (MediaPipe Simulation)
        # Correlated with Stress State
        if self.stress_active:
            facial_target = 85.0 # High Tension
        elif self.recovery_active:
            facial_target = 5.0 # Relaxed
        else:
            facial_target = 15.0
            
        self.baselines['facial'] += (facial_target - self.baselines['facial']) * 0.1
        facial_val = self.baselines['facial'] + random.uniform(-2, 2)
        
        # 4. pH Level (Metabolic)
        # Slow moving metric
        ph_val = 7.35 + (math.sin(elapsed / 60.0) * 0.05) + random.uniform(-0.01, 0.01)
        
        # 5. Skin Temp
        # Stress -> Vasoconstriction -> Lower Temp
        if self.stress_active:
            temp_target = 35.8
        elif self.recovery_active:
            temp_target = 36.8
        else:
            temp_target = 36.6
            
        self.baselines['temp'] += (temp_target - self.baselines['temp']) * 0.02
        temp_val = self.baselines['temp'] + random.uniform(-0.05, 0.05)

        return {
            'hrv': max(10, min(120, hrv_val)),
            'gsr': max(1, min(20, gsr_val)),
            'facial': max(0, min(100, facial_val)),
            'ph': max(6.8, min(7.8, ph_val)),
            'temp': max(35.0, min(38.0, temp_val))
        }

    def load_csv_data(self, filepath):
        """
        Loads external dataset for analysis.
        Demonstrates ability to handle real-world data.
        """
        try:
            df = pd.read_csv(filepath)
            return df
        except FileNotFoundError:
            return None

# Singleton instance for global access
data_engine = DataEngine()
