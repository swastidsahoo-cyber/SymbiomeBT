"""
Environmental Symbiome Feedback (v1.0)
High-fidelity interface for tracking environmental stressors and their impact on resilience.
Matches provided competition mockup exactly.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
import textwrap
import pandas as pd
from datetime import datetime

def clean_render(html_str):
    """Ensure HTML strings are perfectly dedented and clean for Streamlit."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def render_environmental_tracker_page():
    # --- CSS STYLES (HI-FI MATCH) ---
    clean_render("""
<style>
.env-header { text-align: center; margin-bottom: 40px; }
.env-title { color: #f59e0b; font-size: 2.2rem; font-weight: 800; margin-bottom: 5px; }
.env-sub { color: #94a3b8; font-size: 0.9rem; }

/* Stat Badges */
.env-stat-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }
.env-stat-card {
    background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px; padding: 18px; display: flex; flex-direction: column; gap: 8px; position: relative;
}
.env-stat-tag {
    position: absolute; top: 10px; right: 10px; font-size: 0.55rem;
    background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 2px 6px; border-radius: 4px; font-weight: 800;
}
.env-stat-val { color: white; font-weight: 800; font-size: 1.6rem; line-height: 1; }
.env-stat-lbl { color: #94a3b8; font-size: 0.7rem; font-weight: 600; }

/* Impact Model Panel */
.impact-panel {
    background: rgba(30, 41, 59, 0.3); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 20px; padding: 30px; margin-bottom: 30px;
}
.prediction-box {
    background: rgba(15, 23, 42, 0.6); border-radius: 12px; padding: 25px;
    display: flex; justify-content: space-between; align-items: center;
}

/* Tip Items */
.tip-item {
    background: rgba(15, 23, 42, 0.4); border-radius: 10px; padding: 16px; margin-bottom: 12px;
    display: flex; justify-content: space-between; align-items: center;
}
.impact-chip {
    background: rgba(16, 185, 129, 0.1); color: #10b981; border: 1px solid rgba(16, 185, 129, 0.3);
    font-size: 0.65rem; font-weight: 800; padding: 3px 8px; border-radius: 4px;
}
</style>
    """)

    # --- HEADER ---
    clean_render("""
<div class="env-header">
    <div class="env-title">Environmental Symbiome Feedback</div>
    <div class="env-sub">How your surrounding environment shapes your physiological resilience</div>
</div>
    """)

    # --- TOP BADGES ---
    st.markdown('<div class="env-stat-grid">', unsafe_allow_html=True)
    env_stats = [
        ("☀️", "65%", "Light Intensity", "Optimal"),
        ("🔊", "39 dB", "Ambient Noise", "Optimal"),
        ("🌡️", "21 °C", "Temperature", "Optimal"),
        ("💧", "69%", "Humidity", "Optimal")
    ]
    cols = st.columns(4)
    for i, (icon, val, lbl, tag) in enumerate(env_stats):
        with cols[i]:
            st.markdown(f"""
<div class="env-stat-card">
    <div class="env-stat-tag">{tag}</div>
    <div style="font-size: 1.2rem; margin-bottom: 5px;">{icon}</div>
    <div class="env-stat-val">{val}</div>
    <div class="env-stat-lbl">{lbl}</div>
</div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- LIVE IMPACT MODEL ---
    st.markdown('<div class="impact-panel">', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; gap: 10px; align-items: center; margin-bottom: 25px;"><span style="color: #a855f7;">⚡</span><span style="color: white; font-weight: 800; font-size: 0.9rem;">Live Environmental Impact Model</span></div>', unsafe_allow_html=True)
    
    col_s1, col_s2 = st.columns([2, 1])
    with col_s1:
        light_slider = st.slider("Light Exposure", 0, 100, 65)
        noise_slider = st.slider("Noise Level", 20, 100, 39)
        temp_slider = st.slider("Temperature", 10, 40, 21)
        
        # Calculate Mock Impact
        optimality = 100 - abs(light_slider - 65) - abs(noise_slider - 39) - abs(temp_slider - 21)
        optimality = max(0, min(100, optimality))
        impact_sri = (optimality - 50) / 2 # Simple formula for demo
        
    with col_s2:
        st.markdown(f"""
<div style="margin-top: 20px;">
    <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 10px;">Predicted SRI Impact</div>
    <div style="color: {'#10b981' if impact_sri >= 0 else '#ef4444'}; font-size: 2rem; font-weight: 950;">{'+' if impact_sri >= 0 else ''}{impact_sri:.1f}%</div>
    
    <div style="margin-top: 30px;">
        <div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 10px; display: flex; justify-content: space-between;">
            <span>Optimality Score</span>
            <span>{int(optimality)}/100</span>
        </div>
        <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px;">
            <div style="width: {optimality}%; height: 100%; background: white; border-radius: 3px;"></div>
        </div>
    </div>
</div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MINI CHARTS ---
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown('<div class="impact-panel" style="padding: 20px;">', unsafe_allow_html=True)
        st.markdown('<div style="color: white; font-weight: 800; font-size: 0.85rem; margin-bottom: 15px;">Light vs Resilience</div>', unsafe_allow_html=True)
        x_light = np.linspace(20, 100, 50)
        y_light = 50 + 30 * np.exp(-((x_light - 75)**2) / 400) # Bell curve
        fig_l = go.Figure()
        fig_l.add_trace(go.Scatter(x=x_light, y=y_light, fill='tozeroy', line_color='#f59e0b', fillcolor='rgba(245, 158, 11, 0.1)'))
        fig_l.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False, title="Light (%)"), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[40, 90]))
        st.plotly_chart(fig_l, use_container_width=True, key="light_curve")
        st.markdown('<div style="color: #94a3b8; font-size: 0.65rem; margin-top: 10px;">Moderate light (60-80%) correlates with optimal resilience</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_c2:
        st.markdown('<div class="impact-panel" style="padding: 20px;">', unsafe_allow_html=True)
        st.markdown('<div style="color: white; font-weight: 800; font-size: 0.85rem; margin-bottom: 15px;">Noise vs Resilience</div>', unsafe_allow_html=True)
        x_noise = np.linspace(20, 100, 50)
        y_noise = 80 - 0.5 * x_noise + np.random.normal(0, 1, 50) # Linear decay
        fig_n = go.Figure()
        fig_n.add_trace(go.Scatter(x=x_noise, y=y_noise, line_color='#3b82f6', mode='lines'))
        fig_n.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=200, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False, title="Noise (dB)"), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[40, 90]))
        st.plotly_chart(fig_n, use_container_width=True, key="noise_curve")
        st.markdown('<div style="color: #94a3b8; font-size: 0.65rem; margin-top: 10px;">Higher ambient noise (>70dB) reduces resilience by average 14%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 24-HOUR PATTERN ---
    st.markdown('<div class="impact-panel">', unsafe_allow_html=True)
    st.markdown('<div style="display: flex; gap: 10px; align-items: center; margin-bottom: 25px;"><span style="color: #2dd4bf;">🕒</span><span style="color: white; font-weight: 800; font-size: 0.9rem;">24-Hour Resilience & Light Pattern</span></div>', unsafe_allow_html=True)
    
    hours = [f"{i}:00" for i in range(24)]
    resilience_24 = [30, 28, 32, 40, 50, 65, 68, 70, 72, 70, 75, 78, 80, 78, 72, 70, 65, 60, 55, 50, 45, 40, 35, 30]
    light_24 = [10, 10, 10, 20, 40, 90, 85, 80, 88, 92, 90, 85, 80, 75, 85, 90, 85, 50, 20, 20, 15, 12, 10, 10]
    
    fig_24 = go.Figure()
    # Light pattern as area
    fig_24.add_trace(go.Scatter(x=hours, y=light_24, name="Light", fill='tozeroy', line=dict(color='#f59e0b', dash='dot'), fillcolor='rgba(245, 158, 11, 0.05)', yaxis='y2'))
    # Resilience as solid line
    fig_24.add_trace(go.Scatter(x=hours, y=resilience_24, name="SRI", line=dict(color='#2dd4bf', width=3)))
    
    fig_24.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300, 
        margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"),
        xaxis=dict(showgrid=False, tickvals=hours[::4]),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="SRI", range=[0, 110]),
        yaxis2=dict(overlaying='y', side='right', title="Light", range=[0, 110], showgrid=False),
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig_24, use_container_width=True, key="24h_env_pattern")
    
    # Day/Night Insight Badges
    b_col1, b_col2 = st.columns(2)
    with b_col1:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.4); border-radius: 10px; padding: 12px; display: flex; gap: 10px; border-left: 3px solid #f59e0b;">
    <div style="font-size: 1.2rem;">☀️</div>
    <div>
        <div style="color: white; font-weight: 800; font-size: 0.75rem;">Day Pattern</div>
        <div style="color: #94a3b8; font-size: 0.65rem;">Morning sunlight exposure improves HRV by 12% and accelerates recovery</div>
    </div>
