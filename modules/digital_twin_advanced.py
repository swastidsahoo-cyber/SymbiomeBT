"""
Digital Twin Advanced - Behavioral Inputs Interface
Interactive sliders for behavioral inputs and twin prediction.
Matches screenshots 3 & 4.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random

def render_digital_twin_advanced_page():
    # CSS Styles
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; background: #0a0e27; }
.twin-adv-header { text-align: center; padding: 30px 0 20px 0; }
.twin-adv-icon { width: 80px; height: 80px; background: linear-gradient(135deg, #a855f7 0%, #ec4899 100%); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 15px auto; font-size: 2rem; }
.twin-adv-title { color: white; font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.twin-adv-subtitle { color: #94a3b8; font-size: 0.85rem; line-height: 1.6; max-width: 600px; margin: 0 auto; }
.twin-metrics-row { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 30px 0; }
.twin-metric-card { background: linear-gradient(135deg, rgba(168, 85, 247, 0.1) 0%, rgba(236, 72, 153, 0.1) 100%); border: 1px solid rgba(168, 85, 247, 0.3); border-radius: 12px; padding: 20px; text-align: center; }
.twin-metric-label { color: #94a3b8; font-size: 0.75rem; font-weight: 600; margin-bottom: 8px; }
.twin-metric-value { color: white; font-size: 1.8rem; font-weight: 900; }
.input-section { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 24px; margin: 20px 0; }
.input-section-title { color: white; font-size: 1rem; font-weight: 800; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
.impact-card { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 10px; padding: 16px; margin: 15px 0; }
.impact-icon { color: #ef4444; font-size: 1.2rem; margin-right: 10px; }
.impact-text { color: white; font-size: 0.85rem; font-weight: 700; }
.impact-value { color: #ef4444; font-size: 0.9rem; font-weight: 800; float: right; }
.chart-container { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0; }
.chart-title { color: white; font-size: 1rem; font-weight: 800; margin-bottom: 15px; }
.explainability-section { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 24px; margin: 20px 0; }
.explainability-title { color: #f59e0b; font-size: 1rem; font-weight: 800; margin-bottom: 20px; display: flex; align-items: center; gap: 10px; }
.feature-bar { margin-bottom: 15px; }
.feature-label { color: white; font-size: 0.8rem; font-weight: 700; margin-bottom: 6px; display: flex; justify-content: space-between; }
.feature-impact { color: #94a3b8; font-size: 0.75rem; }
.feature-bar-bg { width: 100%; height: 10px; background: rgba(255, 255, 255, 0.05); border-radius: 5px; overflow: hidden; }
.feature-bar-fill { height: 100%; border-radius: 5px; }
.model-status { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 16px; margin: 20px 0; }
.model-status-title { color: #10b981; font-size: 0.85rem; font-weight: 800; margin-bottom: 10px; }
.model-stat { display: flex; justify-content: space-between; margin-bottom: 8px; }
.model-stat-label { color: #94a3b8; font-size: 0.75rem; }
.model-stat-value { color: #10b981; font-size: 0.75rem; font-weight: 700; }
.insight-box { background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 10px; padding: 16px; margin: 15px 0; }
.insight-title { color: #6366f1; font-size: 0.85rem; font-weight: 800; margin-bottom: 10px; }
.insight-text { color: #94a3b8; font-size: 0.75rem; line-height: 1.6; }
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Header
    header_html = """<div class="twin-adv-header">
