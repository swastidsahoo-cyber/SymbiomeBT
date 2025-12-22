import random
import numpy as np

class TwinModel:
    """
    The Digital Twin Intelligence Layer.
    Calculates Identity, Resilience Quotient (RQ), and forecasts future states.
    """
    
    def __init__(self):
        # Infer Identity on initialization (simulated inference)
        self.identity = self._infer_identity()
        self.baseline_stability = random.uniform(85, 98) # High stability by default
        self.confidence_score = random.randint(82, 94)
        
    def _infer_identity(self):
        """
        Infers the ANS Sensitivity Class based on 'latent' patterns.
        In a real model, this would cluster historical HRV/GSR patterns.
        """
        phenotypes = [
            "Sympathetic-Dominant",
            "Environment-Reactive",
            "Cognitive Load–Sensitive",
            "Slow-Recovery Phenotype",
            "Vagal-Dissociative"
        ]
        return random.choice(phenotypes)

    def calculate_rq(self, hrv_history, gsr_history):
        """
        Calculates the Resilience Quotient (0-100).
        RQ = Resistance + Recovery Stability - Drift
        """
        if not hrv_history:
            return 85.0 # Default start
            
        # 1. Resistance: Ability to maintain HRV during stress (Variance proxy)
        # Higher variability at rest is good, but stability under load is key.
        # We simplify: High HRV avg = good resistance.
        avg_hrv = np.mean(hrv_history[-20:]) if len(hrv_history) > 20 else 65
        resistance = (avg_hrv / 100) * 40 # Max 40 pts
        
        # 2. Recovery Velocity: How fast it bounces back? 
        # Simulated by looking at recent trend.
        if len(hrv_history) > 5:
            trend = hrv_history[-1] - hrv_history[-5]
            rec_velocity = 30 + clip(trend, -10, 10) # 20-40 pts
        else:
            rec_velocity = 30
            
        # 3. Stability Drift: Long term degradation (simulated noise penalty)
        drift_penalty = random.uniform(0, 10)
        
        rq = resistance + rec_velocity - drift_penalty
        return max(0, min(100, rq))

    def get_rq_breakdown(self, rq_score):
        """Decomposes RQ for the UI."""
        resistance = rq_score * 0.4
        recovery = rq_score * 0.4
        stability = rq_score * 0.2
        return {
            "score": int(rq_score),
            "resistance": int(resistance),
            "recovery": int(recovery),
            "stability": int(stability),
            "trend": random.choice(["↑", "→", "↘"])
        }

    def predict_future(self, current_rq, modifiers):
        """
        Generates a 48-hour forecast based on behavioural modifiers.
        modifiers: dict of {sleep: float, caffeine: float, etc}
        """
        hours = list(range(48))
        
        # Base trajectory (circadian rhythm)
        base_curve = [current_rq + (5 * np.sin(h/24 * 2 * np.pi)) for h in hours]
        
        # Apply Modifiers
        # 1. Sleep: < 7 hours = accumulating drag
        sleep_hours = modifiers.get('sleep', 7.0)
        sleep_impact = 0
        if sleep_hours < 7:
            sleep_deficit = 7 - sleep_hours
            # Decay accumulates over time
            sleep_impact = [-(h * 0.5 * sleep_deficit) for h in hours]
        else:
            # Surplus boost
            sleep_impact = [(h * 0.2) for h in hours]
            
        # 2. Caffeine: Spike then crash
        caffeine_cups = modifiers.get('caffeine', 0)
        caffeine_impact = [0] * 48
        if caffeine_cups > 0:
            # Spike at h=1, Crash at h=5
            for h in range(48):
                if h < 4: caffeine_impact[h] = caffeine_cups * 3
                elif h < 8: caffeine_impact[h] = -(caffeine_cups * 4) # Crash hard
                else: caffeine_impact[h] = -(caffeine_cups * 0.5) # Lingering adenosine
        
        # Combine
        forecast = []
        for i in range(48):
            val = base_curve[i] + sleep_impact[i] + caffeine_impact[i]
            # Add random "life noise"
            val += random.uniform(-2, 2)
            forecast.append(max(10, min(95, val)))
            
        return forecast

    def get_shap_explanation(self, modifiers):
        """
        Returns feature importance for the prediction.
        """
        # Calculate impact magnitude
        sleep_val = abs(modifiers.get('sleep', 7) - 7) * 10
        screen_val = modifiers.get('screen', 2) * 2
        caffeine_val = modifiers.get('caffeine', 1) * 5
        
        total = sleep_val + screen_val + caffeine_val + 10 # +10 base
        
        return {
            "Sleep Quality": sleep_val / total,
            "Screen Time (Night)": screen_val / total,
            "Caffeine Timing": caffeine_val / total,
            "Exercise Duration": 0.1, # Static for now
            "Environmental Noise": 0.05
        }

    def calculate_recovery_kinetics(self):
        """
        Calculates recovery dynamics.
        Returns:
            - half_life (minutes): Time to recover 50% of baseline.
            - recovery_velocity (units/min): Speed of recovery.
        """
        # Simulated metrics based on identity
        base_half_life = 8.5 # minutes
        
        # Modify based on stability
        metrics = {
            "half_life": base_half_life + random.uniform(-1, 2),
            "full_recovery_time": (base_half_life * 2) + random.uniform(0, 5),
            "velocity": "Moderate-Fast",
            "historical_comparison": "+12% vs User Avg"
        }
        return metrics

    def get_intervention_readiness(self, rq_score):
        """
        Determines if the system expects an intervention.
        """
        if rq_score < 40:
            return {
                "status": "Ready",
                "label": "INTERVENTION ELIGIBILITY DETECTED",
                "color": "#ef4444",
                "action": "Initiate Coherence Protocol",
                "confidence": "High (92%)"
            }
        elif rq_score < 70:
            return {
                "status": "Optional",
                "label": "PREVENTATIVE MAINTENANCE SUGGESTED",
                "color": "#f59e0b",
                "action": "Suggest Hydration + 2m Breathe",
                "confidence": "Moderate (78%)"
            }
        else:
            return {
                "status": "Standby",
                "label": "SYSTEM STABLE - NO INTERVENTION",
                "color": "#10b981",
                "action": "Continue Passive Monitoring",
                "confidence": "High (95%)"
            }

def clip(val, min_val, max_val):
    return max(min_val, min(val, max_val))
