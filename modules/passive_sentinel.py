import streamlit as st
import plotly.graph_objects as go
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# PASSIVE SENTINEL LOGIC MODEL
# ==========================================

class PassiveSentinelModel:
    def __init__(self):
        # Initialize Digital Twin Baseline
        self.baseline = {
            "typing_var": 50,  # ms
            "notification_freq": 10, # /hour
            "noise_level": 40, # dB
            "motion": 20 # arbitrary units
        }
        
        # Current State Simulation
        if 'sentinel_history' not in st.session_state:
            st.session_state.sentinel_history = []
        
        # Prediction State (Stable, Rising, Imminent)
        if 'sentinel_status' not in st.session_state:
            st.session_state.sentinel_status = "Stable"
            
        if 'stress_prob' not in st.session_state:
            st.session_state.stress_prob = 15.0

    def update_simulation(self):
        """Simulates 'always-on' background data collection and analysis."""
        
        # 1. Simulate Live Data Stream (Deviations)
        # We simulate a "Rising" stress event if requested or randomly
        current_time = datetime.now()
        
        # Random fluctuations
        typing_cur = self.baseline["typing_var"] + random.uniform(-10, 40)
        notif_cur = self.baseline["notification_freq"] + random.uniform(-5, 15)
        noise_cur = self.baseline["noise_level"] + random.uniform(-10, 30)
        
        # Calculate Deviation Magnitude (Sigma)
        # Simplified for demo: Deviation Score 0-100
        dev_score = 0
        factors = []
        
        if typing_cur > self.baseline["typing_var"] * 1.2:
            dev_score += 20
            factors.append({"name": "Typing Variability", "val": f"↑ {True and int(((typing_cur - 50)/50)*100)}%", "desc": "Erratic keystrokes detected"})
            
        if notif_cur > self.baseline["notification_freq"] * 1.5:
            dev_score += 15
            factors.append({"name": "Notification Flood", "val": "High", "desc": "Frequent interruptions"})
            
        if noise_cur > 60:
            dev_score += 10
            factors.append({"name": "Ambient Noise", "val": f"{int(noise_cur)}dB", "desc": "Loud environment"})
            
        # Add Drift/Hysteresis to Probability
        target_prob = min(99, max(5, dev_score + random.uniform(0, 20)))
        
        # Smooth transition
        st.session_state.stress_prob = (st.session_state.stress_prob * 0.8) + (target_prob * 0.2)
        
        # Determine Status
        prob = st.session_state.stress_prob
        if prob > 80:
            st.session_state.sentinel_status = "Imminent"
        elif prob > 50:
            st.session_state.sentinel_status = "Rising"
        else:
            st.session_state.sentinel_status = "Stable"
            
        # Log History for Graph
        st.session_state.sentinel_history.append({
            "time": current_time,
            "prob": prob
        })
        
        # Keep last 60 points
        if len(st.session_state.sentinel_history) > 60:
            st.session_state.sentinel_history.pop(0)
            
        return factors

# ==========================================
# UI RENDERING
# ==========================================

