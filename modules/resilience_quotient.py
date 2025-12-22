"""
Resilience Quotient (RQ) Dashboard Interface
Visualizes the multi-factor scoring system.
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from .rq_calculator import RQCalculator

def render_resilience_quotient_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #f59e0b; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">🏆</span> Resilience Quotient™
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Your physiological credit score. Measuring the adaptive capacity of your nervous system.
        </p>
    </div>
    """, unsafe_allow_html=True)

    calc = RQCalculator()
    
    # Mock some historical data for the demo
    if 'rq_history' not in st.session_state:
        st.session_state.rq_history = [
            {'hrv': 62, 'recovery_time': 320},
            {'hrv': 65, 'recovery_time': 300},
            {'hrv': 68, 'recovery_time': 280}
        ]
        
    stats = calc.calculate_score(st.session_state.rq_history)
    tier = calc.get_tier(stats['overall'])

    # --- MAIN SCORE GAUGE ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = stats['overall'],
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "RQ SCORE", 'font': {'size': 24, 'color': "white"}},
            gauge = {
                'axis': {'range': [0, 100], 'tickcolor': "white"},
                'bar': {'color': "#f59e0b"},
                'bgcolor': "rgba(0,0,0,0)",
                'steps': [
                    {'range': [0, 50], 'color': "rgba(239, 68, 68, 0.2)"},
                    {'range': [50, 75], 'color': "rgba(245, 158, 11, 0.2)"},
                    {'range': [75, 100], 'color': "rgba(16, 185, 129, 0.2)"}
                ],
                'threshold': {
                    'line': {'color': "white", 'width': 4},
                    'thickness': 0.75,
                    'value': stats['overall']
                }
            }
        ))
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', font=dict(color="white"), height=350)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown(f"""
        <div style="background: rgba(245, 158, 11, 0.1); border: 1px solid #f59e0b; padding: 30px; border-radius: 15px; margin-top: 50px;">
            <div style="color: #f59e0b; font-weight: 700; text-transform: uppercase; letter-spacing: 2px; font-size: 0.9rem;">Current Standing</div>
            <div style="color: white; font-size: 1.8rem; font-weight: 800; margin-top: 10px;">{tier}</div>
            <p style="color: #94a3b8; font-size: 0.9rem; margin-top: 15px;">
                Your RQ is in the top 15% of your age demographic. This indicates strong vagal tone and rapid sympathetic-parasympathetic switching.
            </p>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- COMPONENT BREAKDOWN ---
    st.markdown("### 🧬 Component Analysis")
    cb1, cb2, cb3 = st.columns(3)
    
    def component_card(title, value, color, desc):
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); padding: 20px; border-radius: 10px; border-top: 4px solid {color}; height: 180px;">
            <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase;">{title}</div>
            <div style="color: white; font-size: 2.2rem; font-weight: 700; margin: 5px 0;">{value}</div>
            <div style="color: #cbd5e1; font-size: 0.75rem;">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    with cb1:
        component_card("Resistance", stats['resistance'], "#3b82f6", "Ability to remain stable under acute stress.")
    with cb2:
        component_card("Recovery", stats['recovery'], "#10b981", "Velocity of return to parasympathetic baseline.")
    with cb3:
        component_card("Stability", stats['stability'], "#a78bfa", "Consistency of neural regulation over time.")

    st.divider()

    # --- TIME SERIES ---
    st.markdown("### 📈 RQ Progression")
    # Generating mock trend
    dates = pd.date_range(end=pd.Timestamp.now(), periods=10).strftime("%b %d")
    trend_vals = [65, 66, 64, 68, 70, 69, 72, 75, 74, stats['overall']]
    
    fig_line = go.Figure()
    fig_line.add_trace(go.Scatter(x=dates, y=trend_vals, mode='lines+markers', line=dict(color="#f59e0b", width=4), fill='tozeroy'))
    fig_line.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(showgrid=False),
        yaxis=dict(gridcolor="rgba(255,255,255,0.1)"),
        font=dict(color="white"),
        height=300,
        margin=dict(l=0, r=0, t=10, b=0)
    )
    st.plotly_chart(fig_line, use_container_width=True)
