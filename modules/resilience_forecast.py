"""
Resilience Weather Forecast (v1.5)
PIXEL-PERFECT 1:1 UI Realization.
Matches competition mockups exactly in card structure, colors, and layout.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
import textwrap
from datetime import datetime, timedelta


def render_resilience_forecast_page():
    st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
}

.main-title-container {
    text-align: center;
    padding: 30px 0 20px 0;
}
.main-title {
    color: #0ea5e9;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 8px;
}
.main-subtitle {
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 500;
}

/* Today's Forecast Card */
.today-card {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 32px;
    margin: 20px 0;
    position: relative;
    overflow: hidden;
}
.today-tag {
    background: #111827;
    color: #94a3b8;
    font-size: 0.6rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 4px;
    text-transform: uppercase;
    display: inline-block;
    margin-bottom: 12px;
}
.today-headline {
    color: white;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 5px;
}
.today-date {
    color: #94a3b8;
    font-size: 0.9rem;
    margin-bottom: 30px;
}

.today-metrics {
    display: flex;
    justify-content: flex-start;
    gap: 120px;
}
.metric-box {
    display: flex;
    flex-direction: column;
}
.metric-label {
    color: #94a3b8;
    font-size: 0.75rem;
    font-weight: 700;
    margin-bottom: 8px;
}
.metric-value-large {
    color: #0ea5e9;
    font-size: 2.4rem;
    font-weight: 900;
    line-height: 1;
}
.metric-value-conf {
    color: white;
    font-size: 2.2rem;
    font-weight: 800;
    line-height: 1;
}
.metric-value-risk {
    color: #f59e0b;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
}
.metric-sub {
    font-size: 0.75rem;
    font-weight: 700;
    margin-top: 8px;
}
.today-icon {
    position: absolute;
    top: 30px;
    right: 40px;
    font-size: 5rem;
}

/* 7-Day Outlook Chart */
.chart-panel {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 24px;
    margin: 25px 0;
}
.panel-title {
    color: white;
    font-size: 1.1rem;
    font-weight: 800;
    margin-bottom: 20px;
}

/* Grid Layout */
.forecast-grid-15 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-bottom: 40px;
}
.day-card-15 {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 24px;
    position: relative;
}
.day-card-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 15px;
}
.day-name {
    color: white;
    font-size: 1rem;
    font-weight: 800;
    line-height: 1.2;
}
.day-date-small {
    color: #94a3b8;
    font-size: 0.7rem;
    font-weight: 600;
}
.day-icon-small {
    font-size: 1.8rem;
}
.day-stat-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-top: 20px;
}
.day-stat-lbl {
    color: #94a3b8;
    font-size: 0.7rem;
    font-weight: 600;
}
.day-stat-val {
    color: #0ea5e9;
    font-weight: 900;
    font-size: 0.9rem;
}
.day-progress-bg {
    width: 100%;
    height: 4px;
    background: rgba(255, 255, 255, 0.05);
    border-radius: 2px;
    margin-top: 8px;
    margin-bottom: 12px;
}
.day-progress-fill {
    height: 100%;
    background: white;
    border-radius: 2px;
}
.day-tip-text {
    color: #94a3b8;
    font-size: 0.7rem;
    font-weight: 500;
}

/* Factors & Actions */
.factors-panel {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 30px;
    margin: 40px 0;
}
.factor-row {
    background: rgba(15, 23, 42, 0.4);
    border-radius: 10px;
    padding: 16px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.factor-tag-v15 {
    font-size: 0.65rem;
    font-weight: 900;
    padding: 4px 10px;
    border-radius: 4px;
    text-transform: uppercase;
}

.preventive-panel {
    background: rgba(16, 185, 129, 0.05);
    border: 1px solid rgba(16, 185, 129, 0.2);
    border-radius: 16px;
    padding: 30px;
    margin: 40px 0;
}
.action-card-v15 {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.action-priority {
    color: #94a3b8;
    font-size: 0.7rem;
    font-weight: 700;
}

/* Footer (PIXEL PERFECT v1.5) */
.hifi-footer {
    border-top: 1px solid rgba(51, 65, 85, 0.3);
    padding: 60px 0 30px 0;
    margin-top: 80px;
    display: grid;
    grid-template-columns: 1.5fr 1fr 1fr 1fr;
    gap: 40px;
}
.footer-col-title {
    color: white;
    font-weight: 800;
    font-size: 0.9rem;
    margin-bottom: 20px;
}
.footer-text {
    color: #94a3b8;
    font-size: 0.8rem;
    line-height: 1.8;
}
.award-banner {
    text-align: center;
    border-top: 1px solid rgba(51, 65, 85, 0.3);
    margin-top: 40px;
    padding-top: 40px;
}
</style>
""", unsafe_allow_html=True)

    # --- TOP TITLE ---
    st.markdown("""
<div class="main-title-container">
    <div class="main-title">Resilience Weather Forecast</div>
    <div class="main-subtitle">Your personalized 7-day resilience prediction based on behavioral patterns and historical data</div>
</div>
    """, unsafe_allow_html=True)

    # --- TODAY'S FORECAST CARD ---
    # Using a flat string to guarantee rendering
    today_card_html = """
<div class="today-card">
    <div class="today-tag">Today's Forecast</div>
    <div class="today-headline">Good Resilience</div>
    <div class="today-date">Monday, December 22</div>
    
    <div class="today-metrics">
        <div class="metric-box">
            <div class="metric-label">Predicted SRI</div>
            <div class="metric-value-large">61</div>
            <div class="metric-sub" style="color: #10b981;">↗ Improving</div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Confidence</div>
            <div class="metric-value-conf">85%</div>
            <div style="width: 250px; height: 4px; background: rgba(255,255,255,0.1); border-radius: 2px; margin-top: 15px;">
                <div style="width: 85%; height: 100%; background: white; border-radius: 2px;"></div>
            </div>
        </div>
        <div class="metric-box">
            <div class="metric-label">Risk Level</div>
            <div class="metric-value-risk">Moderate</div>
            <div class="metric-sub" style="color: #94a3b8;">⚠️ Minor stressors possible</div>
        </div>
    </div>
    
    <div class="today-icon" style="filter: drop-shadow(0 0 20px rgba(245, 158, 11, 0.3));">☀️</div>
</div>
"""
    st.markdown(today_card_html, unsafe_allow_html=True)

    # --- 7-DAY OUTLOOK CHART PANEL ---
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">7-Day Resilience Outlook</div>', unsafe_allow_html=True)
    
    # Precise chart to match Mockup
    days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
    vals = [61, 55, 62, 59, 58, 51, 51]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=days, y=vals, 
        mode='lines',
        line=dict(color='#0ea5e9', width=3),
        fill='tozeroy',
        fillcolor='rgba(14, 165, 233, 0.1)'
    ))
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=320,
        margin=dict(l=0, r=0, t=10, b=0),
        xaxis=dict(showgrid=False, tickfont=dict(color="#64748b", size=11), fixedrange=True),
        yaxis=dict(showgrid=True, gridcolor='#1e293b', range=[0, 100], tickfont=dict(color="#64748b", size=11), fixedrange=True),
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})
    st.markdown('</div>', unsafe_allow_html=True)

    # --- 7-DAY GRID ---
    # We use a single markdown block for the entire grid to ensure tight spacing like in the screenshot
    grid_html = '<div class="forecast-grid-15">'
    daily_data = [
        ("Mon", "Dec 22", 61, "☀️", "Start day with 5-min mindful breathing"),
        ("Tue", "Dec 23", 55, "☁️", "Prioritize 15-min sunlight exposure"),
        ("Wed", "Dec 24", 62, "☀️", "Schedule recovery breaks every 2 hours"),
        ("Thu", "Dec 25", 59, "☁️", "Optimize sleep environment tonight"),
        ("Fri", "Dec 26", 58, "☁️", "Consider gentle movement session"),
        ("Sat", "Dec 27", 51, "☁️", "Hydration focus - 2L minimum"),
        ("Sun", "Dec 28", 51, "☁️", "Start day with 5-min mindful breathing")
    ]
    
    for day, date, val, icon, tip in daily_data:
        grid_html += f"""
<div class="day-card-15">
    <div class="day-card-header">
        <div>
            <div class="day-name">{day}</div>
            <div class="day-date-small">{date}</div>
        </div>
        <div class="day-icon-small">{icon}</div>
    </div>
    <div class="day-stat-row">
        <span class="day-stat-lbl">Predicted SRI</span>
        <span class="day-stat-val">{val}</span>
    </div>
    <div class="day-progress-bg">
        <div class="day-progress-fill" style="width: {val}%;"></div>
    </div>
    <div class="day-tip-text">{tip}</div>
</div>
        """
    grid_html += '</div>'
    st.markdown(grid_html, unsafe_allow_html=True)

    # --- FACTORS & ACTIONS ---
    factors_html = """
<div class="factors-panel">
    <div class="panel-title">Forecast Factors</div>
    <div class="factor-row">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 1.2rem;">🗓️</div>
            <div>
                <div style="color: #10b981; font-weight: 800; font-size: 0.85rem;">Weekly Pattern</div>
                <div class="main-subtitle" style="margin-top: 2px;">Your resilience typically peaks mid-week (Wed-Thu) based on historical data</div>
            </div>
        </div>
        <div class="factor-tag-v15" style="color: #10b981; background: rgba(16, 185, 129, 0.1);">positive</div>
    </div>
    <div class="factor-row">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 1.2rem;">😴</div>
            <div>
                <div style="color: #ef4444; font-weight: 800; font-size: 0.85rem;">Sleep Debt</div>
                <div class="main-subtitle" style="margin-top: 2px;">Cumulative sleep deficit may reduce weekend resilience by 8-12%</div>
            </div>
        </div>
        <div class="factor-tag-v15" style="color: #ef4444; background: rgba(239, 68, 68, 0.1);">negative</div>
    </div>
    <div class="factor-row">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 1.2rem;">☀️</div>
            <div>
                <div style="color: #94a3b8; font-weight: 800; font-size: 0.85rem;">Environmental Trends</div>
                <div class="main-subtitle" style="margin-top: 2px;">Seasonal light exposure patterns suggest stable baseline maintenance</div>
            </div>
        </div>
        <div class="factor-tag-v15" style="color: #94a3b8; background: rgba(148, 163, 184, 0.1);">neutral</div>
    </div>
    <div class="factor-row" style="margin-bottom: 0;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="font-size: 1.2rem;">🏃</div>
            <div>
                <div style="color: #10b981; font-weight: 800; font-size: 0.85rem;">Activity Consistency</div>
                <div class="main-subtitle" style="margin-top: 2px;">Regular movement patterns predict sustained adaptive capacity</div>
            </div>
        </div>
        <div class="factor-tag-v15" style="color: #10b981; background: rgba(16, 185, 129, 0.1);">positive</div>
    </div>
</div>

<div class="preventive-panel">
    <div class="panel-title" style="margin-bottom: 25px;">Preventive Actions</div>
    <div class="action-card-v15">
        <div style="display: flex; gap: 15px; align-items: flex-start;">
            <div style="font-size: 1.2rem; color: #94a3b8;">🕒</div>
            <div>
                <div style="color: white; font-weight: 800; font-size: 0.9rem;">Schedule a 15-minute breathing session</div>
                <div class="footer-text" style="margin-top: 4px;">Predicted moderate stress - preventive regulation recommended</div>
                <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 700; margin-top: 6px;">📋 Best time: Morning (8-10 AM)</div>
            </div>
        </div>
        <div class="action-priority">high priority</div>
    </div>
    <div class="action-card-v15">
        <div style="display: flex; gap: 15px; align-items: flex-start;">
            <div style="font-size: 1.2rem; color: #94a3b8;">☀️</div>
            <div>
                <div style="color: white; font-weight: 800; font-size: 0.9rem;">Increase natural light exposure</div>
                <div class="footer-text" style="margin-top: 4px;">Low ambient light correlates with 10% SRI reduction</div>
                <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 700; margin-top: 6px;">📋 Best time: Within 1 hour of waking</div>
            </div>
        </div>
        <div class="action-priority">medium priority</div>
    </div>
    <div class="action-card-v15">
        <div style="display: flex; gap: 15px; align-items: flex-start;">
            <div style="font-size: 1.2rem; color: #94a3b8;">📱</div>
            <div>
                <div style="color: white; font-weight: 800; font-size: 0.9rem;">Evening screen-free window</div>
                <div class="footer-text" style="margin-top: 4px;">Optimize tomorrow's baseline with circadian support</div>
                <div style="color: #94a3b8; font-size: 0.7rem; font-weight: 700; margin-top: 6px;">📋 Best time: 2 hours before bed</div>
            </div>
        </div>
        <div class="action-priority">low priority</div>
    </div>
    
    <div style="background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 8px; padding: 12px; margin-top: 30px; font-size: 0.75rem; color: #38bdf8;">
        📊 <b>Forecast Methodology:</b> Predictions use time-series analysis of your last 14 days, combined with behavioral inputs (sleep, activity, environment). The model learns your personal resilience rhythms and extrapolates forward with confidence intervals. Accuracy improves with more data.
    </div>
</div>
"""
    st.markdown(factors_html, unsafe_allow_html=True)

    # --- PIXEL PERFECT FOOTER (v1.5) ---
    st.markdown("""
<div class="hifi-footer">
    <div>
        <div style="color: #10b981; font-weight: 800; font-size: 0.9rem; margin-bottom: 12px;">🧬 About Symbiome</div>
        <div class="footer-text">
            An AI-enhanced, non-invasive biofeedback platform measuring how body and environment interact to shape stress and gut-related wellbeing.
        </div>
    </div>
    <div>
        <div class="footer-col-title">Core Features</div>
        <div class="footer-text">
            • HRV, GSR, Facial Calm tracking<br>
            • Digital Twin AI prediction<br>
            • Environmental correlation<br>
            • Gut-brain axis logging<br>
            • Gamified biofeedback
        </div>
    </div>
    <div>
        <div class="footer-col-title">Research Ethics</div>
        <div class="footer-text">
            All data is anonymized and stored securely. This platform is designed for research and educational purposes.
        </div>
        <div style="color: #10b981; font-weight: 800; font-size: 0.7rem; margin-top: 15px;">Privacy-first • Consent-driven • Transparent</div>
    </div>
    <div>
        <div class="footer-col-title">Future Vision</div>
        <div class="footer-text">
            • Symbiome Glove (BLE wearable)<br>
            • Cloud-based AI learning<br>
            • Global resilience mapping<br>
            • Clinical validation studies<br>
            • School & workplace pilots
        </div>
    </div>
</div>

<div class="award-banner">
    <div style="color: #f59e0b; font-weight: 800; font-size: 0.85rem;">🏆 Built for BTYSTE & Science Competition Excellence</div>
    <div class="footer-text" style="font-size: 0.7rem; margin-top: 5px;">Multi-modal biometrics • AI prediction • Environmental correlation • Gut-brain research • Community health mapping</div>
    <div class="footer-text" style="font-size: 0.7rem; margin-top: 15px; color: #475569;">Symbiome Research Platform © 2025 - Advancing the science of human resilience</div>
</div>
""", unsafe_allow_html=True)

if __name__ == "__main__":
    render_resilience_forecast_page()
