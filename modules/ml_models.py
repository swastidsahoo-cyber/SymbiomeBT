"""
Machine Learning Models for Resilience Forecasting.
Implements time-series prediction models.
"""
import numpy as np
from typing import List, Tuple

class PredictiveModels:
    """
    Simulates advanced time-series forecasting (LSTM/Prophet style).
    Predicts future resilience states based on historical signals.
    """
    
    @staticmethod
    def forecast_sri(history: List[float], horizon_hours: int = 4) -> Tuple[np.ndarray, np.ndarray]:
        """
        Predicts future SRI values and confidence intervals.
        """
        if len(history) < 5:
            history = [65.0, 68.0, 64.0, 70.0, 72.0]
            
        # Mocking a learned trend using a polynomial fit + noise
        x = np.arange(len(history))
        poly = np.polyfit(x, history, 1)
        
        future_x = np.arange(len(history), len(history) + horizon_hours)
        prediction = np.polyval(poly, future_x)
        
        # Add some seasonality (simulating circadian rhythm influence)
        prediction += 5 * np.sin(future_x / 2.0)
        
        # Confidence intervals
        upper = prediction + 5.0
        lower = prediction - 5.0
        
        return prediction, upper, lower

    @staticmethod
    def calculate_risk_probability(current_sri: float, trend: float) -> float:
        """Determines the probability of a stress event in the next 60 mins."""
        base_prob = (100 - current_sri) / 100.0
        if trend < 0:
            base_prob += abs(trend) * 0.1
        return min(0.95, max(0.05, base_prob))
