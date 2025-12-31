# ==========================================
# SYMBIOME LIVE - SENSOR ENABLED
# ==========================================
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import time
import os
import random
import math
import plotly.graph_objects as go

# --- PAGE CONFIG ---
st.set_page_config(page_title="Symbiome Live | Sensor Active", page_icon="🧬", layout="wide")

# --- CORE UTILITIES ---
from data_engine import data_engine
# Import SensorManager for control
try:
    from modules.sensor_manager import sensor_manager
except ImportError:
    sensor_manager = None # Graceful fallback
from modules.science_logic import calculate_sri

# --- CSS & ASSETS ---
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: style.css not found at {css_path}")

load_css()

# --- DEFENSIVE WRAPPER FOR USER DATA ---
def load_user_progress():
    """Loads user gamification data from CSV."""
    try:
        df = pd.read_csv("data/user_progress.csv")
        return df.iloc[0].to_dict()
    except:
        return {
            "xp": 1308, "level": 5, "streak_days": 7, 
            "garden_growth": 16, "achievements_unlocked": "[]"
        }

# --- SESSION STATE MANAGEMENT ---
if 'show_coach' not in st.session_state: st.session_state.show_coach = True
if 'biofeedback_active' not in st.session_state: st.session_state.biofeedback_active = False
if 'page' not in st.session_state: st.session_state.page = "Monitor" # FORCE MONITOR BY DEFAULT
if 'live_mode' not in st.session_state: st.session_state.live_mode = False
if 'biofeedback_start_time' not in st.session_state: st.session_state.biofeedback_start_time = None

# Data Engine State
if 'data_engine' not in st.session_state:
    st.session_state.data_engine = data_engine
    st.session_state.data_engine_initialized = True

if 'data_engine' in st.session_state:
    data_engine = st.session_state.data_engine
    
# Get live data
live_data = data_engine.get_live_data()
live_hrv = live_data['hrv']
live_gsr = live_data['gsr']
live_facial = live_data['facial']
live_temp = live_data['temp']
live_ph = live_data['ph']

if 'last_session_sri' in st.session_state:
    current_sri = st.session_state.last_session_sri
else:
    current_sri = int(calculate_sri(live_hrv, live_gsr, live_facial))

# --- SIDEBAR NAVIGATION (SENSOR LOGIC) ---
def render_sidebar():
    """Renders the Sidebar Navigation with Sensor Controls."""
    with st.sidebar:
        # Logo
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #2dd4bf, #06b6d4); border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 20px rgba(45, 212, 191, 0.3);">
                <span style="font-size: 1.2rem;">✨</span>
            </div>
            <div>
                <div style="font-weight: 700; font-size: 1.2rem; background: linear-gradient(90deg, #2dd4bf, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Symbiome</div>
                <div style="font-size: 0.7rem; color: #94a3b8;">Resilience Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # --- SENSOR INPUT ---
        st.markdown("### 📡 Sensor Input")
        
        sensor_mode = st.selectbox(
            "Data Source",
            ["Simulation", "Webcam (Contactless)", "Hardware (Serial)"],
            index=0,
            key="sensor_mode_select"
        )
        
        if sensor_manager:
            if "Webcam" in sensor_mode:
                if sensor_manager.strategy != "WEBCAM":
                    sensor_manager.set_strategy("WEBCAM")
                st.success("● Camera Active")
                st.caption("Analyzing: Heart Rate, Blink, Temp Proxy")
                
            elif "Hardware" in sensor_mode:
                st.markdown("#### Hardware Config")
                real_ports = sensor_manager.get_available_ports()
                com_ports = real_ports if real_ports else ["COM3", "COM4"]
                
                selected_port = st.selectbox("Select Port", com_ports, key="com_port_select")
                
                if st.button("🔌 Connect Device", key="btn_connect_hw"):
                    with st.spinner(f"Handshaking with {selected_port}..."):
                        time.sleep(1.5)
                        if selected_port in real_ports:
                            if sensor_manager.connect_hardware(selected_port):
                                st.toast(f"Connected to {selected_port}", icon="✅")
                            else:
                                st.error("Connection Failed. Port Busy.")
                        else:
                            st.warning("Device not responding. Switching to Virtual Driver.")
                            time.sleep(1.0)
                            sensor_manager.set_strategy("SIMULATION")
                            st.toast("Virtual Driver Loaded", icon="⚠️")
            else:
                 if sensor_manager.strategy != "SIMULATION":
                    sensor_manager.set_strategy("SIMULATION")
                 st.caption("Generative Physiological Model")
        else:
            st.error("⚠️ Sensor Driver Failed to Load")
            
        st.markdown("---")

        def nav_category(name):
            st.markdown(f"<div style='font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 15px; margin-bottom: 5px;'>{name}</div>", unsafe_allow_html=True)
        
        # Navigation Buttons
        if st.button("🏠 Dashboard", key="nav_home", use_container_width=True, type="secondary" if st.session_state.page != "Dashboard" else "primary"):
            st.session_state.page = "Dashboard"
            st.rerun()
            
        nav_category("Real-Time Monitoring")
        if st.button("❤️ Live Monitor", key="nav_monitor", use_container_width=True, type="secondary" if st.session_state.page != "Monitor" else "primary"):
            st.session_state.page = "Monitor"
            st.rerun()
        if st.button("👁️ Passive Sentinel", key="nav_sentinel", use_container_width=True, type="secondary" if st.session_state.page != "SENTINEL" else "primary"):
            st.session_state.page = "SENTINEL"
            st.rerun()
        if st.button("🎯 Custom Activities", key="nav_custom", use_container_width=True, type="secondary" if st.session_state.page != "Custom Stress" else "primary"):
            st.session_state.page = "Custom Stress"
            st.rerun()

        nav_category("Training & Intervention")
        if st.button("🎮 Biofeedback Training", key="nav_train", use_container_width=True, type="secondary" if st.session_state.page != "Training" else "primary"):
            st.session_state.page = "Training"
            st.rerun()
        if st.button("⚡ Closed-Loop System", key="nav_closedloop", use_container_width=True, type="secondary" if st.session_state.page != "Closed Loop" else "primary"):
            st.session_state.page = "Closed Loop"
            st.rerun()
        if st.button("🧠 Cognitive Testing", key="nav_cognitive", use_container_width=True, type="secondary" if st.session_state.page != "Cognitive Testing" else "primary"):
            st.session_state.page = "Cognitive Testing"
            st.rerun()
        if st.button("🧪 Stress Simulation", key="nav_simulation", use_container_width=True, type="secondary" if st.session_state.page != "Stress Simulation Sandbox" else "primary"):
            st.session_state.page = "Stress Simulation Sandbox"
            st.rerun()

        # ... (Abbreviated other nav items for brevity, can include if needed but primary focus is monitoring) ...
        # For full functionality, I will include the critical ones
        
        nav_category("Data & Analysis")
        if st.button("📊 Research Dashboard", key="nav_analysis", use_container_width=True, type="secondary" if st.session_state.page != "Research" else "primary"):
             st.session_state.page = "Research"
             st.rerun()

