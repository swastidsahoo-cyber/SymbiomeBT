"""
Resilience Forecast Interface.
A 48-hour physiological weather report.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

def render_resilience_forecast_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #60a5fa; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">🌤️</span> Resilience Forecast
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            A 48-hour outlook of your physiological weather. Plan your high-stress activities when readiness is peak.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- 48-HOUR LOOKAHEAD ---
    st.markdown("### 📅 48-Hour Outlook")
    
    # Generate mock forecast data
    hours = pd.date_range(start=datetime.now(), periods=48, freq='H')
    # Use Sine waves to simulate circadian rhythm + daily variability
    base_readiness = 70 + 15 * np.sin(np.arange(48) * 2 * np.pi / 24) + np.random.normal(0, 3, 48)
    base_readiness = np.clip(base_readiness, 0, 100)
    
    fig = go.Figure()
    
    # Gradient/Zone backgrounds
    fig.add_hrect(y0=0, y1=40, fillcolor="rgba(239, 68, 68, 0.1)", line_width=0, layer="below")
    fig.add_hrect(y0=40, y1=70, fillcolor="rgba(245, 158, 11, 0.1)", line_width=0, layer="below")
    fig.add_hrect(y0=70, y1=100, fillcolor="rgba(16, 185, 129, 0.1)", line_width=0, layer="below")
    
    fig.add_trace(go.Scatter(
        x=hours, 
        y=base_readiness, 
        mode='lines+markers', 
        name="Readiness",
        line=dict(color="#60a5fa", width=3, shape='spline'),
        marker=dict(
            size=8,
            color=base_readiness,
            colorscale='RdYlGn',
            showscale=False
        )
    ))

    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        yaxis=dict(title="Readiness (%)", range=[0, 105], gridcolor="rgba(255,255,255,0.05)"),
        xaxis=dict(gridcolor="rgba(255,255,255,0.05)"),
        height=400,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- FORECAST BLOCKS ---
    st.markdown("### 🕒 Optimal Activity Windows")
    
    c1, c2, c3 = st.columns(3)
    
    def forecast_block(time, activity, icon, readiness):
        color = "#10b981" if readiness > 75 else "#f59e0b" if readiness > 50 else "#ef4444"
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 12px; border-bottom: 4px solid {color};">
            <div style="font-size: 0.8rem; color: #94a3b8; font-weight: 700;">{time}</div>
            <div style="font-size: 1.2rem; color: white; margin: 10px 0;">{icon} {activity}</div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span style="color: {color}; font-weight: 800;">{readiness}%</span>
                <span style="font-size: 0.7rem; color: #94a3b8;">Peak Preparedness</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c1:
        forecast_block("Today 09:00", "Critical Meetings", "📊", 88)
    with c2:
        forecast_block("Today 15:30", "Deep Work", "🧠", 42)
    with c3:
        forecast_block("Tmrw 07:00", "Physical Training", "🏋️", 92)

    st.divider()

    # --- LOGIC EXPLANATION ---
    st.markdown("### 📘 The Science of the Forecast")
    st.info("""
    The Resilience Forecast integrates your historical sleep architecture, autonomic balance (HRV-SDNN), and circadian phase 
    shifts. By modeling your **Biological Recovery Rate**, we predict windows of vulnerability where sympathetic drive may 
    outpace parasympathetic recovery.
    """)