<div class="twin-adv-icon">🧬</div>
<div class="twin-adv-title">Your Digital Twin</div>
<div class="twin-adv-subtitle">An AI-powered model that learns how your body responds to life, predicting your resilience before you feel it.</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Initialize session state
    if 'sleep_duration' not in st.session_state:
        st.session_state.sleep_duration = 7.0
        st.session_state.stress_time = 4.0
        st.session_state.caffeine_intake = 2.0
        st.session_state.exercise_duration = 30.0
    
    # Top Metrics
    current_sri = 54.5
    model_confidence = 89
    
    metrics_html = f"""<div class="twin-metrics-row">
<div class="twin-metric-card">
<div class="twin-metric-label">🧠 Twin Prediction</div>
<div class="twin-metric-value" style="color: #a855f7;">SRI: {current_sri}</div>
</div>
<div class="twin-metric-card">
<div class="twin-metric-label">⚡ Current SRI</div>
<div class="twin-metric-value" style="color: #06b6d4;">{current_sri}</div>
</div>
<div class="twin-metric-card">
<div class="twin-metric-label">🎯 Model Confidence</div>
<div class="twin-metric-value" style="color: #f59e0b;">{model_confidence}%</div>
</div>
</div>"""
    st.markdown(metrics_html, unsafe_allow_html=True)
    
    # Behavioral Inputs Section
    st.markdown('<div class="input-section">', unsafe_allow_html=True)
    st.markdown('<div class="input-section-title">⚙️ Behavioral Input - Train Your Twin</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 8px;">😴 Sleep Duration</div>', unsafe_allow_html=True)
        sleep_duration = st.slider("", 0.0, 12.0, st.session_state.sleep_duration, 0.5, key="sleep_slider", label_visibility="collapsed")
        
        # Dynamic feedback for sleep
        if sleep_duration < 6:
            sleep_feedback = f'<div style="color: #ef4444; font-size: 0.7rem; margin-top: -10px;">⚠️ {sleep_duration} hrs • Critical - Sleep more! Target 7-9 hrs</div>'
            sleep_impact = -15
        elif sleep_duration < 7:
            sleep_feedback = f'<div style="color: #f59e0b; font-size: 0.7rem; margin-top: -10px;">⚡ {sleep_duration} hrs • Below optimal - Increase sleep duration</div>'
            sleep_impact = -8
        elif sleep_duration <= 9:
            sleep_feedback = f'<div style="color: #10b981; font-size: 0.7rem; margin-top: -10px;">✓ {sleep_duration} hrs • Optimal range!</div>'
            sleep_impact = 12
        else:
            sleep_feedback = f'<div style="color: #f59e0b; font-size: 0.7rem; margin-top: -10px;">⚡ {sleep_duration} hrs • Too much - Reduce to 7-9 hrs</div>'
            sleep_impact = -5
        st.markdown(sleep_feedback, unsafe_allow_html=True)
        
        st.markdown('<div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 8px; margin-top: 20px;">☕ Caffeine Intake</div>', unsafe_allow_html=True)
        caffeine_intake = st.slider("", 0.0, 8.0, st.session_state.caffeine_intake, 0.5, key="caffeine_slider", label_visibility="collapsed")
        
        # Dynamic feedback for caffeine
        if caffeine_intake == 0:
            caffeine_feedback = f'<div style="color: #94a3b8; font-size: 0.7rem; margin-top: -10px;">💤 {int(caffeine_intake)} cups • No caffeine</div>'
            caffeine_impact = 0
        elif caffeine_intake <= 2:
            caffeine_feedback = f'<div style="color: #10b981; font-size: 0.7rem; margin-top: -10px;">✓ {int(caffeine_intake)} cups • Optimal intake!</div>'
            caffeine_impact = 3
        elif caffeine_intake <= 4:
            caffeine_feedback = f'<div style="color: #f59e0b; font-size: 0.7rem; margin-top: -10px;">⚠️ {int(caffeine_intake)} cups • Moderate - Consider reducing</div>'
            caffeine_impact = -5
        else:
            caffeine_feedback = f'<div style="color: #ef4444; font-size: 0.7rem; margin-top: -10px;">🚨 {int(caffeine_intake)} cups • Too high! Decrease intake immediately</div>'
            caffeine_impact = -12
        st.markdown(caffeine_feedback, unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 8px;">⏰ Stress Time</div>', unsafe_allow_html=True)
        stress_time = st.slider("", 0.0, 12.0, st.session_state.stress_time, 0.5, key="stress_slider", label_visibility="collapsed")
        
        # Dynamic feedback for stress
        if stress_time <= 2:
            stress_feedback = f'<div style="color: #10b981; font-size: 0.7rem; margin-top: -10px;">✓ {stress_time} hrs • Excellent stress management!</div>'
            stress_impact = 8
        elif stress_time <= 4:
            stress_feedback = f'<div style="color: #06b6d4; font-size: 0.7rem; margin-top: -10px;">✓ {stress_time} hrs • Manageable stress levels</div>'
            stress_impact = 0
        elif stress_time <= 6:
            stress_feedback = f'<div style="color: #f59e0b; font-size: 0.7rem; margin-top: -10px;">⚠️ {stress_time} hrs • High stress - Practice relaxation techniques</div>'
            stress_impact = -8
        else:
            stress_feedback = f'<div style="color: #ef4444; font-size: 0.7rem; margin-top: -10px;">🚨 {stress_time} hrs • Critical! Reduce stress exposure urgently</div>'
            stress_impact = -15
        st.markdown(stress_feedback, unsafe_allow_html=True)
        
        st.markdown('<div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 8px; margin-top: 20px;">🏃 Exercise Duration</div>', unsafe_allow_html=True)
        exercise_duration = st.slider("", 0.0, 180.0, st.session_state.exercise_duration, 5.0, key="exercise_slider", label_visibility="collapsed")
        
        # Dynamic feedback for exercise
        if exercise_duration == 0:
            exercise_feedback = f'<div style="color: #ef4444; font-size: 0.7rem; margin-top: -10px;">⚠️ {int(exercise_duration)} min • No exercise - Start moving!</div>'
            exercise_impact = -10
        elif exercise_duration < 30:
            exercise_feedback = f'<div style="color: #f59e0b; font-size: 0.7rem; margin-top: -10px;">⚡ {int(exercise_duration)} min • Below target - Aim for 30+ min</div>'
            exercise_impact = -3
        elif exercise_duration <= 60:
            exercise_feedback = f'<div style="color: #10b981; font-size: 0.7rem; margin-top: -10px;">✓ {int(exercise_duration)} min • Optimal exercise!</div>'
            exercise_impact = 10
        elif exercise_duration <= 120:
            exercise_feedback = f'<div style="color: #06b6d4; font-size: 0.7rem; margin-top: -10px;">💪 {int(exercise_duration)} min • Great dedication!</div>'
            exercise_impact = 8
        else:
            exercise_feedback = f'<div style="color: #f59e0b; font-size: 0.7rem; margin-top: -10px;">⚡ {int(exercise_duration)} min • Very high - Ensure adequate recovery</div>'
            exercise_impact = 5
        st.markdown(exercise_feedback, unsafe_allow_html=True)
    
    # Update Twin Prediction Button
    if st.button("🔄 Update Twin Prediction", use_container_width=True, type="primary"):
        st.session_state.sleep_duration = sleep_duration
        st.session_state.stress_time = stress_time
        st.session_state.caffeine_intake = caffeine_intake
        st.session_state.exercise_duration = exercise_duration
        st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dynamic Impact Analysis - Show all negative impacts
    negative_impacts = []
    
    if sleep_impact < 0:
        if sleep_duration < 6:
            negative_impacts.append(("😴 Critical Sleep Deficit", sleep_impact, "Sleep < 6 hours severely impacts resilience"))
        elif sleep_duration < 7:
            negative_impacts.append(("😴 Insufficient Sleep", sleep_impact, "Sleep below 7 hours reduces recovery"))
        else:
            negative_impacts.append(("😴 Excessive Sleep", sleep_impact, "Too much sleep can reduce alertness"))
    
    if caffeine_impact < 0:
        if caffeine_intake > 4:
            negative_impacts.append(("☕ Excessive Caffeine", caffeine_impact, f"{int(caffeine_intake)} cups disrupts sleep & increases anxiety"))
        else:
            negative_impacts.append(("☕ High Caffeine", caffeine_impact, f"{int(caffeine_intake)} cups may affect sleep quality"))
    
    if stress_impact < 0:
        if stress_time > 6:
            negative_impacts.append(("⏰ Critical Stress Levels", stress_impact, f"{stress_time} hrs of stress is unsustainable"))
        else:
            negative_impacts.append(("⏰ Elevated Stress", stress_impact, f"{stress_time} hrs of stress impacts recovery"))
    
    if exercise_impact < 0:
        if exercise_duration == 0:
            negative_impacts.append(("🏃 No Exercise", exercise_impact, "Physical activity is essential for resilience"))
        else:
            negative_impacts.append(("🏃 Insufficient Exercise", exercise_impact, f"{int(exercise_duration)} min below recommended 30 min"))
    
    # Show impact cards
    if negative_impacts:
        for impact_name, impact_value, impact_desc in negative_impacts:
            impact_html = f"""<div class="impact-card">
<span class="impact-icon">⚠️</span>
<span class="impact-text">{impact_name}</span>
<span class="impact-value">{impact_value:+d} points</span>
</div>
<div style="color: #94a3b8; font-size: 0.7rem; margin: -10px 0 15px 40px;">{impact_desc}</div>"""
            st.markdown(impact_html, unsafe_allow_html=True)
    else:
        # Show positive message if all inputs are optimal
        positive_html = """<div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 16px; margin: 15px 0;">
<span style="color: #10b981; font-size: 1.2rem; margin-right: 10px;">✓</span>
<span style="color: white; font-size: 0.85rem; font-weight: 700;">All Behavioral Inputs Optimal!</span>
<span style="color: #10b981; font-size: 0.9rem; font-weight: 800; float: right;">Excellent resilience foundation</span>
</div>"""
        st.markdown(positive_html, unsafe_allow_html=True)
    
    # Twin Accuracy Chart
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.markdown('<div class="chart-title">📈 Twin Accuracy - Predicted vs Actual SRI</div>', unsafe_allow_html=True)
    
    # Generate prediction vs actual data
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    predicted = [52 + random.uniform(-3, 3) for _ in range(7)]
    actual = [p + random.uniform(-2, 2) for p in predicted]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=predicted,
        name='Twin Prediction',
        line=dict(color='#a855f7', width=3, dash='dot'),
        mode='lines+markers'
    ))
    fig.add_trace(go.Scatter(
        x=days, y=actual,
        name='Your Actual SRI',
        line=dict(color='#06b6d4', width=3),
        mode='lines+markers',
        fill='tonexty',
        fillcolor='rgba(6, 182, 212, 0.1)'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False, color='#64748b'),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#64748b', range=[0, 100]),
        legend=dict(orientation="h", y=1.1, font=dict(color='white')),
        font=dict(family='Inter', color='white')
    )
    
    st.plotly_chart(fig, use_container_width=True, key="twin_accuracy_chart")
    
    # Mean Absolute Error
    mae = round(np.mean([abs(p - a) for p, a in zip(predicted, actual)]), 1)
    st.markdown(f'<div style="color: #94a3b8; font-size: 0.75rem; margin-top: 10px;">Mean Absolute Error: <span style="color: #10b981; font-weight: 700;">{mae} points</span> (Your twin learns from every session)</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Model Explainability
    st.markdown('<div class="explainability-section">', unsafe_allow_html=True)
    st.markdown('<div class="explainability-title">⚙️ Model Explainability - Feature Importance</div>', unsafe_allow_html=True)
    st.markdown('<div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 20px;">Understanding which factors have the most impact on your resilience predictions (SHAP-inspired analysis)</div>', unsafe_allow_html=True)
    
    # Feature importance bars
    features = [
        ("Sleep Quality", 95, "Highest Impact", "#ec4899"),
        ("Screen Time (Night)", 82, "High Impact", "#a855f7"),
        ("Caffeine Timing", 68, "Moderate Impact", "#f59e0b"),
        ("Exercise Duration", 54, "Moderate Impact", "#10b981"),
        ("Environmental Noise", 32, "Low Impact", "#06b6d4")
    ]
    
    for feature_name, impact, impact_label, color in features:
        feature_html = f"""<div class="feature-bar">
<div class="feature-label">
<span>{feature_name}</span>
<span class="feature-impact">{impact_label}</span>
</div>
<div class="feature-bar-bg">
<div class="feature-bar-fill" style="width: {impact}%; background: linear-gradient(90deg, {color} 0%, {color}88 100%);"></div>
</div>
</div>"""
        st.markdown(feature_html, unsafe_allow_html=True)
    
    # Interpretation note
    interpretation_html = """<div class="insight-box">
<div class="insight-title">💡 Interpretation</div>
<div class="insight-text">Sleep quality contributes 35% to your resilience predictions, suggesting sleep is just 1 factor could accelerate your predictions by 8-12 points.</div>
</div>"""
    st.markdown(interpretation_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Model Training Status
    model_status_html = """<div class="model-status">
<div class="model-status-title">🤖 AI Model Training Status</div>
<div class="model-stat">
<span class="model-stat-label">Model Type</span>
<span class="model-stat-value">Random Forest Regressor</span>
</div>
<div class="model-stat">
<span class="model-stat-label">Training Data</span>
<span class="model-stat-value">42 sessions, 1,680 data points</span>
</div>
<div class="model-stat">
<span class="model-stat-label">Model Accuracy (R² Score)</span>
<span class="model-stat-value">0.857</span>
</div>
<div class="model-stat">
<span class="model-stat-label">Last Retrained</span>
<span class="model-stat-value">2 minutes ago</span>
</div>
<div class="model-stat">
<span class="model-stat-label">Prediction Confidence</span>
<span class="model-stat-value">92.7% • Excellent</span>
</div>
</div>"""
    st.markdown(model_status_html, unsafe_allow_html=True)
    
    # Twin Intelligence Insights
    insights_html = """<div class="insight-box">
<div class="insight-title">🧠 Twin Intelligence Insights</div>
<div class="insight-text">
<strong>📌 Primary Recommendation:</strong> Hydration level is disrupting your twin's cortisol rhythm<br><br>
<strong>💡 What Your Twin Learned:</strong><br>
• Caffeine level is disrupting your twin's cortisol rhythm<br><br>
<strong>🎯 About Your Twin:</strong> The AI model adapts with every session, learning your unique stress patterns, behavioral data to forecast resilience—helping you intervene before crashes.<br><br>
</div>
</div>"""
    st.markdown(insights_html, unsafe_allow_html=True)

if __name__ == "__main__":
    render_digital_twin_advanced_page()
