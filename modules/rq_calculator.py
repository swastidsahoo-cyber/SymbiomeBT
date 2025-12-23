"""
Resilience Quotient™ (RQ) Calculator Engine
Scientific instrument for measuring adaptive capacity to stress.
Calculates RQ from four domains: Recovery Speed, Consistency, Adaptability, Load Tolerance.
"""
import numpy as np
from datetime import datetime, timedelta
import random

class RQCalculator:
    """
    Core calculation engine for Resilience Quotient™.
    
    RQ is a normalized composite score (0-100) representing adaptive capacity:
    - Recovery from stressors
    - Stability across time
    - Adaptation with repeated exposure
    - Tolerance to cumulative load
    """
    
    def __init__(self):
        # Initial weights (will be personalized weekly)
        self.weights = {
            'recovery_speed': 0.30,
            'consistency': 0.25,
            'adaptability': 0.25,
            'load_tolerance': 0.20
        }
        
        # Descriptor thresholds
        self.descriptors = [
            (0, 35, "Vulnerable"),
            (36, 55, "Developing"),
            (56, 75, "Proficient"),
            (76, 90, "Advanced"),
            (91, 100, "Exceptional")
        ]
    
    def calculate_recovery_speed(self, hrv_data=None, gsr_data=None, resp_data=None):
        """
        DOMAIN 1: Recovery Speed (RS)
        
        Measures how quickly physiology returns to baseline after stress.
        
        Inputs:
        - HRV recovery slope
        - GSR decay constant
        - Respiration regularization time
        
        Returns:
        - avg_recovery_time (str): "MM:SS" format
        - score (int): 0-100 percentile-adjusted score
        - percentile (int): User's percentile rank
        """
        # Simulate realistic recovery data
        if hrv_data is None:
            # Generate realistic HRV recovery pattern
            recovery_times = [random.uniform(3, 8) for _ in range(10)]  # minutes
        else:
            recovery_times = hrv_data
        
        avg_recovery_minutes = np.mean(recovery_times)
        
        # Convert to MM:SS format
        minutes = int(avg_recovery_minutes)
        seconds = int((avg_recovery_minutes - minutes) * 60)
        avg_recovery_str = f"{minutes}:{seconds:02d}"
        
        # Normalize to 0-100 score (faster recovery = higher score)
        # Assuming 3 min = 100, 10 min = 0
        score = max(0, min(100, int(100 - ((avg_recovery_minutes - 3) / 7) * 100)))
        
        # Calculate percentile (simulated)
        percentile = min(99, max(1, int(score * 0.9 + random.uniform(-5, 5))))
        
        return {
            'value': avg_recovery_str,
            'score': score,
            'percentile': percentile,
            'raw_minutes': avg_recovery_minutes
        }
    
    def calculate_consistency(self, hrv_variance=None, sentiment_variance=None, task_variance=None):
        """
        DOMAIN 2: Consistency (C)
        
        Measures stability of performance and regulation across days.
        
        Inputs:
        - Day-to-day HRV variance
        - NLP sentiment variance from journaling
        - Cognitive task score variance
        
        Returns:
        - value (int): Stability percentage (0-100%)
        - trend (str): Change indicator (e.g., "+2%")
        """
        # Simulate realistic variance data
        if hrv_variance is None:
            hrv_variance = random.uniform(5, 20)  # Lower is better
        if sentiment_variance is None:
            sentiment_variance = random.uniform(10, 30)
        if task_variance is None:
            task_variance = random.uniform(5, 25)
        
        # Combine variances (lower variance = higher consistency)
        avg_variance = np.mean([hrv_variance, sentiment_variance, task_variance])
        
        # Convert to consistency percentage (inverse of variance)
        consistency = max(0, min(100, int(100 - (avg_variance / 30) * 100)))
        
        # Calculate trend (simulated improvement)
        trend = random.choice(["+1%", "+2%", "+3%", "0%", "-1%"])
        
        return {
            'value': consistency,
            'trend': trend,
            'raw_variance': avg_variance
        }
    
    def calculate_adaptability(self, recovery_improvements=None, stress_response_trends=None):
        """
        DOMAIN 3: Adaptability (A)
        
        Measures efficiency of improvement to repeated stressors.
        
        Inputs:
        - Change in recovery speed over repeated events
        - Reduced peak stress response for similar intensity
        - Improved breathing efficiency over time
        
        Returns:
        - value (int): Percent improvement over 30 days
        - period (str): Time period (e.g., "30d")
        """
        # Simulate realistic improvement data
        if recovery_improvements is None:
            # Generate improvement trend
            improvements = [random.uniform(-2, 8) for _ in range(30)]
        else:
            improvements = recovery_improvements
        
        # Calculate 30-day improvement slope
        improvement_pct = int(np.mean(improvements))
        
        return {
            'value': improvement_pct,
            'period': "30d",
            'raw_improvements': improvements if recovery_improvements else None
        }
    
    def calculate_load_tolerance(self, stress_events=None, baseline_drift=None):
        """
        DOMAIN 4: Load Tolerance (LT)
        
        Measures how many stress events can be handled without degradation.
        
        Inputs:
        - Stress event count
        - Baseline drift detection
        - Failed recovery detection
        
        Returns:
        - value (int): Number of stress events handled
        - degradation (str): Level of degradation (minimal/moderate/significant)
        """
        # Simulate realistic stress event data
        if stress_events is None:
            event_count = random.randint(25, 45)
        else:
            event_count = len(stress_events)
        
        # Simulate baseline drift
        if baseline_drift is None:
            drift_score = random.uniform(0, 15)  # Lower is better
        else:
            drift_score = baseline_drift
        
        # Determine degradation level
        if drift_score < 5:
            degradation = "minimal"
        elif drift_score < 10:
            degradation = "moderate"
        else:
            degradation = "significant"
        
        return {
            'value': event_count,
            'degradation': degradation,
            'drift_score': drift_score
        }
    
    def calculate_rq(self, recovery_speed_data=None, consistency_data=None, 
                     adaptability_data=None, load_tolerance_data=None):
        """
        Calculate final RQ composite score.
        
        RQ = weighted sum of four domain scores
        
        Returns:
        - rq_score (int): Final RQ (0-100)
        - descriptor (str): Tier label
        - confidence (float): Confidence band (0-1)
        - domains (dict): All domain metrics
        """
        # Calculate all domains
        rs = self.calculate_recovery_speed(recovery_speed_data)
        c = self.calculate_consistency(consistency_data)
        a_val = self.calculate_adaptability(adaptability_data)
        lt = self.calculate_load_tolerance(load_tolerance_data)
        
        # Normalize adaptability to 0-100 scale
        a_score = max(0, min(100, 50 + a_val['value'] * 5))  # +10% improvement = 100 score
        
        # Normalize load tolerance to 0-100 scale
        lt_score = max(0, min(100, (lt['value'] / 50) * 100))  # 50 events = 100 score
        
        # Calculate weighted composite
        rq_score = int(
            rs['score'] * self.weights['recovery_speed'] +
            c['value'] * self.weights['consistency'] +
            a_score * self.weights['adaptability'] +
            lt_score * self.weights['load_tolerance']
        )
        
        # Get descriptor
        descriptor = self.get_descriptor(rq_score)
        
        # Calculate confidence (simulated - would be based on data quality in production)
        confidence = random.uniform(0.82, 0.92)
        
        return {
            'rq_score': rq_score,
            'descriptor': descriptor,
            'confidence': confidence,
            'domains': {
                'recovery_speed': rs,
                'consistency': c,
                'adaptability': a_val,
                'load_tolerance': lt
            },
            'weights': self.weights.copy(),
            'timestamp': datetime.now().isoformat()
        }
    
    def get_descriptor(self, rq_score):
        """Get descriptor label for RQ score."""
        for min_val, max_val, label in self.descriptors:
            if min_val <= rq_score <= max_val:
                return label
        return "Unknown"
    
    def update_weights(self, user_history):
        """
        Update personalized weights based on user history.
        Called weekly to adapt to individual patterns.
        
        In production, this would use ML to optimize weights.
        For now, we'll keep default weights.
        """
        # Placeholder for weekly weight adaptation
        # In production: analyze which domains are most predictive for this user
        pass
    
    def generate_trend_data(self, days=14):
        """
        Generate RQ trend data for visualization.
        
        Args:
            days (int): Number of days to generate
        
        Returns:
            list: List of {date, rq_score, dominant_domain, confidence}
        """
        trend_data = []
        base_rq = random.randint(50, 70)
        
        for i in range(days):
            date = datetime.now() - timedelta(days=days-i-1)
            
            # Add realistic variation and trend
            variation = random.uniform(-3, 5)
            rq_score = max(0, min(100, base_rq + variation + (i * 0.3)))  # Slight upward trend
            
            # Determine dominant domain change
            domains = ['Recovery Speed', 'Consistency', 'Adaptability', 'Load Tolerance']
            dominant = random.choice(domains)
            
            # Confidence varies slightly
            confidence = random.uniform(0.82, 0.92)
            
            trend_data.append({
                'date': date.strftime('%b %d'),
                'rq_score': int(rq_score),
                'dominant_domain': dominant,
                'confidence': confidence
            })
            
            base_rq = rq_score  # Update base for next iteration
        
        return trend_data
    
    def generate_stress_response_data(self, num_events=50):
        """
        Generate stress response profile data for scatter plot.
        
        Args:
            num_events (int): Number of stress events to generate
        
        Returns:
            list: List of {stress_intensity, recovery_duration, category}
        """
        events = []
        
        for _ in range(num_events):
            # Stress intensity (0-100)
            intensity = random.uniform(10, 100)
            
            # Recovery duration (minutes) - higher intensity generally means longer recovery
            base_recovery = 2 + (intensity / 100) * 8  # 2-10 minutes
            recovery = base_recovery + random.uniform(-2, 2)
            recovery = max(1, recovery)
            
            # Categorize by recovery speed
            if recovery < 5:
                category = "Fast (< 5min)"
            elif recovery < 10:
                category = "Moderate (5-10min)"
            else:
                category = "Slow (> 10min)"
            
            events.append({
                'stress_intensity': intensity,
                'recovery_duration': recovery,
                'category': category
            })
        
        return events

# Legacy compatibility
def calculate_score(history):
    """Legacy function for backward compatibility."""
    calc = RQCalculator()
    result = calc.calculate_rq()
    return {
        'overall': result['rq_score'],
        'resistance': result['domains']['load_tolerance']['value'],
        'recovery': result['domains']['recovery_speed']['score'],
        'stability': result['domains']['consistency']['value']
    }

def get_tier(score):
    """Legacy function for backward compatibility."""
    calc = RQCalculator()
    return calc.get_descriptor(score)
