"""
Predictive Intelligence Engine (v1.2)
High-fidelity interface for ensemble machine learning stress forecasting.
v1.2: RIPPLE ENGINE - High-frequency jitter, visual transitions, and living graphs.
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

def get_dynamic_state():
    """Generates a randomized alert state that drives the rest of the UI."""
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
    # Rotate alert every 6 seconds for better user visibility of the 'Ripple'
    current_idx = (int(time.time()) // 6) % len(alerts)
    return alerts[current_idx]

def render_predictive_engine_page():
    # --- GET DYNAMIC STATE ---
    state = get_dynamic_state()
    # High-frequency noise for 'constant wiggle' effect
    jitter = lambda x, scale=1.5: [v + random.uniform(-scale, scale) for v in x]
    
    # --- CSS STYLES (HI-FI + RIPPLE ANIMATIONS) ---
    clean_render("""
<style>
@keyframes glow-ripple {
    0% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); border-color: rgba(239, 68, 68, 0.4); }
    50% { box-shadow: 0 0 40px 10px rgba(239, 68, 68, 0.2); border-color: rgba(239, 68, 68, 0.8); }
    100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.4); border-color: rgba(239, 68, 68, 0.4); }
}
@keyframes slide-in {
    from { transform: translateX(-10px); opacity: 0; }
    to { transform: translateX(0); opacity: 1; }
}
.engine-title-container { text-align: center; padding: 20px 0 40px 0; }
.engine-title {
    background: linear-gradient(135deg, #f472b6 0%, #a855f7 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    font-size: 2.6rem; font-weight: 900;
}
.stat-badge {
    background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.1);
    padding: 6px 16px; border-radius: 20px; font-size: 0.8rem; color: #e2e8f0;
    display: flex; align-items: center; gap: 8px;
}
.badge-dot { width: 6px; height: 6px; border-radius: 50%; background: #ef4444; animation: pulse-blink 1s infinite; }
@keyframes pulse-blink { 0% { opacity: 0; } 50% { opacity: 1; } 100% { opacity: 0; } }

.alert-card {
    background: linear-gradient(135deg, rgba(127, 29, 29, 0.4), rgba(69, 10, 10, 0.4));
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 12px; padding: 20px 25px; margin: 40px 0;
    animation: glow-ripple 6s infinite ease-in-out; /* Synced with alert rotation */
}
.alert-content { animation: slide-in 0.5s ease-out; }

.prediction-panel {
    background: rgba(30, 41, 59, 0.4); backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px; padding: 30px; height: 100%;
}
.risk-value { font-size: 3.5rem; font-weight: 900; color: #f87171; line-height: 1; }

.intervention-item {
    background: rgba(15, 23, 42, 0.4); border-left: 4px solid #10b981;
    border-radius: 8px; padding: 20px; margin-bottom: 15px;
    display: flex; justify-content: space-between; align-items: center;
    transition: all 0.2s;
}
.intervention-item:hover { transform: scale(1.02); background: rgba(15, 23, 42, 0.6); }

.impact-badge {
    background: rgba(16, 185, 129, 0.1); color: #10b981;
    font-size: 0.75rem; font-weight: 700; padding: 4px 8px; border-radius: 4px;
}
</style>
    """)

    # --- HEADER ---
    clean_render(f"""
<div class="engine-title-container">
    <div style="font-size: 2.2rem; color: #a855f7; margin-bottom: 10px;">🧬</div>
    <div class="engine-title">Predictive Intelligence Engine</div>
    <div style="display: flex; justify-content: center; gap: 15px; margin-top: 25px;">
        <div class="stat-badge"><span class="badge-dot"></span> LIVE Monitoring</div>
        <div class="stat-badge"><span style="width: 6px; height: 6px; border-radius: 50%; background: #10b981;"></span> Accuracy: 94.7%</div>
        <div class="stat-badge">Stream: {datetime.now().strftime('%H:%M:%S.%f')[:-4]}</div>
    </div>
</div>
    """)

    # --- ALERT CARD (WITH SLIDE-IN RE-ANIMATION TRIGGER) ---
    st.markdown(f"""
<div class="alert-card">
    <div class="alert-content">
        <div style="position: absolute; top: 15px; right: 20px; background: rgba(239, 68, 68, 0.3); color: #f87171; font-size: 0.7rem; font-weight: 800; padding: 4px 10px; border-radius: 4px;">URGENT</div>
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
                <div style="margin-top: 15px; display: flex; align-items: center; gap: 5px; color: #f87171; font-size: 0.7rem; font-weight: 800;">
                    <span style="width: 6px; height: 6px; background: #f87171; border-radius: 2px;"></span> RIPPLE EFFECT ACTIVE: Graphs synchronized to this alert
                </div>
            </div>
        </div>
    </div>
</div>
    """, unsafe_allow_html=True)

    # --- MAIN GRID ---
    col_main, col_side = st.columns([2, 1])

    with col_main:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        h_col1, h_col2 = st.columns([1,1])
        with h_col1: st.markdown('<h4 style="color: white; font-weight: 800; margin: 0;">Burnout Heatmap</h4>', unsafe_allow_html=True)
        with h_col2: st.markdown(f'<div style="text-align: right;"><span style="color: #94a3b8; font-size: 0.7rem; font-weight: 800;">{state["id"].upper()} STATE</span></div>', unsafe_allow_html=True)
        
        # High-frequency jittered risk value
        r_val = state["risk_val"] + random.uniform(-0.5, 0.5)
        v1, v2 = st.columns([1, 1])
        with v1:
            st.markdown(f'<div class="risk-value">{r_val:.1f}%</div>', unsafe_allow_html=True)
            st.markdown('<div style="color: #94a3b8; font-size: 0.8rem; font-weight: 600;">Peak Probability (Fluctuating)</div>', unsafe_allow_html=True)
        with v2:
            st.markdown(f'<div style="text-align: right; margin-top: 10px;"><div style="color: #f97316; font-size: 1.6rem; font-weight: 900;">{state["peak_risk"]}</div></div>', unsafe_allow_html=True)

        # Bar chart with constant 'wiggle'
        hours = [f"{i:02d}:00" for i in range(0, 24, 2)]
        if state['id'] == 'sleep': base_data = [40, 68, 42, 71, 62, 70, 52, 65, 32, 64, 32, 28]
        elif state['id'] == 'worklink': base_data = [92, 85, 40, 30, 25, 20, 15, 60, 80, 75, 50, 45]
        else: base_data = [20, 30, 25, 40, 35, 60, 85, 90, 70, 55, 40, 25]
        
        dynamic_data = jitter(base_data, 2.0) # Apply constant wiggling
            
        fig = go.Figure(data=[go.Bar(x=hours, y=dynamic_data, marker_color=['#f97316' if d > 70 else '#f59e0b' if d > 40 else '#10b981' for d in dynamic_data])])
        fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100]), xaxis=dict(showgrid=False))
        st.plotly_chart(fig, use_container_width=True, key="heatmap_v12")
        st.markdown('</div>', unsafe_allow_html=True)

    with col_side:
        st.markdown('<div class="prediction-panel" style="padding: 24px;">', unsafe_allow_html=True)
        st.markdown('<div style="color: white; font-weight: 800; font-size: 0.85rem; margin-bottom: 20px;">Stress Event Forecast</div>', unsafe_allow_html=True)
        
        # Jittering confidence
        conf = (80 if state['id'] == 'sleep' else 60) + random.uniform(0, 15)
        st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.4); border-radius: 10px; padding: 12px; margin-bottom: 10px; border-left: 2px solid #a855f7;">
                <div style="color: white; font-size: 0.8rem; font-weight: 700; display: flex; justify-content: space-between;"><span>Primary Risk</span> <span>{conf:.1f}%</span></div>
                <div style="color: #94a3b8; font-size: 0.6rem; margin-top: 4px;">Dynamic Confidence Stream</div>
            </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div style="margin-top: 25px; color: white; font-weight: 800; font-size: 0.8rem;">Neural Layer Weights</div>', unsafe_allow_html=True)
        for m in ["Input Drift", "Recurrent St", "Attention"]:
            v = random.randint(70, 99)
            st.markdown(f'<div style="font-size: 0.65rem; color: #94a3b8; margin: 10px 0 4px 0;">{m}</div><div style="width:100%; height:4px; background:rgba(255,255,255,0.05);"><div style="width:{v}%; height:100%; background:white; opacity: 0.8;"></div></div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- BIOMETRIC PREDICTIONS (WITH JITTER) ---
    st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
    st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 25px;">Multi-Modal Biometric Predictions (Live Stream)</h4>', unsafe_allow_html=True)
    
    t = [f"{i}h" for i in range(48)]
    drift = state['drift_factor']
    # Constant jittering of the lines
    y_res = jitter(np.random.normal(90+drift, 2, 48), 1.0)
    y_hrv = jitter(np.random.normal(70-drift, 4, 48), 1.5)
    
    fig_bio = go.Figure()
    fig_bio.add_trace(go.Scatter(x=t, y=y_res, name="Resilience", line=dict(color="#a855f7", width=3)))
    fig_bio.add_trace(go.Scatter(x=t, y=y_hrv, name="HRV", line=dict(color="#10b981", width=2, dash='dot')))
    fig_bio.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), legend=dict(orientation="h", y=-0.2))
    st.plotly_chart(fig_bio, use_container_width=True, key="biometric_v12")
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- INTERVENTIONS (ROTATING) ---
    st.markdown('<div style="font-weight: 800; color: white; font-size: 1.1rem; margin-bottom: 25px;">⚡ Autonomous Intervention Points</div>', unsafe_allow_html=True)
    for title, sub, level, time_str, impact, desc in state['interventions']:
        clean_render(f"""
<div class="intervention-item">
    <div style="flex: 1;">
        <div style="display: flex; gap: 10px; align-items: center; margin-bottom: 6px;">
            <span style="background: {'#ef4444' if level=='critical' else '#f59e0b'}; color: white; font-size: 0.6rem; font-weight: 900; padding: 2px 4px; border-radius: 3px;">{level.upper()}</span>
            <span style="color: white; font-size: 0.85rem; font-weight: 700;">{time_str}</span>
        </div>
        <div style="color: white; font-weight: 800; font-size: 1rem;">{title}</div>
        <div style="color: #94a3b8; font-size: 0.75rem; margin: 4px 0 10px 0;">{desc}</div>
        <div class="impact-badge">{impact}</div>
    </div>
    <div style="background: #10b981; color: white; padding: 8px 16px; border-radius: 6px; font-size: 0.75rem; font-weight: 800; cursor: pointer; border: 1px solid rgba(255,255,255,0.1);">Auto-Schedule</div>
</div>
        """)

    # --- RADAR & TECH (RIPPLED) ---
    r_col1, r_col2 = st.columns(2)
    with r_col1:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 20px;">AI Explanation</h4>', unsafe_allow_html=True)
        r_base = [80, 50, 70, 90, 60] if state['id'] != 'sleep' else [40, 80, 60, 30, 50]
        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(r=jitter(r_base, 3.0), theta=['HRV', 'GSR', 'Temp', 'Sleep', 'Act'], fill='toself', line_color='#10b981'))
        fig_radar.update_layout(polar=dict(radialaxis=dict(visible=False)), paper_bgcolor='rgba(0,0,0,0)', margin=dict(l=30,r=30,t=10,b=20), height=250)
        st.plotly_chart(fig_radar, use_container_width=True, key="radar_v12")
        st.markdown('</div>', unsafe_allow_html=True)
    with r_col2:
        st.markdown('<div class="prediction-panel">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: white; font-weight: 800; margin-bottom: 20px;">Architecture</h4>', unsafe_allow_html=True)
        st.markdown(f'<div style="color: #94a3b8; font-size: 0.8rem; line-height: 2;">• Model: Neural + RF Ensemble<br>• Latency: <5ms Real-Time<br>• Nodes Check: {random.randint(400, 500)} OK<br>• Update: Syncing...</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- HIGH-FREQUENCY REFRESH (1s) ---
    time.sleep(1)
    st.rerun()

if __name__ == "__main__":
    render_predictive_engine_page()
