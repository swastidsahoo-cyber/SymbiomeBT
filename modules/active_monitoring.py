import streamlit as st
import cv2
import numpy as np
import av
import time
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from .sensor_manager import sensor_manager

# --- WEBRTC PROCESSOR ---
class FacialAnalysisProcessor(VideoTransformerBase):
    def __init__(self):
        self.frame_count = 0
        self.last_update = time.time()
        
    def transform(self, frame):
        # 1. Convert to OpenCV format
        img = frame.to_ndarray(format="bgr24")
        
        # 2. Pass to SensorManager for analysis (Thread-safe call ideally, but direct here for simplicity)
        # We inject the frame into the sensor manager's pipeline
        sensor_manager.process_external_frame(img)
        
        # 3. Get latest metrics to overlay
        readings = sensor_manager.get_readings()
        
        # 4. Draw Overlay
        # Pulse Graph (Simulated visual for now)
        h, w = img.shape[:2]
        
        # Draw Face Box (Mock if no face found, or real if SensorManager found one)
        # For efficiency, we just draw the HUD
        
        # HUD: Heart Rate
        cv2.rectangle(img, (10, 10), (200, 110), (0, 0, 0), -1)
        cv2.rectangle(img, (10, 10), (200, 110), (0, 255, 0), 1)
        
        cv2.putText(img, f"HR: {int(readings['hr'])} bpm", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.putText(img, f"HRV: {int(readings['hrv'])} ms", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.putText(img, f"Stress: {int(readings['facial_stress'])}%", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        
        return img

def render_active_monitoring_page():
    """
    Real-time facial analysis page using WebRTC.
    Works on both Local and Cloud deployments.
    """
    st.markdown('<div style="text-align: center; margin-bottom: 20px;"><h2 style="background: linear-gradient(90deg, #2dd4bf, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800;">Active Facial Analysis</h2><p style="color: #94a3b8;">Real-time physiological estimation via browser-based camera processing</p></div>', unsafe_allow_html=True)

    # Main Layout
    col_video, col_stats = st.columns([1.5, 1])
    
    with col_video:
        st.info("💡 Click 'START' below to activate your camera. Allow browser permissions.")
        
        # WEBRTC STREAMER
        # key="active-monitor" ensures it persists
        # RTC Configuration is moving to STUN servers to bypass cloud firewalls
        rtc_configuration = {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
        
        ctx = webrtc_streamer(
            key="active-monitor",
            video_processor_factory=FacialAnalysisProcessor,
            rtc_configuration=rtc_configuration,
            media_stream_constraints={"video": True, "audio": False},
            async_processing=True
        )
        
    with col_metrics:
        st.markdown("### 📊 Live Metrics")
        
        # Live Stats Placeholders
        # We need to pull data from SensorManager which is being updated by the video processor
        p_stress = st.empty()
        p_details = st.empty()
        
        if sensor_manager.strategy == "HARDWARE":
             st.warning("⚠️ HARDWARE MODE: Requires running app LOCALLY (localhost). Cloud cannot access your USB ports.")
        
        # Render Loop (only runs if stream is active)
        # We use a placeholder loop that updates ONLY the metrics, not the whole page
        if ctx.state.playing:
            while ctx.state.playing:
                # Get latest readings
                readings = sensor_manager.get_readings()
                
                # Stress Display
                stress_val = int(readings['facial_stress'])
                stress_color = "#10b981" if stress_val < 30 else "#f59e0b" if stress_val < 60 else "#ef4444"
                
                p_stress.markdown(f"""
                <div style="background: linear-gradient(135deg, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8)); border-radius: 12px; padding: 20px; border: 1px solid {stress_color}; box-shadow: 0 0 20px {stress_color}40; margin-bottom: 20px;">
                    <div style="font-size: 0.85rem; color: #94a3b8; letter-spacing: 1px;">REAL-TIME STRESS</div>
                    <div style="font-size: 3.5rem; font-weight: 800; color: {stress_color}; line-height: 1.1;">{stress_val}</div>
                    <div style="font-size: 1rem; color: {stress_color}; font-weight: 600;">{readings['emotion'].upper()}</div>
                </div>
                """, unsafe_allow_html=True)
                
                p_details.markdown(f"""
                <div style="background: rgba(15, 23, 42, 0.5); border-radius: 12px; padding: 15px; border: 1px solid rgba(255,255,255,0.1);">
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #cbd5e1;">💓 Heart Rate</span>
                        <span style="color: #f43f5e; font-weight:bold; font-size: 1.2rem;">{int(readings['hr'])} <span style="font-size:0.8rem">bpm</span></span>
                    </div>
                    <div style="display: flex; justify-content: space-between; padding: 10px 0; border-bottom: 1px solid rgba(255,255,255,0.05);">
                        <span style="color: #cbd5e1;">⚡ HRV</span>
                        <span style="color: #2dd4bf; font-weight:bold; font-size: 1.2rem;">{int(readings['hrv'])} <span style="font-size:0.8rem">ms</span></span>
                    </div>
                     <div style="display: flex; justify-content: space-between; padding: 10px 0;">
                        <span style="color: #cbd5e1;">🌡️ Facial Temp</span>
                        <span style="color: #fbbf24; font-weight:bold; font-size: 1.2rem;">{readings['temp']:.1f}°C</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Update rate (Keep reasonable to avoid UI lag)
                time.sleep(0.1)
        else:
            st.info("Waiting for video stream...")
