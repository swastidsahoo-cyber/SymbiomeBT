"""
Resilience Weather Forecast (v2.0)
High-fidelity interface for 7-day resilience forecasting.
Matches provided competition mockups exactly.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
import textwrap
from datetime import datetime, timedelta

def clean_render(html_str):
    """Ensure HTML strings are perfectly dedented and clean for Streamlit."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def render_resilience_forecast_page():
    # --- CSS STYLES ---
    clean_render("""
<style>
/* Main Title */
.forecast-title-container {
    text-align: center;
    padding: 20px 0 40px 0;
}
.forecast-title {
    color: #38bdf8;
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 5px;
}
.forecast-sub {
    color: #94a3b8;
    font-size: 0.9rem;
}

/* Summary Card */
.forecast-card-main {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px;
    padding: 30px;
    margin-bottom: 30px;
    position: relative;
}
.day-tag {
    background: rgba(30, 41, 59, 0.8);
    color: #94a3b8;
    font-size: 0.65rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 4px;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 10px;
}

/* Outlook Chart Panel */
.outlook-panel {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 30px;
}

/* Daily Grid */
.forecast-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 15px;
    margin-bottom: 30px;
}
.day-card {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
}
.day-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}

/* Factor Items */
.factor-container {
    background: rgba(30, 41, 59, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 30px;
}
.factor-item {
    background: rgba(15, 23, 42, 0.4);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.factor-tag {
    font-size: 0.65rem;
    font-weight: 800;
    padding: 3px 8px;
    border-radius: 4px;
    text-transform: uppercase;
}

/* Preventive Actions */
.preventive-container {
    background: rgba(6, 78, 59, 0.1);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 16px;
    padding: 24px;
    margin-bottom: 40px;
}
.action-card {
    background: rgba(15, 23, 42, 0.4);
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

/* Footer Section */
.footer-section {
    padding-top: 50px;
    border-top: 1px solid rgba(255,255,255,0.05);
    margin-top: 50px;
}
</style>
    """)

    # --- HEADER ---
    clean_render("""
<div class="forecast-title-container">
    <div class="forecast-title">Resilience Weather Forecast</div>
    <div class="forecast-sub">Your personalized 7-day resilience prediction based on behavioral patterns and historical data</div>
</div>
    """)

    # --- TODAY'S FORECAST CARD (SCREENSHOT 1) ---
    st.markdown('<div class="forecast-card-main">', unsafe_allow_html=True)
    c_main1, c_main2 = st.columns([2, 1])
    with c_main1:
        clean_render("""
<div class="day-tag">Today's Forecast</div>
<h2 style="color: white; font-weight: 800; margin-bottom: 5px;">Good Resilience</h2>
<div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 30px;">Monday, December 22</div>
        """)
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        with stat_col1:
            clean_render("""
<div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 5px;">Predicted SRI</div>
<div style="color: #38bdf8; font-size: 2.5rem; font-weight: 900;">61</div>
<div style="color: #10b981; font-size: 0.8rem; font-weight: 700; margin-top: 5px;">↗ Improving</div>
            """)
        with stat_col2:
            clean_render("""
<div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 15px;">Confidence</div>
<div style="color: #a855f7; font-size: 2.2rem; font-weight: 900;">85%</div>
<div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 15px;">
    <div style="width: 85%; height: 100%; background: white; border-radius: 2px;"></div>
</div>
            """)
        with stat_col3:
            clean_render("""
<div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 5px;">Risk Level</div>
<div style="color: #f59e0b; font-size: 2rem; font-weight: 900;">Moderate</div>
<div style="color: #94a3b8; font-size: 0.75rem; margin-top: 5px;">⚠️ Minor stressors possible</div>
            """)
            
    with c_main2:
        clean_render("""
<div style="text-align: right;">
    <div style="font-size: 5rem; color: #f59e0b; filter: drop-shadow(0 0 20px rgba(245, 158, 11, 0.4));">☀️</div>
</div>
        """)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 7-DAY OUTLOOK CHART ---
    st.markdown('<div class="outlook-panel">', unsafe_allow_html=True)
    st.markdown('<div style="font-weight: 800; color: white; font-size: 1.1rem; margin-bottom: 25px;">7-Day Resilience Outlook</div>', unsafe_allow_html=True)
    
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    sri_values = [61, 55, 62, 59, 58, 51, 51]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=sri_values, 
        mode='lines',
        line=dict(color='#06b6d4', width=3),
        fill='tozeroy',
        fillcolor='rgba(6, 182, 212, 0.1)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, tickfont=dict(color="#94a3b8")),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100], tickfont=dict(color="#94a3b8")),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 7-DAY GRID ---
    grid_cols = st.columns(2)
    daily_data = [
        ("Mon", "Dec 22", 61, "☀️", "Start day with 5-min mindful breathing"),
        ("Tue", "Dec 23", 55, "☁️", "Prioritize 15-min sunlight exposure"),
        ("Wed", "Dec 24", 62, "☀️", "Schedule recovery breaks every 2 hours"),
        ("Thu", "Dec 25", 59, "☁️", "Optimize sleep environment tonight"),
        ("Fri", "Dec 26", 58, "☁️", "Consider gentle movement session"),
        ("Sat", "Dec 27", 51, "☁️", "Hydration focus - 2L minimum"),
        ("Sun", "Dec 28", 51, "☁️", "Start day with 5-min mindful breathing")
    ]
    
    for i, (day, date, val, icon, tip) in enumerate(daily_data):
        with grid_cols[i % 2]:
            st.markdown(f"""
<div class="day-card">
    <div class="day-card-header">
        <div>
            <div style="font-weight: 800; color: white;">{day}</div>
            <div style="color: #94a3b8; font-size: 0.7rem;">{date}</div>
        </div>
        <div style="font-size: 1.5rem;">{icon}</div>
    </div>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
        <span style="color: #94a3b8; font-size: 0.75rem;">Predicted SRI</span>
        <span style="color: #38bdf8; font-weight: 800; font-size: 0.8rem;">{val}</span>
    </div>
    <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px; margin-bottom: 15px;">
        <div style="width: {val}%; height: 100%; background: white; border-radius: 2px;"></div>
    </div>
    <div style="color: #94a3b8; font-size: 0.75rem;">{tip}</div>
</div>
            """, unsafe_allow_html=True)
            st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- FORECAST FACTORS ---
    st.markdown('<div class="factor-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 25px;">Forecast Factors</h4>', unsafe_allow_html=True)
    
    factors = [
        ("Weekly Pattern", "Your resilience typically peaks mid-week (Wed-Thu) based on historical data", "positive", "#10b981", "🗓️"),
        ("Sleep Debt", "Cumulative sleep deficit may reduce weekend resilience by 8-12%", "negative", "#ef4444", "😴"),
        ("Environmental Trends", "Seasonal light exposure patterns suggest stable baseline maintenance", "neutral", "#94a3b8", "☀️"),
        ("Activity Consistency", "Regular movement patterns predict sustained adaptive capacity", "positive", "#10b981", "🏃")
    ]
    
    for name, desc, label, color, icon in factors:
        st.markdown(f"""
<div class="factor-item">
    <div style="display: flex; gap: 15px; align-items: flex-start;">
        <div style="font-size: 1.2rem;">{icon}</div>
        <div>
            <div style="color: {color}; font-weight: 800; font-size: 0.85rem;">{name}</div>
            <div style="color: #94a3b8; font-size: 0.75rem; margin-top: 4px;">{desc}</div>
        </div>
    </div>
    <div class="factor-tag" style="background: {color + '20'}; color: {color}; border: 1px solid {color + '40'};">{label}</div>
</div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- PREVENTIVE ACTIONS ---
    st.markdown('<div class="preventive-container">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 25px;">Preventive Actions</h4>', unsafe_allow_html=True)
    
    actions = [
        ("Schedule a 15-minute breathing session", "Predicted moderate stress - preventive regulation recommended", "High priority", "#ef4444", "🕒"),
        ("Increase natural light exposure", "Low ambient light correlates with 10% SRI reduction", "medium priority", "#f59e0b", "☀️"),
        ("Evening screen-free window", "Optimize tomorrow's baseline with circadian support", "low priority", "#3B82F6", "📱")
    ]
    
    for title, desc, priority, color, icon in actions:
        st.markdown(f"""
<div class="action-card">
    <div style="display: flex; gap: 15px; align-items: flex-start;">
        <div style="font-size: 1.2rem; color: #94a3b8;">{icon}</div>
        <div>
            <div style="color: white; font-weight: 800; font-size: 0.9rem;">{title}</div>
            <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 4px;">{desc}</div>
            <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 6px;">⏱️ Best time: Morning (8-10 AM)</div>
        </div>
    </div>
    <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 800; text-transform: lowercase;">{priority}</div>
</div>
        """, unsafe_allow_html=True)
        
    clean_render("""
<div style="background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 8px; padding: 12px; margin-top: 20px; font-size: 0.75rem; color: #67e8f9; line-height: 1.4;">
📊 <b>Forecast Methodology</b>: Predictions use time-series analysis of your last 14 days, combined with behavioral inputs (sleep, activity, environment). The model learns your personal resilience rhythms and extrapolates forward with confidence intervals. Accuracy improves with more data.
</div>
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- FOOTER SECTION ---
    st.markdown('<div class="footer-section">', unsafe_allow_html=True)
    f_col1, f_col2, f_col3, f_col4 = st.columns(4)
    with f_col1:
        st.markdown("""
<div style="color: #10b981; font-weight: 800; font-size: 0.9rem; margin-bottom: 15px;">🧬 About Symbiome</div>
<div style="color: #94a3b8; font-size: 0.75rem; line-height: 1.6;">
An AI-enhanced, non-invasive biofeedback platform measuring how body and environment interact to shape stress and gut-related wellbeing.
</div>
        """, unsafe_allow_html=True)
    with f_col2:
        st.markdown("""
<div style="color: white; font-weight: 800; font-size: 0.9rem; margin-bottom: 15px;">Core Features</div>
<div style="color: #94a3b8; font-size: 0.75rem; line-height: 2;">
• HRV, GSR, Facial Calm tracking<br>
• Digital Twin AI prediction<br>
• Environmental correlation<br>
• Gut-brain axis logging<br>
• Gamified biofeedback
</div>
        """, unsafe_allow_html=True)
    with f_col3:
        st.markdown("""
<div style="color: white; font-weight: 800; font-size: 0.9rem; margin-bottom: 15px;">Research Ethics</div>
<div style="color: #94a3b8; font-size: 0.75rem; line-height: 1.6;">
All data is anonymized and stored securely. This platform is designed for research and educational purposes.
</div>
<div style="color: #10b981; font-size: 0.7rem; font-weight: 700; margin-top: 10px;">Privacy-first • Consent-driven • Transparent</div>
        """, unsafe_allow_html=True)
    with f_col4:
        st.markdown("""
<div style="color: white; font-weight: 800; font-size: 0.9rem; margin-bottom: 15px;">Future Vision</div>
<div style="color: #94a3b8; font-size: 0.75rem; line-height: 2;">
• Symbiome Glove (BLE wearable)<br>
• Cloud-based AI learning<br>
• Global resilience mapping<br>
• Clinical validation studies<br>
• School & workplace pilots
</div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    st.markdown("""
<div style="text-align: center; border-top: 1px solid rgba(255,255,255,0.05); padding-top: 30px;">
    <div style="color: #f59e0b; font-weight: 800; font-size: 0.85rem;">🏆 Built for BTYSTE & Science Competition Excellence</div>
    <div style="color: #94a3b8; font-size: 0.7rem; margin-top: 5px;">Multi-modal biometrics • AI prediction • Environmental correlation • Gut-brain research • Community health mapping</div>
    <div style="color: #64748b; font-size: 0.7rem; margin-top: 15px;">Symbiome Research Platform © 2025 - Advancing the science of human resilience</div>
</div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_resilience_forecast_page()
