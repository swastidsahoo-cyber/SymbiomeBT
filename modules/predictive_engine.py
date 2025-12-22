"""
Predictive Intelligence Engine (v1.0)
High-fidelity interface for ensemble machine learning stress forecasting.
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

def render_predictive_engine_page():
    # --- SESSION STATE INITIALIZATION ---
    if 'scheduled_interventions' not in st.session_state:
        st.session_state.scheduled_interventions = []

    # --- CSS STYLES (HI-FI HI-CONTRAST) ---
    clean_render("""
<style>
/* Header Styling */
.engine-title-container {
    text-align: center;
    padding: 20px 0 40px 0;
}
.engine-icon {
    font-size: 2.2rem;
    color: #a855f7;
    margin-bottom: 10px;
}
.engine-title {
    background: linear-gradient(135deg, #f472b6 0%, #a855f7 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.6rem;
    font-weight: 900;
    margin-bottom: 5px;
}
.engine-sub {
    color: #94a3b8;
    font-size: 0.95rem;
    max-width: 600px;
    margin: 0 auto;
    line-height: 1.5;
}

/* Badge Dashboard */
.stat-badge-row {
    display: flex;
    justify-content: center;
    gap: 15px;
    margin-top: 25px;
}
.stat-badge {
    background: rgba(15, 23, 42, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 6px 16px;
    border-radius: 20px;
    font-size: 0.8rem;
    color: #e2e8f0;
    display: flex;
    align-items: center;
    gap: 8px;
}
.badge-dot {
    width: 6px; height: 6px; border-radius: 50%;
}

/* Alert System */
.alert-card {
    background: linear-gradient(135deg, rgba(127, 29, 29, 0.3), rgba(69, 10, 10, 0.3));
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 12px;
    padding: 20px 25px;
    margin: 40px 0;
    position: relative;
    overflow: hidden;
}
.alert-tag {
    position: absolute; top: 15px; right: 20px;
    background: rgba(239, 68, 68, 0.2);
    color: #f87171;
    font-size: 0.7rem;
    font-weight: 800;
    padding: 4px 10px;
    border-radius: 4px;
    letter-spacing: 1px;
}

/* Prediction Cards */
.prediction-panel {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 30px;
    height: 100%;
}
.risk-value {
    font-size: 3.5rem;
    font-weight: 900;
    color: #f87171;
    line-height: 1;
}

/* Intervention Points */
.intervention-item {
    background: rgba(15, 23, 42, 0.4);
    border-left: 4px solid #10b981;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 15px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: all 0.3s ease;
}
.intervention-item:hover {
    background: rgba(15, 23, 42, 0.6);
    transform: translateX(5px);
}
.impact-badge {
    background: rgba(16, 185, 129, 0.1);
    color: #10b981;
    font-size: 0.75rem;
    font-weight: 700;
    padding: 4px 8px;
    border-radius: 4px;
    margin-top: 8px;
    display: inline-block;
}

/* AI Coach Bubble */
.ai-coach-mini {
    position: fixed; bottom: 30px; right: 30px;
    width: 380px;
    background: #064e3b;
    border: 1px solid #059669;
    border-radius: 20px;
    padding: 24px;
    box-shadow: 0 20px 50px rgba(0,0,0,0.5);
    z-index: 9999;
}

/* Technical Stack View */
.tech-architecture {
    background: #020617;
    border: 1px solid rgba(6, 182, 212, 0.3);
    border-radius: 12px;
    padding: 25px;
    margin-top: 50px;
}
</style>
    """)

    # --- HEADER SECTION ---
    clean_render("""
<div class="engine-title-container">
    <div class="engine-icon">🧬</div>
    <div class="engine-title">Predictive Intelligence Engine</div>
    <div class="engine-sub">
        Ensemble Machine Learning (Random Forest + Neural Networks) predicting physiological stress events before conscious awareness
    </div>
    <div class="stat-badge-row">
        <div class="stat-badge"><span class="badge-dot" style="background: #a855f7;"></span> Live Model: v3.2.1</div>
        <div class="stat-badge"><span class="badge-dot" style="background: #10b981;"></span> Accuracy: 94.7%</div>
        <div class="stat-badge"><span class="badge-dot" style="background: #38bdf8;"></span> Last Update: 10:52:30 AM</div>
    </div>
</div>
    """)

    # --- ALERT SYSTEM (SCREENSHOT 1) ---
    clean_render("""
<div class="alert-card">
    <div class="alert-tag">URGENT</div>
    <div style="display: flex; gap: 15px; align-items: flex-start;">
        <span style="font-size: 1.4rem; color: #ef4444;">⚠️</span>
        <div>
            <div style="font-weight: 800; color: white; font-size: 1.05rem; margin-bottom: 5px;">Predictive Alert System</div>
            <div style="font-weight: 700; color: #fecaca; font-size: 0.95rem; margin-bottom: 8px;">
                ⚠️ Cumulative sleep debt exceeding resilience threshold
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; line-height: 1.4;">
                3 consecutive nights of sub-optimal recovery detected. Tomorrow's baseline SRI projected to drop 18%.
            </div>
        </div>
    </div>
</div>
    """)

    # --- FORECAST CONTROLS ---
    f_col1, f_col2, f_col3 = st.columns([1, 2, 1])
    with f_col2:
        forecast_window = st.radio(
            "Forecast Window Selection",
            ["24h Forecast", "48h Forecast", "72h Forecast"],
            index=1,
            horizontal=True,
            label_visibility="collapsed"
        )

    st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)

    # --- MAIN ENGINE GRID ---
    col_main, col_side = st.columns([2, 1])

    with col_main:
        with st.container():
            st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
            head_col1, head_col2 = st.columns([2,1])
            with head_col1:
                st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 30px;">Burnout Probability Heatmap</h4>', unsafe_allow_html=True)
            with head_col2:
                 st.markdown(f'<div style="text-align: right;"><span style="background: rgba(239, 68, 68, 0.2); color: #f87171; font-size: 0.65rem; padding: 3px 8px; border-radius: 4px; font-weight: 800;">{forecast_window.split(" ")[0]} Window</span></div>', unsafe_allow_html=True)

            v_col1, v_col2 = st.columns([1, 1])
            with v_col1:
                st.markdown('<div class="risk-value">96%</div>', unsafe_allow_html=True)
                st.markdown('<div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Peak Risk Probability</div>', unsafe_allow_html=True)
                st.markdown('<div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; margin-top: 15px; position: relative;"><div style="width: 96%; height: 100%; background: white; border-radius: 4px;"></div></div>', unsafe_allow_html=True)
            with v_col2:
                st.markdown('<div style="text-align: right; margin-top: 10px;">', unsafe_allow_html=True)
                st.markdown('<div style="color: #f97316; font-size: 1.8rem; font-weight: 900;">Tomorrow</div>', unsafe_allow_html=True)
                st.markdown('<div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">2pm</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            # --- BURNOUT CHART ---
            hours = [f"{i:02d}:00" for i in range(0, 24, 2)]
            risk_levels = [40, 68, 42, 71, 62, 70, 52, 65, 32, 64, 32, 28]
            colors = ['#f59e0b' if r > 40 else '#10b981' for r in risk_levels]
            colors[3] = '#f97316' # Highlight the peak
            colors[5] = '#f97316'

            fig = go.Figure(data=[go.Bar(
                x=hours,
                y=risk_levels,
                marker_color=colors,
                marker_line_width=0,
                width=1.2
            )])
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=0, r=0, t=20, b=0),
                height=250,
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', tickfont=dict(color='#94a3b8'), title='Risk %'),
                xaxis=dict(showgrid=False, tickfont=dict(color='#94a3b8')),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            clean_render("""
<div style="background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.1); border-radius: 8px; padding: 10px 15px; margin-top: 20px;">
    <div style="color: #f87171; font-size: 0.75rem; font-weight: 700; display: flex; align-items: center; gap: 8px;">
        📌 Critical Insight: Critical burnout window detected on Tomorrow 2pm. Predicted migraine onset with 82% confidence. Preventive intervention strongly recommended.
    </div>
</div>
            """)
            st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        # --- STRESS EVENT FORECAST (SIDEBAR) ---
        st.markdown('<div class="prediction-panel" style="padding: 24px;">', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; gap: 10px; align-items: center; margin-bottom: 25px;"><span style="color: #a855f7;">🌐</span><span style="color: white; font-weight: 800; font-size: 0.9rem;">Stress Event Forecast</span></div>', unsafe_allow_html=True)
        
        events = [
            ("Acute Stress Response", "Next 4-6 hours", 82),
            ("Cortisol Spike", "Tomorrow morning", 67),
            ("Recovery Window", "Tomorrow evening", 91)
        ]
        
        for name, time_lbl, val in events:
            st.markdown(f"""
<div style="background: rgba(15, 23, 42, 0.4); border-radius: 12px; padding: 15px; margin-bottom: 12px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 5px;">
<span style="color: white; font-size: 0.85rem; font-weight: 700;">{name}</span>
<span style="color: white; font-size: 0.7rem; font-weight: 800;">{val}%</span>
</div>
<div style="color: #94a3b8; font-size: 0.65rem; margin-bottom: 10px;">{time_lbl}</div>
<div style="width: 100%; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px;">
<div style="width: {val}%; height: 100%; background: #a855f7; border-radius: 2px;"></div>
</div>
</div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="height: 30px;"></div>', unsafe_allow_html=True)
        
        # --- MODEL CONFIDENCE ---
        st.markdown('<div style="display: flex; gap: 10px; align-items: center; margin-bottom: 25px;"><span style="color: #38bdf8;">📈</span><span style="color: white; font-weight: 800; font-size: 0.9rem;">Model Confidence</span></div>', unsafe_allow_html=True)
        
        models = [("Random Forest", 88), ("Neural Network", 92), ("Ensemble", 95)]
        for m_name, m_val in models:
            st.markdown(f"""
<div style="margin-bottom: 15px;">
<div style="color: #94a3b8; font-size: 0.75rem; margin-bottom: 6px;">{m_name}</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px;">
<div style="width: {m_val}%; height: 100%; background: white; border-radius: 3px;"></div>
</div>
</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- BIOMETRIC PREDICTIONS (SCREENSHOT 2) ---
    st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 30px;">Multi-Modal Biometric Predictions</h4>', unsafe_allow_html=True)
    
    t_axis = [f"{i}h" for i in range(48)]
    fig_bio = go.Figure()
    fig_bio.add_trace(go.Scatter(x=t_axis, y=np.random.normal(95, 2, 48), name="Resilience Index", line=dict(color="#a855f7", width=3), marker=dict(size=4)))
    fig_bio.add_trace(go.Scatter(x=t_axis, y=np.random.normal(70, 5, 48), name="Heart Rate Variability", line=dict(color="#10b981", width=2, dash='dot')))
    fig_bio.add_trace(go.Scatter(x=t_axis, y=np.random.normal(45, 3, 48), name="Galvanic Skin Response", line=dict(color="#f59e0b", width=2)))
    fig_bio.add_trace(go.Scatter(x=t_axis, y=np.random.normal(32, 1, 48), name="Skin Temperature", line=dict(color="#38bdf8", width=2)))
    
    fig_bio.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=10, b=0), height=300,
        font=dict(color="#94a3b8"),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', nticks=24),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'),
        legend=dict(orientation="h", y=-0.2, x=0.5, xanchor="center")
    )
    st.plotly_chart(fig_bio, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- AUTONOMOUS INTERVENTIONS (SCREENSHOT 2) ---
    clean_render("""
<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px;">
    <span style="font-size: 1.5rem; color: #10b981;">⚡</span>
    <span style="font-weight: 800; color: white; font-size: 1.2rem;">Autonomous Intervention Points</span>
</div>
    """)
    
    interventions = [
        ("Autonomous haptic breathing protocol", "8-minute session", "critical", "Next 2 hours", "Expected Impact: +15% SRI", "Pre-symptomatic HRV decay detected. Early intervention can prevent acute stress response."),
        ("Blue light reduction + temperature optimization", "Sleep window", "high", "This evening (6-8 PM)", "Expected Impact: +22% SRI", "Optimize tomorrow's baseline through circadian support and sleep quality enhancement."),
        ("Sunlight exposure protocol", "15 minutes within 1hr of waking", "medium", "Tomorrow morning", "Expected Impact: +12% SRI", "Cortisol awakening response normalization to prevent afternoon crash.")
    ]
    
    for title, sub, level, time_str, impact, desc in interventions:
        st.markdown(f"""
<div class="intervention-item">
    <div style="flex: 1;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
            <span style="background: {'#ef4444' if level=='critical' else '#f59e0b' if level=='high' else '#3b82f6'}; color: white; font-size: 0.65rem; font-weight: 900; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">{level}</span>
            <span style="color: white; font-size: 0.9rem; font-weight: 700;">{time_str}</span>
        </div>
        <div style="color: white; font-weight: 800; font-size: 1.05rem; margin-bottom: 4px;">{title} ({sub})</div>
        <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 10px;">{desc}</div>
        <div class="impact-badge">{impact}</div>
    </div>
    <div style="margin-left: 20px;">
        <div style="background: #10b981; color: white; padding: 8px 16px; border-radius: 6px; font-size: 0.8rem; font-weight: 800; cursor: pointer;">Auto-Schedule</div>
    </div>
</div>
        """, unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- ARCHITECTURE & EXPLANATION (SCREENSHOT 3) ---
    arch_col1, arch_col2 = st.columns(2)
    with arch_col1:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 30px;">Current vs Predicted State</h4>', unsafe_allow_html=True)
        # Radar Chart
        categories = ['HRV', 'GSR', 'Temperature', 'Sleep Quality', 'Activity']
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=[80, 50, 70, 90, 60], theta=categories, fill='toself', name='Current', line_color='#10b981'))
        fig_radar.add_trace(go.Scatterpolar(r=[60, 80, 85, 40, 75], theta=categories, fill='toself', name='Predicted', line_color='#f97316'))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, showticklabels=False, gridcolor='rgba(255,255,255,0.1)')),
            paper_bgcolor='rgba(0,0,0,0)', font=dict(color="#94a3b8"),
            margin=dict(l=40, r=40, t=10, b=10), showlegend=True,
            legend=dict(orientation="h", y=-0.1)
        )
        st.plotly_chart(fig_radar, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with arch_col2:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 30px;">AI Model Explanation</h4>', unsafe_allow_html=True)
        clean_render("""
<div style="margin-bottom: 25px;">
    <div style="display: flex; gap: 8px; align-items: center; margin-bottom: 15px;">
        <span style="color: #38bdf8;">ⓘ</span>
        <span style="color: white; font-weight: 800; font-size: 0.85rem;">Feature Importance</span>
    </div>
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;"><span style="color: #e2e8f0; font-size: 0.75rem;">HRV Trend (7-day)</span><span style="color: white; font-size: 0.7rem;">28.4%</span></div>
        <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px;"><div style="width: 28%; height: 100%; background: white; border-radius: 2px;"></div></div>
    </div>
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;"><span style="color: #e2e8f0; font-size: 0.75rem;">Sleep Debt</span><span style="color: white; font-size: 0.7rem;">22.1%</span></div>
        <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px;"><div style="width: 22%; height: 100%; background: white; border-radius: 2px;"></div></div>
    </div>
    <div style="margin-bottom: 12px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 6px;"><span style="color: #e2e8f0; font-size: 0.75rem;">Circadian Phase</span><span style="color: white; font-size: 0.7rem;">15.3%</span></div>
        <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.05); border-radius: 2px;"><div style="width: 15%; height: 100%; background: white; border-radius: 2px;"></div></div>
    </div>
</div>
<div style="background: rgba(168, 85, 247, 0.1); border: 1px solid rgba(168, 85, 247, 0.2); border-radius: 8px; padding: 12px; font-size: 0.7rem; color: #d8b4fe; line-height: 1.4;">
📊 <b>Methodology</b>: The ensemble model combines Random Forest (pattern recognition) with LSTM Neural Networks (temporal dependencies). Training data: 10,000+ anonymized sessions. Real-time inference with 5-second latency.
</div>
        """)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- TECHNICAL ARCHITECTURE FOOTER ---
    st.markdown("""
<div class="tech-architecture">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 20px;">
        <span style="font-size: 1.4rem; color: #38bdf8;">🌐</span>
        <span style="font-weight: 800; color: white; font-size: 1rem;">Technical Architecture</span>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 40px;">
        <div style="color: #94a3b8; font-size: 0.8rem; line-height: 1.8;">
            • Ensemble Model: RF + LSTM Neural Network<br>
            • Feature Engineering: 47 derived metrics<br>
            • Model Accuracy: 94.7% (p<0.001)<br>
            • Confidence Interval: 95% CI with bootstrapping
        </div>
        <div style="color: #94a3b8; font-size: 0.8rem; line-height: 1.8;">
            • Training Dataset: 10,247 sessions (14 days rolling)<br>
            • Prediction Latency: <5ms edge inference<br>
            • False Positive Rate: 3.2%<br>
            • Auto-retraining: Every 72 hours on new data
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

    # --- AI COACH MINI (V9.1) ---
    clean_render("""
<div class="ai-coach-mini">
    <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 15px;">
        <div style="display: flex; align-items: center; gap: 12px;">
            <div style="background: rgba(16, 185, 129, 0.2); width: 32px; height: 32px; border-radius: 8px; display: flex; align-items: center; justify-content: center; color: #10b981;">💡</div>
            <div style="color: white; font-weight: 800; font-size: 0.85rem;">AI Coach</div>
        </div>
        <span style="color: #94a3b8; font-size: 1rem; cursor: pointer;">×</span>
    </div>
    <div style="color: white; font-weight: 700; font-size: 0.95rem; margin-bottom: 8px;">Did You Know?</div>
    <div style="color: #a7f3d0; font-size: 0.8rem; line-height: 1.5; margin-bottom: 20px;">
        Your gut microbiome produces 90% of serotonin. Poor gut health can reduce HRV by 18% on average.
    </div>
    <div style="display: flex; gap: 15px;">
        <div style="background: #10b981; color: white; padding: 6px 14px; border-radius: 6px; font-size: 0.75rem; font-weight: 800;">Learn More</div>
        <div style="color: white; font-size: 0.75rem; font-weight: 700; display: flex; align-items: center; padding: 6px 0;">Next Tip →</div>
    </div>
    <div style="display: flex; justify-content: center; gap: 5px; margin-top: 15px;">
        <div style="width: 4px; height: 4px; border-radius: 50%; background: #059669;"></div>
        <div style="width: 12px; height: 4px; border-radius: 2px; background: #10b981;"></div>
        <div style="width: 4px; height: 4px; border-radius: 50%; background: #059669;"></div>
    </div>
</div>
    """)

if __name__ == "__main__":
    render_predictive_engine_page()