</div>
        """, unsafe_allow_html=True)
    with b_col2:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.4); border-radius: 10px; padding: 12px; display: flex; gap: 10px; border-left: 3px solid #3b82f6;">
    <div style="font-size: 1.2rem;">🌙</div>
    <div>
        <div style="color: white; font-weight: 800; font-size: 0.75rem;">Night Pattern</div>
        <div style="color: #94a3b8; font-size: 0.65rem;">Low light after 10 PM supports natural cortisol reduction and sleep quality</div>
    </div>
</div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- OPTIMIZATION TIPS ---
    st.markdown('<div style="font-weight: 800; color: white; font-size: 1.1rem; margin-bottom: 25px;">Environmental Optimization Tips</div>', unsafe_allow_html=True)
    tips = [
        ("💡", "Optimize your workspace lighting", "Try 60-70% brightness with natural light exposure for peak resilience", "+8% SRI"),
        ("🔇", "Create quiet zones during peak stress", "Reduce ambient noise below 50dB during focused work or recovery sessions", "+12% recovery speed"),
        ("🌡️", "Maintain thermal comfort", "Keep temperature between 20-22°C for optimal autonomic balance", "+6% HRV"),
        ("🌅", "Morning light ritual", "15 minutes of bright light exposure within 1 hour of waking", "+18% morning resilience")
    ]
    
    for icon, title, desc, tag in tips:
        st.markdown(f"""
<div class="tip-item">
    <div style="display: flex; gap: 15px; align-items: flex-start;">
        <div style="font-size: 1.2rem;">{icon}</div>
        <div>
            <div style="color: white; font-weight: 800; font-size: 0.85rem;">{title}</div>
            <div style="color: #94a3b8; font-size: 0.75rem; margin-top: 4px;">{desc}</div>
        </div>
    </div>
    <div class="impact-chip">{tag}</div>
</div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_environmental_tracker_page()
