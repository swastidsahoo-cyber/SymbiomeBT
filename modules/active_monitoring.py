import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
from .sensor_manager import sensor_manager

def render_active_monitoring_page():
    """
    Real-time facial analysis page.
    Connects to SensorManager (MediaPipe backend) and visualizes data.
    """
    st.markdown('<div style="text-align: center; margin-bottom: 20px;"><h2 style="background: linear-gradient(90deg, #2dd4bf, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">Active Facial Analysis</h2><p style="color: #94a3b8;">Real-time physiological estimation via webcam photoplethysmography & expression analysis</p></div>', unsafe_allow_html=True)

    # Check/Set Sensor Strategy
    if sensor_manager.strategy != "WEBCAM":
        sensor_manager.set_strategy("WEBCAM")
        # Give it a moment to init
        time.sleep(0.5)

    # Layout: Video Feed | Real-time Metrics
    col_video, col_metrics = st.columns([1.5, 1])

    with col_video:
        st.markdown('<div style="background: #0f172a; border-radius: 16px; padding: 10px; border: 1px solid #1e293b; text-align: center;">', unsafe_allow_html=True)
        video_placeholder = st.empty()
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Controls
        c1, c2 = st.columns(2)
        with c1:
            if st.button("⏹ Stop Monitoring", use_container_width=True, type="secondary"):
                sensor_manager.set_strategy("SIMULATION")
                st.session_state.page = "Dashboard"
                st.rerun()
        with c2:
            st.markdown('<div style="text-align: right; color: #64748b; font-size: 0.8rem; padding-top: 10px;">PROCESSING: 30 FPS</div>', unsafe_allow_html=True)

    with col_metrics:
        # Metrics Placeholders
        p_stress = st.empty()
        p_hr = st.empty()
        p_metrics = st.empty()
        
    # Stats history for charting (local to this run loop)
    # Note: efficient charting in loop is tricky, we'll use limited deque if needed or just live values
    
    # Loop for Real-Time UI
    # We use a loop here because we want high refresh rate for video
    # Streamlit refresh loop
    
    # Run for X iterations or until stop
    # In Streamlit Cloud, active loops can be tricky but st.empty works well
    
    run_monitoring = True
    
    while run_monitoring:
        # 1. Get Frame
        frame = sensor_manager.get_latest_frame()
        readings = sensor_manager.get_readings()
        
        # 2. Update Video
        if frame is not None:
            video_placeholder.image(frame, channels="RGB", use_container_width=True, caption="Live Analysis Feed")
        else:
            video_placeholder.info("Initializing Camera Source... Please allow permission.")
        
        # 3. Update Metrics
        # Stress Score (Gauge style visual)
        stress_val = int(readings['facial_stress'])
        stress_color = "#10b981" if stress_val < 30 else "#f59e0b" if stress_val < 60 else "#ef4444"
        
        p_stress.markdown(f"""
        <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8)); border-radius: 12px; padding: 20px; border: 1px solid {stress_color}; box-shadow: 0 0 20px {stress_color}40; margin-bottom: 20px;">
            <div style="font-size: 0.85rem; color: #94a3b8; letter-spacing: 1px;">REAL-TIME STRESS</div>
            <div style="font-size: 3.5rem; font-weight: 800; color: {stress_color}; line-height: 1.1;">{stress_val}</div>
            <div style="font-size: 1rem; color: {stress_color}; font-weight: 600;">{readings['emotion'].upper()}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # HR & HRV
        p_hr.markdown(f"""
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
            <div style="background: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="color: #f43f5e; font-size: 1.5rem;">♥ {int(readings['hr'])}</div>
                <div style="color: #faa7b8; font-size: 0.8rem;">HEART RATE</div>
            </div>
            <div style="background: rgba(30, 41, 59, 0.5); padding: 15px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.1);">
                <div style="color: #2dd4bf; font-size: 1.5rem;">⚡ {int(readings['hrv'])}</div>
                <div style="color: #99f6e4; font-size: 0.8rem;">HRV (ms)</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Secondary Metrics
        p_metrics.markdown(f"""
        <div style="background: rgba(15, 23, 42, 0.5); border-radius: 12px; padding: 15px;">
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; margin-bottom: 8px;">
                <span style="color: #cbd5e1;">🌡️ Facial Temp</span>
                <span style="color: #cbd5e1; font-weight:bold;">{readings['temp']:.1f}°C</span>
            </div>
            <div style="display: flex; justify-content: space-between; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 8px; margin-bottom: 8px;">
                <span style="color: #cbd5e1;">👁️ Blink Rate</span>
                <span style="color: #cbd5e1; font-weight:bold;">{int(readings['blink_rate'])} bpm</span>
            </div>
            <div style="display: flex; justify-content: space-between;">
                <span style="color: #cbd5e1;">📡 Signal Quality</span>
                <span style="color: #a78bfa; font-weight:bold;">{int(readings['confidence'])}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # 4. Loop Control
        time.sleep(0.05) # ~20 FPS refresh limit
