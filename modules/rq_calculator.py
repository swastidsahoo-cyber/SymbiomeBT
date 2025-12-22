"""
Resilience Quotient (RQ) Calculator.
Quantifies nervous system performance using multi-modal biometric inputs.
"""
from typing import Dict, List
import numpy as np

class RQCalculator:
    """
    Calculates the Resilience Quotient based on three main pillars:
    1. Resistance (Stress Absorption)
    2. Recovery (Vagal Velocity)
    3. Stability (Neural Variance)
    """
    
    def __init__(self):
        self.weights = {
            'resistance': 0.35,
            'recovery': 0.45,
            'stability': 0.20
        }
    
    def calculate_score(self, session_data: List[Dict]) -> Dict:
        """
        Processes historical session data to produce a current RQ.
        """
        if not session_data:
            return {'overall': 65.0, 'resistance': 60.0, 'recovery': 65.0, 'stability': 70.0}
            
        hrvs = [s['hrv'] for s in session_data]
        recoveries = [s['recovery_time'] for s in session_data]
        
        # 1. Resistance (Average HRV relative to population baseline)
        avg_hrv = np.mean(hrvs)
        resistance_score = (avg_hrv / 85.0) * 100
        
        # 2. Recovery (Inverse of recovery time)
        # Assuming < 180s is elite (100 pts), > 600s is poor (40 pts)
        avg_rec = np.mean(recoveries)
        recovery_score = 100 - (avg_rec - 180) * (60/420)
        
        # 3. Stability (Standard Deviation of HRV)
        # Higher SDNN is generally better for health, but here we look for stability
        stability_score = 100 - (np.std(hrvs) * 2) 
        
        # Final weighted sum
        overall = (resistance_score * self.weights['resistance'] + 
                   recovery_score * self.weights['recovery'] + 
                   stability_score * self.weights['stability'])
        
        return {
            'overall': round(np.clip(overall, 0, 100), 1),
            'resistance': round(np.clip(resistance_score, 0, 100), 1),
            'recovery': round(np.clip(recovery_score, 0, 100), 1),
            'stability': round(np.clip(stability_score, 0, 100), 1)
        }

    def get_tier(self, score: float) -> str:
        if score > 85: return "Elite (Nervous System Fortified)"
        if score > 70: return "Dynamic (High Performance)"
        if score > 50: return "Functional (Baseline Stable)"
        return "Vulnerable (Intervention Advised)"
