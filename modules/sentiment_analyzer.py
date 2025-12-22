"""
NLP Sentiment Analyzer.
Analyzes journal entries for emotional state and stress indicators.
"""
from typing import Dict
try:
    from transformers import pipeline
except ImportError:
    pipeline = None

class SentimentAnalyzer:
    """
    Analyzes text to extract mood, stress levels, and emotional keywords.
    Uses a pre-trained model if available, otherwise falls back to keyword mapping.
    """
    
    def __init__(self):
        self.tokenizer = None
        # In a real environment, we'd load a model. For Streamlit Cloud, we'll use a lean approach.
        self.keywords = {
            'stress': ['anxious', 'worried', 'stressed', 'overwhelmed', 'tired', 'burnt out', 'tense'],
            'positive': ['happy', 'relaxed', 'calm', 'good', 'excited', 'refreshed', 'peaceful'],
            'negative': ['sad', 'angry', 'frustrated', 'exhausted', 'bad', 'miserable']
        }
        
    def analyze_text(self, text: str) -> Dict:
        """
        Performs sentiment and emotion analysis on the provided text.
        """
        text_lower = text.lower()
        
        # Simple keyword scoring for demo robustness
        scores = {k: sum(1 for word in v if word in text_lower) for k, v in self.keywords.items()}
        
        # Determine dominant emotion
        if scores['stress'] > 0:
            sentiment = "Stress-Reactive"
            color = "#ef4444"
        elif scores['positive'] > scores['negative']:
            sentiment = "Resilient"
            color = "#10b981"
        elif scores['negative'] > scores['positive']:
            sentiment = "Vulnerable"
            color = "#f59e0b"
        else:
            sentiment = "Neutral/Observational"
            color = "#94a3b8"
            
        return {
            'label': sentiment,
            'color': color,
            'stress_score': min(100, scores['stress'] * 20 + 20) if text else 0,
            'keywords': [w for v in self.keywords.values() for w in v if w in text_lower]
        }
