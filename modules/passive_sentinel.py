import streamlit as st
import plotly.graph_objects as go
import random
import time
from datetime import datetime

# ==========================================
# PASSIVE SENTINEL - EXACT UI MATCH
# ==========================================

def render_passive_sentinel():
    """Renders Passive Sentinel matching the exact design screenshots."""
    
    # Initialize session state
    if 'sentinel_enabled' not in st.session_state:
        st.session_state.sentinel_enabled = False
    if 'sentinel_sensitivity' not in st.session_state:
        st.session_state.sentinel_sensitivity = 'Medium'
    if 'stress_probability' not in st.session_state:
        st.session_state.stress_probability = random.randint(60, 95)
    if 'probability_history' not in st.session_state:
        st.session_state.probability_history = [random.randint(40, 80) for _ in range(60)]
    
    # Update probability if enabled
    if st.session_state.sentinel_enabled:
        st.session_state.stress_probability = min(99, max(10, st.session_state.stress_probability + random.uniform(-5, 5)))
        st.session_state.probability_history.append(st.session_state.stress_probability)
        if len(st.session_state.probability_history) > 60:
            st.session_state.probability_history.pop(0)
    
    # ==========================================
    # HEADER - Purple gradient with bell icon
    # ==========================================
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 25px;">
        <div style="font-size: 2.5rem;">🔔</div>
        <div>
            <div style="font-size: 2rem; font-weight: 700; background: linear-gradient(90deg, #c084fc, #a855f7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                Passive Stress Sentinel
            </div>
            <div style="color: #94a3b8; font-size: 1rem;">
                Always-on monitoring that alerts you before stress peaks—no active input required
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # MONITORING TOGGLE
    # ==========================================
    col_toggle_label, col_toggle_switch = st.columns([4, 1])
    
    with col_toggle_label:
        if st.session_state.sentinel_enabled:
            st.markdown("""
            <div style="background: rgba(168, 85, 247, 0.1); border: 1px solid #a855f7; border-radius: 12px; padding: 15px;">
                <div style="color: #c084fc; font-weight: 600; font-size: 1.1rem;">🟣 Passive Monitoring Active</div>
                <div style="color: #94a3b8; font-size: 0.9rem;">Analyzing passive signals in real-time</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: rgba(71, 85, 105, 0.1); border: 1px solid #475569; border-radius: 12px; padding: 15px;">
                <div style="color: #94a3b8; font-weight: 600; font-size: 1.1rem;">⚫ Monitoring Paused</div>
                <div style="color: #64748b; font-size: 0.9rem;">Enable to receive early stress warnings</div>
            </div>
            """, unsafe_allow_html=True)
    
    with col_toggle_switch:
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        st.session_state.sentinel_enabled = st.toggle("ON" if st.session_state.sentinel_enabled else "OFF", 
                                                      value=st.session_state.sentinel_enabled, 
                                                      key='sentinel_toggle_main')
    
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # CONDITIONAL RENDERING
    # ==========================================
    
    if st.session_state.sentinel_enabled:
        # ENABLED STATE - Show full monitoring interface
        
        # Early Stress Alert Banner (if probability > 70%)
        if st.session_state.stress_probability > 70:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); border: 2px solid #ef4444; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
                <div style="display: flex; align-items: start; gap: 15px;">
                    <div style="font-size: 2rem;">⚠️</div>
                    <div style="flex: 1;">
                        <div style="color: white; font-weight: 700; font-size: 1.2rem; margin-bottom: 5px;">Early Stress Signs Detected</div>
                        <div style="color: #fca5a5; font-size: 0.95rem; margin-bottom: 15px;">
                            Symbiome noticed patterns that typically precede stress. A 60-second breathing exercise might help.
                        </div>
                        <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 10px;">
                            <span style="background: rgba(0,0,0,0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; color: #fca5a5;">HRV drop detected</span>
                            <span style="background: rgba(0,0,0,0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; color: #fca5a5;">Elevated ambient noise</span>
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            col_btn1, col_btn2 = st.columns([1, 3])
            with col_btn1:
                if st.button("🧘 Start 60s Breathing", use_container_width=True, type="primary"):
                    st.toast("Breathing exercise started", icon="🧘")
            with col_btn2:
                if st.button("Dismiss (snooze 10m)", use_container_width=True):
                    st.toast("Alert dismissed", icon="✓")
            
            st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
        
        # Real-Time Stress Probability Display
        risk_level = "High risk" if st.session_state.stress_probability > 75 else "Moderate" if st.session_state.stress_probability > 50 else "Low risk"
        risk_color = "#ef4444" if st.session_state.stress_probability > 75 else "#f59e0b" if st.session_state.stress_probability > 50 else "#10b981"
        
        st.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid {risk_color}40; border-radius: 16px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="font-size: 0.85rem; letter-spacing: 1px; text-transform: uppercase; color: #64748b; margin-bottom: 5px;">
                        ⚡ Real-Time Stress Probability
                    </div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">
                        Live assessment based on passive signals (updates every second)
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 3rem; font-weight: 800; color: {risk_color}; line-height: 1;">
                        {int(st.session_state.stress_probability)}%
                    </div>
                    <div style="font-size: 0.75rem; color: {risk_color}; font-weight: 600;">
                        {risk_level}
                    </div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Probability Graph
        fig = go.Figure()
        x_vals = list(range(len(st.session_state.probability_history)))
        y_vals = st.session_state.probability_history
        
        fig.add_trace(go.Scatter(
            x=x_vals,
            y=y_vals,
            mode='lines',
            fill='tozeroy',
            line=dict(color='#a855f7', width=2),
            fillcolor='rgba(168, 85, 247, 0.3)'
        ))
        
        fig.add_hline(y=50, line_dash="dot", line_color="rgba(148, 163, 184, 0.3)", annotation_text="Moderate", annotation_position="right")
        fig.add_hline(y=75, line_dash="dot", line_color="rgba(239, 68, 68, 0.5)", annotation_text="Alert", annotation_position="right")
        
        fig.update_layout(
            height=250,
            margin=dict(l=0, r=0, t=10, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15, 23, 42, 0.6)',
            xaxis=dict(showgrid=False, visible=False),
            yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100], title=""),
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Passive Signals Live Readings
        st.markdown("#### 📊 Passive Signals")
        st.markdown("<div style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px;'>Live readings from device sensors and behavioral patterns</div>", unsafe_allow_html=True)
        
        col1, col2, col3, col4, col5, col6 = st.columns(6)
        
        signals = [
            ("💓", "63", "HRV (ms)", col1),
            ("🔊", "46", "Noise (dB)", col2),
            ("⌨️", "32", "Typing Var", col3),
            ("📱", "16", "Motion", col4),
            ("🔔", "0", "Notifications", col5),
            ("💡", "78", "Brightness", col6)
        ]
        
        for icon, value, label, col in signals:
            with col:
                st.markdown(f"""
                <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 12px; text-align: center;">
                    <div style="font-size: 1.5rem; margin-bottom: 5px;">{icon}</div>
                    <div style="font-size: 1.5rem; font-weight: 700; color: white;">{value}</div>
                    <div style="font-size: 0.7rem; color: #64748b;">{label}</div>
                </div>
                """, unsafe_allow_html=True)
    
    else:
        # DISABLED STATE - Show "Passive Monitoring is Off"
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px; background: rgba(15, 23, 42, 0.4); border-radius: 16px; border: 1px solid #1e293b;">
            <div style="font-size: 4rem; margin-bottom: 20px; opacity: 0.5;">🔕</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 10px;">Passive Monitoring is Off</div>
            <div style="color: #94a3b8; max-width: 500px; margin: 0 auto 30px; line-height: 1.6;">
                Enable passive monitoring to receive early stress warnings without having to actively provide data. 
                The system analyzes device sensors and behavioral patterns to detect stress before you consciously feel it.
            </div>
            <button style="background: #a855f7; color: white; border: none; padding: 12px 24px; border-radius: 8px; font-weight: 600; font-size: 1rem; cursor: pointer;">
                ▶ Enable Passive Monitoring
            </button>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
    
    # ==========================================
    # SENSOR PERMISSIONS (Always visible)
    # ==========================================
    st.markdown("### 🛡️ Sensor Permissions")
    st.markdown("<div style='color: #94a3b8; margin-bottom: 15px;'>Control which passive signals are collected (local processing only)</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    sensors = [
        ("📷", "Camera (PPG)", "Heart rate variability", col1),
        ("🎤", "Microphone", "Ambient noise level", col2),
        ("📱", "Motion Sensors", "Agitation & restlessness", col1),
        ("🔔", "Notification Tracking", "Count only, no content", col2)
    ]
    
    for icon, title, desc, col in sensors:
        with col:
            st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
                <div style="display: flex; align-items: center; gap: 12px;">
                    <div style="font-size: 1.5rem;">{icon}</div>
                    <div style="flex: 1;">
                        <div style="color: white; font-weight: 600;">{title}</div>
                        <div style="font-size: 0.8rem; color: #94a3b8;">{desc}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            st.checkbox(f'Enable {title}', value=True, key=f'sensor_{title.replace(" ", "_")}')
    
    # ==========================================
    # ALERT SENSITIVITY
    # ==========================================
    st.markdown("### ⚙️ Alert Sensitivity")
    st.markdown("<div style='color: #94a3b8; margin-bottom: 15px;'>Adjust how sensitive the passive monitoring system is to stress signals</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("Low", use_container_width=True, type="primary" if st.session_state.sentinel_sensitivity == 'Low' else "secondary"):
            st.session_state.sentinel_sensitivity = 'Low'
    with col2:
        if st.button("Medium", use_container_width=True, type="primary" if st.session_state.sentinel_sensitivity == 'Medium' else "secondary"):
            st.session_state.sentinel_sensitivity = 'Medium'
    with col3:
        if st.button("High", use_container_width=True, type="primary" if st.session_state.sentinel_sensitivity == 'High' else "secondary"):
            st.session_state.sentinel_sensitivity = 'High'
    
    sensitivity_descriptions = {
        'Low': 'Fewer alerts, only trigger on high-confidence stress patterns. Best for avoiding false positives.',
        'Medium': 'Balanced approach. Alerts when multiple signals show stress patterns. Recommended for most users.',
        'High': 'More frequent alerts. Catches early subtle patterns. May have more false positives.'
    }
    
    st.info(f"**Current setting: {st.session_state.sentinel_sensitivity}** - {sensitivity_descriptions[st.session_state.sentinel_sensitivity]}")
    
    # ==========================================
    # ALERT HISTORY
    # ==========================================
    st.markdown("### ⏱️ Alert History")
    st.markdown("<div style='color: #94a3b8; margin-bottom: 15px;'>Recent passive alerts and your responses</div>", unsafe_allow_html=True)
    
    # Sample alert
    st.markdown("""
    <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="color: #f43f5e; font-weight: 700; font-family: monospace;">2:34:09 PM</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 3px;">HRV drop detected, Elevated ambient noise</div>
        </div>
        <div style="background: #7f1d1d; color: #fca5a5; padding: 6px 12px; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">
            75% risk
        </div>
        <button style="background: transparent; border: 1px solid #475569; color: #94a3b8; padding: 6px 12px; border-radius: 6px; cursor: pointer;">
            Dismissed
        </button>
    </div>
    """, unsafe_allow_html=True)
    
    # Auto-refresh if enabled
    if st.session_state.sentinel_enabled:
        time.sleep(1)
        st.rerun()
