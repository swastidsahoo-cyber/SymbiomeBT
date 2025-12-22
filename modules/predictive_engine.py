"""
Predictive Intelligence Engine (v1.3)
High-fidelity interface for ensemble machine learning stress forecasting.
v1.3: HI-FI TABS & RIPPLE - Restoring exact mockup tabs with 1s jitter engine.
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

def get_dynamic_state(window_selection="24h Forecast"):
    """Generates a randomized alert state tied to the selected window."""
    alerts = [
        {
            "id": "sleep",
            "title": "Cumulative sleep debt exceeding resilience threshold",
            "desc": "3 consecutive nights of sub-optimal recovery detected. Tomorrow's baseline SRI projected to drop 18%.",
            "peak_risk": "Tomorrow 2pm",
            "risk_val": 96,
            "drift_factor": 15,
            "interventions": [
                ("Autonomous haptic breathing protocol", "8-minute session", "critical", "Next 2 hours", "Expected Impact: +15% SRI", "Pre-symptomatic HRV decay detected."),
                ("Blue light reduction + temp optimization", "Sleep window", "high", "Tonight 8 PM", "Expected Impact: +22% SRI", "Circadian support.")
            ]
        },
        {
            "id": "worklink",
            "title": "Anticipatory stress spike detected (Meeting Load)",
            "desc": "Calendar analysis shows 4 high-stakes meetings tomorrow. Cortisol baseline rising pre-emptively.",
            "peak_risk": "Next 4 hours",
            "risk_val": 84,
            "drift_factor": -8,
            "interventions": [
                ("Vagus nerve stimulation session", "15 mins", "high", "In 30 mins", "Expected Impact: +10% SRI", "Sympathetic nervous system regulation."),
                ("Cognitive reappraisal exercise", "AI-guided", "medium", "Before 2 PM", "Expected Impact: +8% SRI", "Stress mindset shift.")
            ]
        },
        {
            "id": "environ",
            "title": "Environmental Stress Sensitivity Warning",
            "desc": "Ambient noise and CO2 levels in 'Home Office' correlating with HRV stabilization failure.",
            "peak_risk": "Tonight 10pm",
            "risk_val": 72,
            "drift_factor": 5,
            "interventions": [
                ("Active noise mitigation protocol", "Immediate", "medium", "Now", "Expected Impact: +12% SRI", "Sensory load reduction."),
                ("Air quality optimization cycle", "Purification", "low", "Tonight", "Expected Impact: +5% SRI", "Physiological load reduction.")
            ]
        }
    ]
    # Mix state based on both Time and Window Selection for variety
    seed = (int(time.time()) // 8) + len(window_selection)
    return alerts[seed % len(alerts)]

def render_predictive_engine_page():
    # --- CSS STYLES (MATCHING MOCKUP EXACTLY) ---
    clean_render("""
