import streamlit as st
import plotly.graph_objects as go
import random
import time
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==========================================
# PASSIVE SENTINEL - COMPLETE IMPLEMENTATION
# ==========================================

class PassiveSentinelEngine:
    """
    Digital Twin-based stress prediction engine.
    Simulates passive data collection from device sensors and behavioral patterns.
    """
    
    def __init__(self):
        # Initialize session state for Passive Sentinel
        if 'sentinel_enabled' not in st.session_state:
            st.session_state.sentinel_enabled = False
        
        if 'sentinel_sensitivity' not in st.session_state:
            st.session_state.sentinel_sensitivity = 'Medium'
            
        if 'sensor_permissions' not in st.session_state:
            st.session_state.sensor_permissions = {
                'camera_ppg': True,
                'microphone': True,
                'motion': True,
                'notifications': True
            }
        
        if 'stress_probability' not in st.session_state:
            st.session_state.stress_probability = 15.0
            
        if 'probability_history' not in st.session_state:
            st.session_state.probability_history = [15.0] * 60
            
        if 'alert_history' not in st.session_state:
            st.session_state.alert_history = []
            
        if 'baseline_learned' not in st.session_state:
            # Digital Twin Baseline
            st.session_state.baseline_learned = True
            st.session_state.baseline = {
                'typing_variability': 45,  # ms
                'notification_freq': 8,     # per hour
                'ambient_noise': 35,        # dB
                'screen_brightness': 60,    # %
                'motion_level': 20,         # arbitrary units
                'hrv_baseline': 65          # ms
            }
    
    def update_simulation(self):
        """Simulates real-time passive data collection and stress prediction."""
        
        if not st.session_state.sentinel_enabled:
            return None
        
        # Simulate sensor readings with realistic variation
        current_readings = {
            'typing_variability': st.session_state.baseline['typing_variability'] + random.uniform(-15, 35),
            'notification_freq': st.session_state.baseline['notification_freq'] + random.uniform(-3, 12),
            'ambient_noise': st.session_state.baseline['ambient_noise'] + random.uniform(-10, 25),
            'screen_brightness': st.session_state.baseline['screen_brightness'] + random.uniform(-20, 20),
            'motion_level': st.session_state.baseline['motion_level'] + random.uniform(-10, 15),
            'hrv_current': st.session_state.baseline['hrv_baseline'] + random.uniform(-20, 10)
        }
        
        # Calculate deviations (in standard deviations σ)
        deviations = {}
        contributing_factors = []
        deviation_score = 0
        
        # Typing variability
        if current_readings['typing_variability'] > st.session_state.baseline['typing_variability'] * 1.2:
            dev_pct = int(((current_readings['typing_variability'] - st.session_state.baseline['typing_variability']) / st.session_state.baseline['typing_variability']) * 100)
            contributing_factors.append({
                'name': 'Typing Variability',
                'value': f'↑ {dev_pct}%',
                'description': 'Erratic keystroke timing detected'
            })
            deviation_score += 25
        
        # Notification frequency
        if current_readings['notification_freq'] > st.session_state.baseline['notification_freq'] * 1.5:
            contributing_factors.append({
                'name': 'Notification Flood',
                'value': 'High',
                'description': 'Frequent interruptions detected'
            })
            deviation_score += 20
        
        # Ambient noise
        if current_readings['ambient_noise'] > 55:
            contributing_factors.append({
                'name': 'Environmental Noise',
                'value': f"{int(current_readings['ambient_noise'])} dB",
                'description': 'Loud environment detected'
            })
            deviation_score += 15
        
        # HRV drop
        if current_readings['hrv_current'] < st.session_state.baseline['hrv_baseline'] * 0.85:
            contributing_factors.append({
                'name': 'HRV Drop Detected',
                'value': '↓ 15%',
                'description': 'Reduced heart rate variability'
            })
            deviation_score += 30
        
        # Screen time spike
        if random.random() > 0.7:
            contributing_factors.append({
                'name': 'Screen Time Spike',
                'value': '↑ 40%',
                'description': 'Extended screen exposure'
            })
            deviation_score += 10
        
        # Adjust sensitivity
        sensitivity_multipliers = {'Low': 0.7, 'Medium': 1.0, 'High': 1.3}
        multiplier = sensitivity_multipliers[st.session_state.sentinel_sensitivity]
        
        # Calculate stress probability (0-100%)
        target_probability = min(99, max(5, deviation_score * multiplier + random.uniform(-5, 10)))
        
        # Smooth transition (exponential moving average)
        st.session_state.stress_probability = (st.session_state.stress_probability * 0.7) + (target_probability * 0.3)
        
        # Update history
        st.session_state.probability_history.append(st.session_state.stress_probability)
        if len(st.session_state.probability_history) > 60:
            st.session_state.probability_history.pop(0)
        
        # Determine status
        prob = st.session_state.stress_probability
        if prob >= 75:
            status = 'Imminent'
            status_color = '#ef4444'
            status_message = f'High probability of stress escalation in the next 15 minutes'
        elif prob >= 50:
            status = 'Rising'
            status_color = '#f59e0b'
            status_message = 'Early stress indicators detected — monitor closely'
        else:
            status = 'Stable'
            status_color = '#10b981'
            status_message = 'No elevated stress patterns detected'
        
        # Trigger alert if threshold crossed
        if prob >= 70 and len(st.session_state.alert_history) == 0:
            self.trigger_alert(prob, contributing_factors)
        
        return {
            'status': status,
            'status_color': status_color,
            'status_message': status_message,
            'probability': prob,
            'factors': contributing_factors
        }
    
    def trigger_alert(self, probability, factors):
        """Logs an alert event."""
        alert = {
            'time': datetime.now().strftime('%I:%M %p'),
            'risk_level': f'{int(probability)}% risk',
            'factors': ', '.join([f['name'] for f in factors[:2]])
        }
        st.session_state.alert_history.insert(0, alert)
        if len(st.session_state.alert_history) > 5:
            st.session_state.alert_history.pop()


