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
        Uses scientifically accurate wave superposition (RSA, Mayer Waves) for realism.
        """
        if not self.is_running:
            return {k: v for k, v in self.baselines.items()}
            
        elapsed = time.time() - self.start_time
        
        # --- 1. Heart Rate Variability (RSA Model) ---
        # Scientific Basis: 
        # - RSA (Respiratory Sinus Arrhythmia): ~0.25 Hz (Breathing rate ~15 bpm)
        # - Mayer Waves (Baroreflex): ~0.1 Hz (Blood pressure oscillation)
        
        # Determine State Parameters
        if self.stress_active:
            # Stress: Low HRV, suppressed RSA, dominant low-frequency Mayer waves
            hrv_target = 40.0
            rsa_amp = 2.0   # Suppressed breathing influence
            mayer_amp = 8.0 # Dominant sympathetic oscillation
            smoothing = 0.1
        elif self.recovery_active:
            # Recovery: High HRV, dominant RSA (deep breathing)
            hrv_target = 90.0
            rsa_amp = 20.0  # Deep breathing
            mayer_amp = 4.0
            smoothing = 0.05
        else:
            # Baseline: Balanced
            hrv_target = 65.0
            rsa_amp = 10.0
            mayer_amp = 5.0
            smoothing = 0.05
            
        # Smooth baseline transition
        self.baselines['hrv'] += (hrv_target - self.baselines['hrv']) * smoothing
        
        # Wave Superposition Formula
        # HRV(t) = Baseline + RSA * sin(2π * 0.25 * t) + Mayer * sin(2π * 0.1 * t) + Noise
        hrv_val = self.baselines['hrv'] + \
                  (rsa_amp * math.sin(2 * math.pi * 0.25 * elapsed)) + \
                  (mayer_amp * math.sin(2 * math.pi * 0.1 * elapsed)) + \
                  random.gauss(0, 1.0) # Low noise for cleaner signal
        
        # --- 2. Galvanic Skin Response (GSR) ---
        # Scientific Basis:
        # - Tonic (SCL): Slow drifting baseline (minutes)
        # - Phasic (SCR): Rapid peaks (seconds) in response to arousal
        
        if self.stress_active:
            gsr_target = 18.0 # High arousal
            smoothing = 0.08
        elif self.recovery_active:
            gsr_target = 3.0  # Deep relaxation
            smoothing = 0.05
        else:
            # Natural drift
            gsr_target = 8.0 + (2.0 * math.sin(elapsed * 0.05))
            smoothing = 0.02
            
        self.baselines['gsr'] += (gsr_target - self.baselines['gsr']) * smoothing
        
        # Phasic Bursts (SCRs)
        # Instead of random noise, we add smooth "bumps"
        # We simulate a burst if a random threshold is met, decaying over time
        scr_val = 0
        if self.stress_active:
             # Frequent bursts in stress
             scr_val = 2.0 * math.sin(elapsed * 0.5) if math.sin(elapsed * 0.5) > 0 else 0
        
        gsr_val = self.baselines['gsr'] + scr_val + random.gauss(0, 0.05)
        
        # --- 3. Facial Stress ---
        if self.stress_active:
            facial_target = 90.0
        elif self.recovery_active:
            facial_target = 5.0
        else:
            facial_target = 15.0 + (5.0 * math.sin(elapsed * 0.1))
            
        self.baselines['facial'] += (facial_target - self.baselines['facial']) * 0.1
        facial_val = self.baselines['facial'] + random.gauss(0, 1.0)
        
        # --- 4. pH Level ---
        ph_val = 7.35 + (0.05 * math.sin(elapsed * 0.2)) + random.gauss(0, 0.002)
        
        # --- 5. Temperature ---
        if self.stress_active:
            temp_target = 35.5
        elif self.recovery_active:
            temp_target = 37.0
        else:
            temp_target = 36.6 + (0.2 * math.cos(elapsed * 0.05))
            
        self.baselines['temp'] += (temp_target - self.baselines['temp']) * 0.01
        temp_val = self.baselines['temp'] + random.gauss(0, 0.02)

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
