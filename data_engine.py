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

    def get_session_duration(self):
        """Returns formatted session duration (MM:SS)."""
        if not self.start_time:
            return "00:00"
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        return f"{mins:02d}:{secs:02d}"

    def get_live_data(self):
        """
        Generates live data point based on time and current state.
        Uses complex wave superposition and Gaussian noise for realism.
        """
        if not self.is_running:
            return {k: v for k, v in self.baselines.items()}
            
    def get_live_data(self):
        """
        Generates live data point based on time and current state.
        Uses complex wave superposition, random drift, and Gaussian noise for realism.
        """
        if not self.is_running:
            return {k: v for k, v in self.baselines.items()}
            
        elapsed = time.time() - self.start_time
        
        # --- 1. Heart Rate Variability (RSA Model) ---
        # Natural Drift: The "center" of the HRV wanders slightly
        drift = math.sin(elapsed * 0.05) * 5 
        
        if self.stress_active:
            hrv_target = 40.0 # Sharp drop
            hrv_amp = 3       # Rigid, low variability (Stress)
            smoothing = 0.1   # Fast reaction
        elif self.recovery_active:
            hrv_target = 90.0 # High peak
            hrv_amp = 25      # Huge respiratory sinus arrhythmia (Deep breathing)
            smoothing = 0.05
        else:
            # Normal wandering baseline
            hrv_target = 65.0 + drift 
            hrv_amp = 12      # Healthy variability
            smoothing = 0.05
            
        self.baselines['hrv'] += (hrv_target - self.baselines['hrv']) * smoothing
        
        # Complex wave: RSA (fast, 0.25Hz) + Mayer (slow, 0.1Hz) + Noise
        # We use slightly different frequencies to create "beating" patterns
        hrv_val = self.baselines['hrv'] + \
                  (hrv_amp * math.sin(elapsed * 1.5)) + \
                  (hrv_amp * 0.6 * math.sin(elapsed * 0.4)) + \
                  random.gauss(0, 2.0)
        
        # --- 2. Galvanic Skin Response (GSR) ---
        # Spontaneous fluctuations (NS-SCRs)
        if self.stress_active:
            gsr_target = 15.0 # High arousal
            smoothing = 0.08
        elif self.recovery_active:
            gsr_target = 3.0  # Deep relaxation
            smoothing = 0.05
        else:
            # Slow wandering
            gsr_target = 8.0 + (math.cos(elapsed * 0.03) * 2)
            smoothing = 0.02
            
        self.baselines['gsr'] += (gsr_target - self.baselines['gsr']) * smoothing
        
        # GSR has "bursts" rather than smooth waves
        burst = 0
        if random.random() > 0.95: # Occasional random spikes
            burst = random.uniform(0.5, 1.5)
            
        gsr_val = self.baselines['gsr'] + \
                  (0.5 * math.cos(elapsed * 0.1)) + \
                  burst + \
                  random.gauss(0, 0.1)
        
        # --- 3. Facial Stress ---
        if self.stress_active:
            facial_target = 90.0
        elif self.recovery_active:
            facial_target = 5.0
        else:
            facial_target = 15.0 + (math.sin(elapsed * 0.1) * 5)
            
        self.baselines['facial'] += (facial_target - self.baselines['facial']) * 0.1
        facial_val = self.baselines['facial'] + random.gauss(0, 3.0)
        
        # --- 4. pH Level ---
        # Tends to be stable but fluctuates with "breathing" logic
        ph_val = 7.35 + (math.sin(elapsed * 0.2) * 0.03) + random.gauss(0, 0.01)
        
        # --- 5. Temperature ---
        if self.stress_active:
            temp_target = 35.5 # Vasoconstriction (Cold hands)
        elif self.recovery_active:
            temp_target = 37.0 # Vasodilation (Warm hands)
        else:
            temp_target = 36.6 + (math.cos(elapsed * 0.05) * 0.2)
            
        self.baselines['temp'] += (temp_target - self.baselines['temp']) * 0.01
        temp_val = self.baselines['temp'] + random.gauss(0, 0.03)

        return {
            'hrv': max(10, min(120, hrv_val)),
            'gsr': max(1, min(25, gsr_val)),
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
