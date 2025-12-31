import time
import math
import random
import pandas as pd
import numpy as np
import streamlit as st

from modules.sensor_manager import sensor_manager

class DataEngine:
    """
    Handles all physiological data generation, simulation, and external data loading.
    Now delegates real-time Sensing to SensorManager.
    """
    
    def __init__(self):
        self.start_time = None
        self.is_running = False
        self.events = []
        
        # We now pull baselines from SensorManager if active
        
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
        self.log_event("Stress Spike", "Manual Trigger")
        
    def trigger_recovery(self):
        self.log_event("Recovery Marker", "Manual Trigger")

    def get_session_duration(self):
        if not self.start_time:
            return "00:00"
        elapsed = int(time.time() - self.start_time)
        mins, secs = divmod(elapsed, 60)
        return f"{mins:02d}:{secs:02d}"

    def get_live_data(self):
        """
        Retrieves the latest packet from the active SensorManager strategy.
        """
        if not self.is_running:
            # Return static defaults if not running
            return {
                'hrv': 65.0, 'gsr': 8.0, 'facial': 15.0, 
                'ph': 7.35, 'temp': 36.6, 'hr': 70.0,
                'blink_rate': 12.0, 'emotion': 'Neutral'
            }
            
        # Get Real (or Simulated) Readings from the Manager
        readings = sensor_manager.get_readings()
        
        # Map SensorManager keys to DataEngine keys (maintain backward compatibility)
        return {
            'hrv': readings.get('hrv', 65.0),
            'gsr': readings.get('gsr', 8.0), # Helper logic might be needed if mapped differently
            'facial': readings.get('facial_stress', 15.0),
            'ph': 7.35, # pH is not easily measurable via webcam
            'temp': readings.get('temp', 36.6),
            'hr': readings.get('hr', 70.0),
            'blink_rate': readings.get('blink_rate', 12.0),
            'emotion': readings.get('emotion', 'Neutral'),
            'confidence': readings.get('confidence', 0.0)
        }

    def load_csv_data(self, filepath):
        try:
            df = pd.read_csv(filepath)
            return df
        except FileNotFoundError:
            return None

# Singleton instance for global access
data_engine = DataEngine()