def render_passive_sentinel():
    model = PassiveSentinelModel()
    deviations = model.update_simulation()
    
    # Refresh to simulate "Always On" feel if in main loop, 
    # but here we rely on Streamlit's rerun capability or a timer if we want auto-update.
    # For now, we assume user interaction or global timer refreshes it.

    status = st.session_state.sentinel_status
    prob = st.session_state.stress_prob
    
    # Color Map
    status_colors = {
        "Stable": "#10b981", # Green
        "Rising": "#f59e0b", # Yellow
        "Imminent": "#ef4444" # Red
    }
    main_color = status_colors[status]
    
    # --- HERO SECTION ---
    st.markdown(f"""
    <div style="margin-bottom: 20px;">
        <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #00f2fe, #4facfe); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
           🔔 Passive Stress Sentinel
        </div>
        <div style="color: #94a3b8; font-size: 1.1rem; margin-top: 5px;">
            Always-on monitoring that alerts you before stress peaks—no active input required.
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Layout
    col_status, col_context = st.columns([1, 1.5], gap="large")
    
    with col_status:
        # A. STATUS PANEL & B. CONFIDENCE RING
        st.markdown(f"""
        <div style="
            background: rgba(15, 23, 42, 0.6); 
            border: 1px solid {main_color}40; 
            border-radius: 20px; 
            padding: 30px; 
            text-align: center;
            box-shadow: 0 0 30px {main_color}10;
        ">
            <div style="font-size: 0.9rem; letter-spacing: 2px; text-transform: uppercase; color: #64748b; margin-bottom: 20px;">
                Current Threat Level
            </div>
            
            <!-- RING ANIMATION (CSS helper) -->
            <div style="
                width: 200px; height: 200px; margin: 0 auto;
                border-radius: 50%;
                border: 8px solid #1e293b;
                border-top: 8px solid {main_color};
                border-right: 8px solid {main_color};
                display: flex; flex-direction: column; justify-content: center; align-items: center;
                box-shadow: 0 0 20px {main_color}20;
                transform: rotate(-45deg); /* Static for demo, could animate */
            ">
                <div style="transform: rotate(45deg); text-align: center;">
                    <div style="font-size: 3rem; font-weight: 800; color: white; line-height: 1;">
                        {int(prob)}%
                    </div>
                    <div style="font-size: 0.8rem; color: {main_color}; font-weight: 700;">PROBABILITY</div>
                </div>
            </div>
            
            <div style="margin-top: 30px;">
                <div style="font-size: 2rem; font-weight: 700; color: {main_color}; text-shadow: 0 0 10px {main_color}40;">
                    {status}
                </div>
                <div style="color: #cbd5e1; font-size: 0.9rem; margin-top: 5px;">
                    {get_status_message(status)}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # D. EARLY ACTION SUGGESTION
        if status != "Stable":
            st.markdown(f"""
            <div style="margin-top: 20px; background: rgba(51, 65, 85, 0.3); border-left: 4px solid {main_color}; padding: 15px; border-radius: 0 12px 12px 0;">
                <div style="display: flex; gap: 10px; align-items: start;">
                    <div style="font-size: 1.5rem;">🧘</div>
                    <div>
                        <div style="font-weight: 600; color: white;">Suggested Intervention</div>
                        <div style="font-size: 0.9rem; color: #cbd5e1;">Your patterns match early cognitive overload. A 60-second reset could prevent a peak.</div>
                        <div style="margin-top: 10px; display: flex; gap: 10px;">
                            <button style="background: {main_color}; color: black; border: none; padding: 6px 12px; border-radius: 6px; font-weight: 600; cursor: pointer;">Start 1-min Reset</button>
                            <button style="background: transparent; border: 1px solid #475569; color: #94a3b8; padding: 6px 12px; border-radius: 6px; cursor: pointer;">Dismiss</button>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
    with col_context:
        # C. EXPLAINABILITY PANEL
        st.markdown("#### 🕵️ What Changed? (Explainability)")
        st.markdown("Analysis of behavioral and environmental deviations from your Digital Twin baseline.")
        
        if not deviations:
            st.info("No significant deviations detected. Your biomarkers are tracking with your baseline.")
        else:
            for factor in deviations:
                st.markdown(f"""
                <div style="
                    display: flex; justify-content: space-between; align-items: center;
                    background: #0f172a; border: 1px solid #1e293b; 
                    padding: 12px 20px; border-radius: 10px; margin-bottom: 10px;
                ">
                    <div>
                        <div style="color: #e2e8f0; font-weight: 600;">{factor['name']}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8;">{factor['desc']}</div>
                    </div>
                    <div style="font-family: monospace; font-weight: 700; color: #f43f5e; background: #f43f5e20; padding: 4px 8px; border-radius: 6px;">
                        {factor['val']}
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
        # E. TIMELINE VIEW
        st.markdown("#### 📉 Stress Probability Micro-Trend (Last 30m)")
        
        # Prepare Data
        hist = st.session_state.sentinel_history
        if len(hist) > 1:
            df = pd.DataFrame(hist)
            # Create Plotly Chart
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(df))), 
                y=df['prob'],
                mode='lines',
                fill='tozeroy',
                line=dict(color=main_color, width=3),
                fillcolor=f"rgba({int(main_color[1:3], 16)}, {int(main_color[3:5], 16)}, {int(main_color[5:7], 16)}, 0.1)"
            ))
            
            fig.add_hline(y=50, line_dash="dot", line_color="rgba(255,255,255,0.2)", annotation_text="Alert Threshold", annotation_position="top right")
            
            fig.update_layout(
                height=250,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100]),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
        # Data Handling Info
        with st.expander("🔒 Privacy & Ethical Data Use"):
            st.markdown("""
            **How Passive Sentinel protects your privacy:**
            *   **Metadata only:** We measure typing *rhythm*, not what you type.
            *   **Local processing:** All raw sensor data is processed on-device.
            *   **No recording:** Audio is sampled for decibel level only; no conversations are recorded.
            *   **You are in control:** Pause monitoring at any time.
            """)

def get_status_message(status):
    if status == "Stable":
        return "No elevated stress patterns detected. Baseline normal."
    elif status == "Rising":
        return "Early stress indicators detected — monitor closely."
    else:
        return "High probability of stress escalation in the next 15 minutes."
