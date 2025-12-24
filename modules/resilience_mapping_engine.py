"""
Community Resilience Mapping - Data Engine
Population-level analytics for environmental stress patterns.
K-anonymized aggregation with strict privacy safeguards.
"""
import numpy as np
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class ResilienceMappingEngine:
    """
    Core calculation engine for Community Resilience Mapping.
    
    PRIVACY-FIRST ARCHITECTURE:
    - Minimum N threshold (K≥10)
    - Automatic suppression if N < threshold
    - No individual-level data exposure
    - K-anonymization enforced
    """
    
    def __init__(self, min_n=10):
        """
        Initialize mapping engine.
        
        Args:
            min_n: Minimum participants per location (default: 10)
        """
        self.min_n = min_n
        
        # Sample locations for demonstration
        self.locations = [
            {
                'name': 'Science Wing',
                'type': 'classroom',
                'building': 'Main Building',
                'capacity': 120
            },
            {
                'name': 'Library',
                'type': 'study_space',
                'building': 'Library Building',
                'capacity': 200
            },
            {
                'name': 'Sports Hall',
                'type': 'sports',
                'building': 'Athletics Complex',
                'capacity': 150
            },
            {
                'name': 'Cafeteria',
                'type': 'dining',
                'building': 'Student Center',
                'capacity': 300
            },
            {
                'name': 'Computer Lab',
                'type': 'lab',
                'building': 'Tech Building',
                'capacity': 80
            }
        ]
    
    def aggregate_location_data(self, location_name: str, time_window: str = 'week') -> Optional[Dict]:
        """
        Aggregate resilience data for a location.
        
        PRIVACY SAFEGUARD: Returns None if N < min_n
        
        Args:
            location_name: Name of location
            time_window: 'day', 'week', or 'month'
        
        Returns:
            Aggregated data dict or None if suppressed
        """
        # Simulate participant count (always ≥ min_n for demo)
        participant_count = random.randint(self.min_n, 150)
        
        # PRIVACY CHECK: Suppress if below threshold
        if participant_count < self.min_n:
            return None
        
        # Generate aggregated RQ scores (no individual data)
        rq_scores = [random.randint(35, 95) for _ in range(participant_count)]
        avg_rq = int(np.mean(rq_scores))
        
        # Calculate recovery speed (aggregated)
        recovery_times = [random.uniform(3, 10) for _ in range(participant_count)]
        avg_recovery_minutes = np.mean(recovery_times)
        recovery_str = f"{int(avg_recovery_minutes)}:{int((avg_recovery_minutes % 1) * 60):02d}"
        
        # Calculate stress event frequency
        stress_events = [random.randint(5, 30) for _ in range(participant_count)]
        avg_stress_events = int(np.mean(stress_events))
        
        # Unresolved stress percentage
        unresolved_pct = random.randint(5, 35)
        
        return {
            'location': location_name,
            'participant_count': participant_count,
            'avg_rq': avg_rq,
            'avg_recovery_speed': recovery_str,
            'avg_stress_events': avg_stress_events,
            'unresolved_stress_pct': unresolved_pct,
            'time_window': time_window
        }
    
    def calculate_composite_resilience(self, location_data: Dict) -> Dict:
        """
        Calculate composite resilience score with color band.
        
        Args:
            location_data: Aggregated location data
        
        Returns:
            Dict with score, color_band, and trend
        """
        score = location_data['avg_rq']
        
        # Determine color band
        if score >= 75:
            color_band = 'green'
            label = 'Adaptive'
        elif score >= 50:
            color_band = 'yellow'
            label = 'Moderate Load'
        else:
            color_band = 'red'
            label = 'High Strain'
        
        # Simulate trend (would be calculated from historical data)
        trend_value = random.choice([-5, -2, 0, 2, 5])
        if trend_value > 2:
            trend = 'improving'
        elif trend_value < -2:
            trend = 'declining'
        else:
            trend = 'stable'
        
        return {
            'composite_resilience': score,
            'color_band': color_band,
            'label': label,
            'trend': trend,
            'trend_value': trend_value
        }
    
    def generate_peak_stress_times(self, location_name: str) -> Dict[str, int]:
        """
        Generate hourly stress intensity histogram.
        
        Args:
            location_name: Name of location
        
        Returns:
            Dict mapping hour to stress intensity (0-100)
        """
        peak_times = {}
        
        # School hours: 8 AM - 6 PM
        for hour in range(8, 19):
            # Simulate stress patterns
            if hour in [9, 14]:  # Peak times (class start, post-lunch)
                intensity = random.randint(60, 85)
            elif hour in [12, 17]:  # Lower times (lunch, end of day)
                intensity = random.randint(30, 50)
            else:
                intensity = random.randint(40, 70)
            
            peak_times[f"{hour:02d}:00"] = intensity
        
        return peak_times
    
    def calculate_recovery_patterns(self, location_data: Dict) -> Dict:
        """
        Calculate recovery pattern metrics.
        
        Args:
            location_data: Aggregated location data
        
        Returns:
            Dict with recovery metrics
        """
        # Institutional baseline (simulated)
        baseline_recovery = "5:30"
        baseline_unresolved = 15
        
        # Compare to baseline
        current_recovery = location_data['avg_recovery_speed']
        current_unresolved = location_data['unresolved_stress_pct']
        
        # Calculate comparison
        recovery_comparison = "faster" if current_recovery < baseline_recovery else "slower"
        unresolved_comparison = "lower" if current_unresolved < baseline_unresolved else "higher"
        
        return {
            'avg_recovery_speed': current_recovery,
            'unresolved_stress_pct': current_unresolved,
            'baseline_recovery': baseline_recovery,
            'baseline_unresolved': baseline_unresolved,
            'recovery_comparison': recovery_comparison,
            'unresolved_comparison': unresolved_comparison
        }
    
    def get_environmental_factors(self, location_name: str) -> Dict:
        """
        Get environmental correlates for a location.
        
        Args:
            location_name: Name of location
        
        Returns:
            Dict with environmental factors
        """
        # Simulate environmental data
        noise_levels = ['low', 'moderate', 'high']
        occupancy_levels = ['low', 'moderate', 'high']
        activities = ['lecture', 'exam', 'study', 'break', 'lab work']
        
        return {
            'noise_level': random.choice(noise_levels),
            'occupancy_density': random.choice(occupancy_levels),
            'primary_activity': random.choice(activities)
        }
    
    def generate_action_items(self, locations_data: List[Dict]) -> List[Dict]:
        """
        Generate data-driven administrative action items.
        
        Args:
            locations_data: List of location data with resilience scores
        
        Returns:
            List of action items with priority, rationale, and suggestions
        """
        action_items = []
        
        for loc_data in locations_data:
            score = loc_data['composite_resilience']
            location = loc_data['location']
            
            # High priority (red) - High strain locations
            if score < 50:
                action_items.append({
                    'priority': 'high',
                    'color': 'red',
                    'location': location,
                    'trigger': f"Composite resilience score: {score}/100",
                    'confidence': 'High',
                    'rationale': f"{location} shows sustained high strain patterns. Consider environmental or schedule modifications.",
                    'suggested_response': 'Schedule adjustment or environmental modification',
                    'category': 'Immediate attention recommended'
                })
            
            # Medium priority (yellow) - Moderate load
            elif score < 75:
                action_items.append({
                    'priority': 'medium',
                    'color': 'yellow',
                    'location': location,
                    'trigger': f"Composite resilience score: {score}/100",
                    'confidence': 'Moderate',
                    'rationale': f"{location} shows moderate load. Monitor for trends and consider preventive measures.",
                    'suggested_response': 'Continued monitoring',
                    'category': 'Preventive consideration'
                })
            
            # Low priority (green) - Adaptive
            else:
                action_items.append({
                    'priority': 'low',
                    'color': 'green',
                    'location': location,
                    'trigger': f"Composite resilience score: {score}/100",
                    'confidence': 'High',
                    'rationale': f"{location} demonstrates strong adaptive patterns. Consider as best practice model.",
                    'suggested_response': 'Document best practices',
                    'category': 'Positive pattern identified'
                })
        
        # Sort by priority (high first)
        priority_order = {'high': 0, 'medium': 1, 'low': 2}
        action_items.sort(key=lambda x: priority_order[x['priority']])
        
        return action_items
    
    def generate_policy_insights(self, locations_data: List[Dict]) -> List[str]:
        """
        Generate population-level policy insights.
        
        Args:
            locations_data: List of location data
        
        Returns:
            List of insight strings
        """
        insights = []
        
        # Calculate overall patterns
        avg_scores = [loc['composite_resilience'] for loc in locations_data]
        overall_avg = np.mean(avg_scores)
        
        # Insight 1: Overall resilience level
        if overall_avg >= 75:
            insights.append(
                "Population-level resilience across campus is strong. "
                "Current environmental configurations appear to support adaptive capacity."
            )
        elif overall_avg >= 50:
            insights.append(
                "Population-level resilience shows moderate patterns. "
                "Consider targeted environmental optimizations in specific zones."
            )
        else:
            insights.append(
                "Population-level resilience indicates systemic strain patterns. "
                "Comprehensive environmental and schedule review recommended."
            )
        
        # Insight 2: Variability across locations
        score_std = np.std(avg_scores)
        if score_std > 15:
            insights.append(
                "Significant variability detected across locations. "
                "This suggests environmental factors play a substantial role in resilience outcomes."
            )
        
        # Insight 3: Temporal patterns
        insights.append(
            "Peak stress times consistently occur during mid-morning (9-10 AM) and early afternoon (2-3 PM). "
            "Consider schedule modifications or break periods during these windows."
        )
        
        return insights
    
    def suppress_if_below_threshold(self, data: Dict) -> Optional[Dict]:
        """
        Privacy guard: Suppress data if participant count < min_n.
        
        Args:
            data: Location data with participant_count
        
        Returns:
            Data if N ≥ min_n, None otherwise
        """
        if data.get('participant_count', 0) < self.min_n:
            return None
        return data
    
    def get_all_locations_data(self, time_window: str = 'week') -> List[Dict]:
        """
        Get aggregated data for all locations.
        
        Args:
            time_window: 'day', 'week', or 'month'
        
        Returns:
            List of location data dicts (only those meeting min_n threshold)
        """
        all_data = []
        
        for location in self.locations:
            # Aggregate data
            loc_data = self.aggregate_location_data(location['name'], time_window)
            
            # Privacy check
            if loc_data is None:
                continue
            
            # Calculate composite resilience
            resilience = self.calculate_composite_resilience(loc_data)
            
            # Combine data
            combined = {
                **loc_data,
                **resilience,
                'location_type': location['type'],
                'building': location['building']
            }
            
            all_data.append(combined)
        
        return all_data
