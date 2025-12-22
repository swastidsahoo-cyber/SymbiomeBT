"""
Shared utilities for Symbiome platform
"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import hashlib
import json

class DataModels:
    """Shared data models and structures"""
    
    @staticmethod
    def create_session_data(
        sri: float,
        hrv: float,
        gsr: float,
        duration: int,
        session_type: str = "biofeedback"
    ) -> Dict:
        """Create standardized session data structure"""
        return {
            "id": hashlib.md5(str(datetime.now()).encode()).hexdigest()[:12],
            "timestamp": datetime.now().isoformat(),
            "sri": sri,
            "hrv": hrv,
            "gsr": gsr,
            "duration": duration,
            "type": session_type,
            "recovery_time": np.random.randint(180, 600)
        }
    
    @staticmethod
    def calculate_sri(hrv: float, gsr: float, facial_calm: float = 75.0) -> float:
        """Calculate Stress Resilience Index"""
        # Weighted formula: HRV (35%), GSR (30%), Facial (35%)
        normalized_gsr = max(0, 100 - gsr)  # Invert GSR (lower is better)
        sri = (hrv * 0.35) + (normalized_gsr * 0.30) + (facial_calm * 0.35)
        return np.clip(sri, 0, 100)

class TimeSeriesGenerator:
    """Generate realistic time-series data"""
    
    @staticmethod
    def generate_hrv_series(
        base_hrv: float = 65,
        length: int = 100,
        noise_level: float = 5.0
    ) -> np.ndarray:
        """Generate realistic HRV time series"""
        t = np.linspace(0, 10, length)
        # Circadian rhythm + random walk
        circadian = 10 * np.sin(2 * np.pi * t / 24)
        noise = np.random.normal(0, noise_level, length)
        trend = np.cumsum(np.random.normal(0, 0.5, length))
        
        hrv = base_hrv + circadian + noise + trend
        return np.clip(hrv, 30, 100)
    
    @staticmethod
    def generate_gsr_series(
        base_gsr: float = 2.5,
        length: int = 100,
        stress_events: int = 3
    ) -> np.ndarray:
        """Generate realistic GSR time series with stress spikes"""
        gsr = np.ones(length) * base_gsr
        
        # Add stress spikes
        for _ in range(stress_events):
            spike_pos = np.random.randint(10, length - 10)
            spike_magnitude = np.random.uniform(1.5, 3.0)
            spike_width = np.random.randint(5, 15)
            
            for i in range(spike_width):
                if spike_pos + i < length:
                    decay = np.exp(-i / 5)
                    gsr[spike_pos + i] += spike_magnitude * decay
        
        # Add noise
        gsr += np.random.normal(0, 0.2, length)
        return np.clip(gsr, 0.5, 8.0)

class CloudStorage:
    """Cloud storage utilities (Firebase/Supabase)"""
    
    def __init__(self, provider: str = "firebase"):
        self.provider = provider
        self.initialized = False
    
    def initialize(self, credentials: Dict):
        """Initialize cloud storage connection"""
        # Will implement Firebase Admin SDK
        self.initialized = True
        return True
    
    def upload_session(self, session_data: Dict) -> bool:
        """Upload session data to cloud"""
        if not self.initialized:
            return False
        # Implementation will use Firebase Firestore
        return True
    
    def download_sessions(self, user_id: str, days: int = 30) -> List[Dict]:
        """Download user sessions from cloud"""
        if not self.initialized:
            return []
        # Implementation will query Firestore
        return []

def format_duration(seconds: int) -> str:
    """Format duration in human-readable format"""
    if seconds < 60:
        return f"{seconds}s"
    elif seconds < 3600:
        return f"{seconds // 60}m {seconds % 60}s"
    else:
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours}h {minutes}m"

def calculate_percentile(value: float, distribution: List[float]) -> int:
    """Calculate percentile rank of value in distribution"""
    if not distribution:
        return 50
    sorted_dist = sorted(distribution)
    rank = sum(1 for x in sorted_dist if x <= value)
    return int((rank / len(sorted_dist)) * 100)