<style>
@keyframes glow-ripple {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); border-color: rgba(239, 68, 68, 0.4); }
    50% { box-shadow: 0 0 40px 10px rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.8); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); border-color: rgba(239, 68, 68, 0.4); }
}
.engine-title {
    background: linear-gradient(135deg, #f472b6 0%, #a855f7 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2.6rem; font-weight: 900; text-align: center;
}
.stat-badge {
    background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 6px 16px; border-radius: 20px; font-size: 0.8rem; color: #e2e8f0;
    display: flex; align-items: center; gap: 8px;
}
.alert-card {
    background: linear-gradient(135deg, rgba(127, 29, 29, 0.3), rgba(69, 10, 10, 0.3));
    border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px;
    padding: 20px 25px; margin: 30px 0;
    animation: glow-ripple 8s infinite ease-in-out;
}
.prediction-panel {
    background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 20px;
    padding: 30px; height: 100%; position: relative;
}
/* TAB STYLING TO MATCH MOCKUP */
div[data-testid="stHorizontalBlock"] button {
    background: transparent !important; border: 1px solid rgba(255,255,255,0.1) !important;
    color: #94a3b8 !important; border-radius: 8px !important;
}
div[data-testid="stHorizontalBlock"] button[kind="primary"] {
    background: white !important; color: #020617 !important; border: none !important;
}

.intervention-item {
    background: rgba(15, 23, 42, 0.4); border-left: 4px solid #10b981;
    border-radius: 8px; padding: 20px; margin-bottom: 15px;
    display: flex; justify-content: space-between; align-items: center;
}
.risk-value { font-size: 3.5rem; font-weight: 900; color: #f87171; line-height: 1; }
</style>
    """)

    # --- HEADER ---
    clean_render(f"""
<div style="text-align: center; margin-bottom: 40px;">
    <div style="font-size: 2.2rem; color: #a855f7; margin-bottom: 10px;">🧬</div>
    <div class="engine-title">Predictive Intelligence Engine</div>
    <p style="color: #94a3b8; font-size: 0.95rem; margin-top: 10px;">
        Ensemble Machine Learning (Random Forest + Neural Networks) predicting physiological stress events before conscious awareness
    </p>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 25px;">
        <div class="stat-badge"><span style="width:6px;height:6px;background:#a855f7;border-radius:50%;"></span> Live Model: v3.2.1</div>
        <div class="stat-badge"><span style="width:6px;height:6px;background:#10b981;border-radius:50%;"></span> Accuracy: 94.7%</div>
        <div class="stat-badge"><span style="width:6px;height:6px;background:#38bdf8;border-radius:50%;"></span> Last Update: {datetime.now().strftime('%H:%M:%S')}</div>
    </div>
</div>
    """)

    # --- FORECAST WINDOW TABS (HI-FI) ---
    t_col1, t_col2, t_col3 = st.columns([1, 2, 1])
    with t_col2:
        # We simulate the exact mockup buttons using radio or a custom row
        selected_window = st.radio(
            "Forecast Window Selection",
            ["24h Forecast", "48h Forecast", "72h Forecast"],
            index=1,
            horizontal=True,
            label_visibility="collapsed"
        )
    
    # Get state based on time AND selected window
    state = get_dynamic_state(selected_window)
    jitter = lambda x, scale=2.5: [v + random.uniform(-scale, scale) for v in x]

    # --- ALERT CARD ---
    clean_render(f"""
<div class="alert-card">
    <div style="position: absolute; top: 15px; right: 20px; background: rgba(239, 68, 68, 0.2); color: #f87171; font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 4px;">URGENT</div>
    <div style="display: flex; gap: 15px; align-items: flex-start;">
        <span style="font-size: 1.4rem; color: #ef4444;">⚠️</span>
        <div>
            <div style="font-weight: 800; color: white; font-size: 1.05rem; margin-bottom: 5px;">Predictive Alert System</div>
            <div style="font-weight: 700; color: #fecaca; font-size: 0.95rem; margin-bottom: 8px;">
                ⚠️ {state['title']}
            </div>
            <div style="color: #94a3b8; font-size: 0.85rem; line-height: 1.4;">
                {state['desc']}
            </div>
        </div>
    </div>
</div>
    """)

    # --- MAIN GRID ---
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        h1, h2 = st.columns([1,1])
        with h1: st.markdown('<h4 style="color: white; font-weight: 800; margin: 0;">Burnout Probability Heatmap</h4>', unsafe_allow_html=True)
        with h2: st.markdown(f'<div style="text-align: right;"><span style="color: #f87171; font-size: 0.65rem; background: rgba(239,68,68,0.2); padding: 3px 8px; border-radius: 4px; font-weight: 800;">{selected_window.split(" ")[0]} Window</span></div>', unsafe_allow_html=True)
        
        v1, v2 = st.columns([1, 1])
        with v1:
            r_val = state["risk_val"] + random.uniform(-0.8, 0.8)
            st.markdown(f'<div class="risk-value">{r_val:.1f}%</div>', unsafe_allow_html=True)
            st.markdown('<div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Peak Risk Probability (LIVE)</div>', unsafe_allow_html=True)
            st.markdown(f'<div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px; margin-top: 15px;"><div style="width: {r_val}%; height: 100%; background: white; border-radius: 4px;"></div></div>', unsafe_allow_html=True)
        with v2:
            st.markdown(f'<div style="text-align: right; margin-top: 10px;"><div style="color: #f97316; font-size: 1.8rem; font-weight: 900;">{state["peak_risk"]}</div><div style="color: #94a3b8; font-size: 0.85rem; font-weight: 600;">Peak Stress Window</div></div>', unsafe_allow_html=True)

        # Bar chart with Jitter
        hours = [f"{i:02d}:00" for i in range(0, 24, 2)]
        if state['id'] == 'sleep': base_d = [40, 68, 42, 71, 62, 70, 52, 65, 32, 64, 32, 28]
        elif state['id'] == 'worklink': base_d = [92, 85, 40, 30, 25, 20, 15, 60, 80, 75, 50, 45]
        else: base_d = [20, 30, 25, 40, 35, 60, 85, 90, 70, 55, 40, 25]
        
        fig = go.Figure(data=[go.Bar(x=hours, y=jitter(base_d), marker_color=['#f97316' if d > 70 else '#f59e0b' if d > 40 else '#10b981' for d in base_d])])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100]), xaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True, key=f"heatmap_{selected_window}")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="prediction-panel" style="padding: 24px;">', unsafe_allow_html=True)
        st.markdown('<div style="display: flex; gap: 10px; align-items: center; margin-bottom: 25px;"><span style="color: #a855f7;">🌐</span><span style="color: white; font-weight: 800; font-size: 0.9rem;">Stress Event Forecast</span></div>', unsafe_allow_html=True)
        
        events = [("Acute Stress", "4-6h", 82), ("Cortisol Spike", "AM", 67), ("Recovery Win", "PM", 91)]
        for name, time_lbl, val in events:
            j_val = val + random.randint(-2, 2)
            st.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.4); border-radius: 12px; padding: 15px; margin-bottom: 12px;">
                    <div style="display: flex; justify-content: space-between; align-items: center;"><span style="color: white; font-size: 0.85rem; font-weight: 700;">{name}</span><span style="color: white; font-size: 0.7rem; font-weight: 800;">{j_val}%</span></div>
                    <div style="color: #94a3b8; font-size: 0.65rem; margin-top: 4px;">{time_lbl} forecast</div>
                </div>
            """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: 30px; font-weight: 800; color: white; font-size: 0.85rem;">Model Confidence</div>', unsafe_allow_html=True)
        for m in ["Random Forest", "Neural Net", "Ensemble"]:
            v = random.randint(80, 99)
            st.markdown(f'<div style="font-size: 0.7rem; color: #94a3b8; margin: 10px 0 4px 0;">{m}</div><div style="width:100%; height:4px; background:rgba(255,255,255,0.05);"><div style="width:{v}%; height:100%; background:white;"></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- BIOMETRIC PREDICTIONS (WITH JITTER) ---
    st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 30px;">Multi-Modal Biometric Predictions (Live)</h4>', unsafe_allow_html=True)
    
    t = [f"{i}h" for i in range(48)]
    d = state['drift_factor']
    fig_bio = go.Figure()
    fig_bio.add_trace(go.Scatter(x=t, y=jitter(np.random.normal(90+d, 2, 48)), name="Resilience Index", line=dict(color="#a855f7", width=3)))
    fig_bio.add_trace(go.Scatter(x=t, y=jitter(np.random.normal(70-d, 5, 48)), name="HRV", line=dict(color="#10b981", width=2, dash='dot')))
    fig_bio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=280, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_bio, use_container_width=True, key=f"bio_{selected_window}")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- INTERVENTIONS ---
    st.markdown('<div style="display: flex; align-items: center; gap: 12px; margin-bottom: 25px;"><span style="font-size: 1.5rem; color: #10b981;">⚡</span><span style="font-weight: 800; color: white; font-size: 1.2rem;">Autonomous Intervention Points</span></div>', unsafe_allow_html=True)
    for title, sub, level, t_str, impact, desc in state['interventions']:
        clean_render(f"""
<div class="intervention-item">
    <div style="flex: 1;">
        <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 8px;">
            <span style="background: {'#ef4444' if level=='critical' else '#f59e0b'}; color: white; font-size: 0.65rem; font-weight: 900; padding: 2px 6px; border-radius: 4px; text-transform: uppercase;">{level}</span>
            <span style="color: white; font-size: 0.9rem; font-weight: 700;">{t_str}</span>
        </div>
        <div style="color: white; font-weight: 800; font-size: 1.1rem;">{title} ({sub})</div>
        <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 4px;">{desc}</div>
        <div class="impact-badge">{impact}</div>
    </div>
    <div style="background: #10b981; color: white; padding: 10px 20px; border-radius: 8px; font-size: 0.8rem; font-weight: 800; cursor: pointer;">Auto-Schedule</div>
</div>
        """)

    # --- ARCHITECTURE (HI-FI RADAR) ---
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    r_c1, r_c2 = st.columns(2)
    with r_c1:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 20px;">Current vs Predicted State</h4>', unsafe_allow_html=True)
        r_vals = [80, 50, 70, 90, 60] if state['id'] != 'sleep' else [40, 80, 60, 30, 50]
        fig_r = go.Figure()
        fig_r.add_trace(go.Scatterpolar(r=jitter(r_vals, 4.0), theta=['HRV', 'GSR', 'Temp', 'Sleep', 'Act'], fill='toself', line_color='#10b981'))
        fig_r.update_layout(polar=dict(radialaxis=dict(visible=False)), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=30,r=30,t=10,b=20), height=250)
        st.plotly_chart(fig_r, use_container_width=True, key=f"radar_{selected_window}")
        st.markdown('</div>', unsafe_allow_html=True)
    with r_c2:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 20px;">Technical Architecture</h4>', unsafe_allow_html=True)
        st.markdown('<div style="color: #94a3b8; font-size: 0.85rem; line-height: 2;">• Ensemble: Neural + RF Multi-Layer<br>• Model Accuracy: 94.7% (p<0.001)<br>• Retraining: Every 72h on Live Data<br>• Latency: <5ms Real-Time Inference</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 1S HIGH-FREQUENCY REFRESH ---
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    render_predictive_engine_page()