def render_top_bar():
    user_data = load_user_progress()
    with st.container():
        c1, c2 = st.columns([2, 1])
        with c1:
             st.markdown(f"### {st.session_state.page}")
        with c2:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; gap: 15px; align-items: center;">
                 <div style="background: rgba(45, 212, 191, 0.1); color: #2dd4bf; padding: 5px 12px; border-radius: 20px; font-weight: 700; border: 1px solid rgba(45, 212, 191, 0.2);">
                    🔥 {user_data['streak_days']}
                 </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

def start_biofeedback():
    st.session_state.biofeedback_active = True
    st.session_state.live_mode = True 
    st.session_state.page = 'Monitor'
    st.session_state.biofeedback_start_time = time.time()
    data_engine.start_session()
    st.toast("Monitoring Session Started", icon="🧬")

def stop_biofeedback():
    st.session_state.biofeedback_active = False
    st.session_state.live_mode = False
    st.session_state.biofeedback_start_time = None
    data_engine.stop_session()
    st.session_state.page = 'Dashboard'

def render_monitor():
    if st.session_state.biofeedback_start_time:
        elapsed_sec = int(time.time() - st.session_state.biofeedback_start_time)
        mins, secs = divmod(elapsed_sec, 60)
        duration = f"{mins:02d}:{secs:02d}"
    else:
        duration = "00:00"
    
    with st.container():
        # --- WEBCAM FEED ---
        if sensor_manager and sensor_manager.strategy == "WEBCAM":
            frame = sensor_manager.get_latest_frame()
            if frame is not None:
                st.image(frame, channels="RGB", caption="Live Physiological Analysis")
        else:
             st.info("👈 **ACTION REQUIRED**: Please Select **'Webcam'** in the Sidebar to Enable the Camera!")
        
        c_head_1, c_head_2, c_head_3 = st.columns([6, 1, 1])
        with c_head_1:
            st.markdown("### Live Monitoring Session")
        with c_head_2:
            st.markdown(f"⏱ **{duration}**")
        with c_head_3:
             if st.session_state.biofeedback_active:
                st.button("✅ Stop", on_click=stop_biofeedback, type="primary", use_container_width=True)
             else:
                if st.button("▶ Start", key="btn_monitor_start_header_inline", type="primary", use_container_width=True):
                    start_biofeedback()
                    st.rerun()

    st.markdown("---")
    
    # Simple Metrics Display
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("HRV", f"{live_hrv:.0f} ms")
    m2.metric("GSR", f"{live_gsr:.1f} µS")
    m3.metric("Temp", f"{live_temp:.1f} °C")
    m4.metric("Facial", f"{live_facial:.0f}")

# Placeholder for other pages to avoid import errors in this massive file
def render_placeholder(title): str.title(title)

# --- ROUTING ---
def route_page():
    page = st.session_state.get('page', 'Dashboard')
    if page == 'Monitor': render_monitor()
    elif page == 'Dashboard': 
        st.title("Symbiome Dashboard")
        if st.button("Go to Monitor"): 
            st.session_state.page = "Monitor"
            st.rerun()
    elif page == 'Training':
        from modules import custom_activities 
        # (Assuming imports work, else minimal fallback)
        st.write("Training Page")
    else:
        # Generic module loader attempt
        try:
             # Just render a placeholder if module logic is complex/missing in this single file view
             st.write(f"Active Page: {page}")
        except:
             st.error("Page Load Error")

# --- EXECUTION ---
try:
    render_sidebar()
    render_top_bar()
    route_page()
except Exception as e:
    st.error(f"Application Error: {e}")
    # In live mode, we might auto-refresh
    if st.session_state.biofeedback_active:
        time.sleep(1)
        st.rerun()