def render_passive_sentinel():
    """Renders the complete Passive Sentinel UI matching the design specifications."""
    
    engine = PassiveSentinelEngine()
    
    # Header
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 15px; margin-bottom: 30px;">
        <div style="font-size: 2.5rem;">🔔</div>
        <div>
            <div style="font-size: 2rem; font-weight: 700; color: #c084fc;">Passive Stress Sentinel</div>
            <div style="color: #94a3b8; font-size: 1rem;">Always-on monitoring that alerts you before stress peaks—no active input required</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # ==========================================
    # MONITORING TOGGLE
    # ==========================================
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid #1e293b; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: white; font-weight: 600; font-size: 1.1rem;">🟣 Passive Monitoring Active</div>
                <div style="color: #94a3b8; font-size: 0.9rem;">Analyzing passive signals in real-time</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    col_toggle1, col_toggle2 = st.columns([3, 1])
    with col_toggle2:
        st.session_state.sentinel_enabled = st.toggle('ON', value=st.session_state.sentinel_enabled, key='sentinel_toggle')
    
    # ==========================================
    # EARLY STRESS ALERT (if triggered)
    # ==========================================
    data = engine.update_simulation()
    
    if data and data['probability'] >= 70:
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, #7f1d1d 0%, #991b1b 100%); border: 2px solid #ef4444; border-radius: 12px; padding: 20px; margin-bottom: 20px;">
            <div style="display: flex; align-items: start; gap: 15px;">
                <div style="font-size: 2rem;">⚠️</div>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 700; font-size: 1.2rem; margin-bottom: 5px;">Early Stress Signs Detected</div>
                    <div style="color: #fca5a5; font-size: 0.95rem; margin-bottom: 15px;">
                        Symbiome noticed patterns that typically precede stress. A 60-second breathing exercise might help.
                    </div>
                    <div style="display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 15px;">
                        {' '.join([f'<span style="background: rgba(0,0,0,0.3); padding: 4px 10px; border-radius: 6px; font-size: 0.85rem; color: #fca5a5;">{f["name"]}</span>' for f in data['factors'][:3]])}
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
    
    # ==========================================
    # MAIN CONTENT AREA
    # ==========================================
    
    if not st.session_state.sentinel_enabled:
        # OFF STATE
        st.markdown("""
        <div style="text-align: center; padding: 80px 20px; background: rgba(15, 23, 42, 0.4); border-radius: 16px; border: 1px solid #1e293b;">
            <div style="font-size: 4rem; margin-bottom: 20px; opacity: 0.5;">🔕</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white; margin-bottom: 10px;">Passive Monitoring is Off</div>
            <div style="color: #94a3b8; max-width: 500px; margin: 0 auto; line-height: 1.6;">
                Enable passive monitoring to receive early stress warnings without having to actively provide data. 
                The system analyzes device sensors and behavioral patterns to detect stress before you consciously feel it.
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        
        # Show sensor permissions even when off
        render_sensor_permissions()
        render_sensitivity_controls()
        render_alert_history()
        
    else:
        # ON STATE - Show live monitoring
        col_left, col_right = st.columns([1, 1.5], gap="large")
        
        with col_left:
            # REAL-TIME STRESS PROBABILITY
            st.markdown(f"""
            <div style="background: rgba(15, 23, 42, 0.6); border: 1px solid {data['status_color']}40; border-radius: 16px; padding: 25px; text-align: center;">
                <div style="font-size: 0.85rem; letter-spacing: 2px; text-transform: uppercase; color: #64748b; margin-bottom: 15px;">
                    ⚡ Real-Time Stress Probability
                </div>
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 20px;">
                    Live assessment based on passive signals (updates every second)
                </div>
                
                <!-- Circular Probability Meter -->
                <div style="position: relative; width: 180px; height: 180px; margin: 20px auto;">
                    <svg width="180" height="180" style="transform: rotate(-90deg);">
                        <circle cx="90" cy="90" r="70" fill="none" stroke="#1e293b" stroke-width="12"/>
                        <circle cx="90" cy="90" r="70" fill="none" stroke="{data['status_color']}" stroke-width="12"
                                stroke-dasharray="{(data['probability']/100) * 440} 440"
                                stroke-linecap="round"
                                style="filter: drop-shadow(0 0 10px {data['status_color']}80);"/>
                    </svg>
                    <div style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); text-align: center;">
                        <div style="font-size: 3rem; font-weight: 800; color: white; line-height: 1;">{int(data['probability'])}%</div>
                        <div style="font-size: 0.75rem; color: {data['status_color']}; font-weight: 700; margin-top: 5px;">
                            {data['status'].upper()}
                        </div>
                    </div>
                </div>
                
                <div style="margin-top: 25px; padding-top: 20px; border-top: 1px solid #1e293b;">
                    <div style="font-size: 1.3rem; font-weight: 700; color: {data['status_color']}; margin-bottom: 5px;">
                        {data['status']}
                    </div>
                    <div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.4;">
                        {data['status_message']}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col_right:
            # MICRO-TREND TIMELINE
            st.markdown("#### 📉 Stress Probability Micro-Trend (Last 60 min)")
            
            fig = go.Figure()
            x_vals = list(range(len(st.session_state.probability_history)))
            y_vals = st.session_state.probability_history
            
            fig.add_trace(go.Scatter(
                x=x_vals,
                y=y_vals,
                mode='lines',
                fill='tozeroy',
                line=dict(color=data['status_color'], width=3),
                fillcolor=f"rgba({int(data['status_color'][1:3], 16)}, {int(data['status_color'][3:5], 16)}, {int(data['status_color'][5:7], 16)}, 0.2)"
            ))
            
            fig.add_hline(y=50, line_dash="dot", line_color="rgba(148, 163, 184, 0.3)", 
                         annotation_text="Moderate", annotation_position="right")
            fig.add_hline(y=75, line_dash="dot", line_color="rgba(239, 68, 68, 0.5)", 
                         annotation_text="Alert", annotation_position="right")
            
            fig.update_layout(
                height=280,
                margin=dict(l=0, r=0, t=10, b=0),
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(15, 23, 42, 0.6)',
                xaxis=dict(showgrid=False, visible=False),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100], title="Probability %"),
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
            
            # WHAT CHANGED? (Explainability)
            st.markdown("#### 🕵️ What Changed? (Explainability)")
            st.markdown("<div style='color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px;'>Analysis of behavioral and environmental deviations from your Digital Twin baseline.</div>", unsafe_allow_html=True)
            
            if data['factors']:
                for factor in data['factors']:
                    st.markdown(f"""
                    <div style="display: flex; justify-content: space-between; align-items: center; background: #0f172a; border: 1px solid #1e293b; padding: 12px 18px; border-radius: 10px; margin-bottom: 10px;">
                        <div>
                            <div style="color: #e2e8f0; font-weight: 600; font-size: 0.95rem;">{factor['name']}</div>
                            <div style="font-size: 0.8rem; color: #94a3b8;">{factor['description']}</div>
                        </div>
                        <div style="font-family: monospace; font-weight: 700; color: #f43f5e; background: #f43f5e20; padding: 6px 12px; border-radius: 6px;">
                            {factor['value']}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("✓ No significant deviations detected. Your biomarkers are tracking with your baseline.")
        
        # Full-width sections below
        st.markdown("<div style='height: 30px;'></div>", unsafe_allow_html=True)
        render_sensor_permissions()
        render_sensitivity_controls()
        render_alert_history()


def render_sensor_permissions():
    """Renders the sensor permissions panel."""
    st.markdown("### 🛡️ Sensor Permissions")
    st.markdown("<div style='color: #94a3b8; margin-bottom: 15px;'>Control which passive signals are collected (local processing only)</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 1.5rem;">📷</div>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 600;">Camera (PPG)</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Heart rate variability</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.sensor_permissions['camera_ppg'] = st.checkbox('Enable', value=st.session_state.sensor_permissions['camera_ppg'], key='cam_ppg')
        
        st.markdown("""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 1.5rem;">📱</div>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 600;">Motion Sensors</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Agitation & restlessness</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.sensor_permissions['motion'] = st.checkbox('Enable', value=st.session_state.sensor_permissions['motion'], key='motion_sens')
    
    with col2:
        st.markdown("""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 1.5rem;">🎤</div>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 600;">Microphone</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Ambient noise level</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.sensor_permissions['microphone'] = st.checkbox('Enable', value=st.session_state.sensor_permissions['microphone'], key='mic_sens')
        
        st.markdown("""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 12px;">
                <div style="font-size: 1.5rem;">🔔</div>
                <div style="flex: 1;">
                    <div style="color: white; font-weight: 600;">Notification Tracking</div>
                    <div style="font-size: 0.8rem; color: #94a3b8;">Count only, no content</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.sensor_permissions['notifications'] = st.checkbox('Enable', value=st.session_state.sensor_permissions['notifications'], key='notif_track')


def render_sensitivity_controls():
    """Renders alert sensitivity controls."""
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


def render_alert_history():
    """Renders recent alert history."""
    st.markdown("### ⏱️ Alert History")
    st.markdown("<div style='color: #94a3b8; margin-bottom: 15px;'>Recent passive alerts and your responses</div>", unsafe_allow_html=True)
    
    if st.session_state.alert_history:
        for alert in st.session_state.alert_history:
            st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 15px; margin-bottom: 10px; display: flex; justify-content: space-between; align-items: center;">
                <div>
                    <div style="color: #f43f5e; font-weight: 700; font-family: monospace;">{alert['time']}</div>
                    <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 3px;">{alert['factors']}</div>
                </div>
                <div style="background: #7f1d1d; color: #fca5a5; padding: 6px 12px; border-radius: 6px; font-weight: 700; font-size: 0.85rem;">
                    {alert['risk_level']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 10px; padding: 20px; text-align: center; color: #64748b; font-style: italic;">
            No alerts yet. The system is learning your baseline patterns.
        </div>
        """, unsafe_allow_html=True)
    
    # Privacy notice
    with st.expander("🔒 Privacy & Ethical Data Use"):
        st.markdown("""
        **How Passive Sentinel protects your privacy:**
        
        - **Metadata only:** We measure typing *rhythm*, not what you type
        - **Local processing:** All raw sensor data is processed on-device
        - **No recording:** Audio is sampled for decibel level only; no conversations are recorded
        - **No content access:** Notification count only, never reads message content
        - **You are in control:** Pause monitoring or disable specific sensors at any time
        - **Digital Twin:** Your baseline is personal and never shared
        
        **Scientific Foundation:**
        This system uses **Digital Phenotyping** - a research-validated approach used in mental health studies, 
        burnout detection, and cognitive load research. It detects stress through behavioral biomarkers and 
        environmental patterns, not invasive surveillance.
        """)
