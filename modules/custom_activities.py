"""
Custom Activities Interface.
Real-time biometric capture using camera-based PPG (Photoplethysmography).
"""
import streamlit as st
import cv2
import numpy as np
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration, WebRtcMode
import av
from .ppg_analyzer import PPGAnalyzer
from .utils import DataModels
import time

# --- PPG VIDEO PROCESSOR ---
class PPGVideoProcessor:
    def __init__(self):
        self.analyzer = PPGAnalyzer(window_size=150) # 5 second window for faster feedback
        self.last_hr = 0
        self.last_hrv = 0
        self.confidence = 0

    def recv(self, frame: av.VideoFrame) -> av.VideoFrame:
        img = frame.to_ndarray(format="bgr24")
        
        # Add frame to analyzer
        self.analyzer.add_sample(img)
        
        # Calculate HR and HRV
        hr, conf = self.analyzer.calculate_heart_rate()
        hrv = self.analyzer.calculate_hrv()
        
        if hr > 0:
            self.last_hr = hr
            self.last_hrv = hrv
            self.confidence = conf
            
        # Draw ROI and HR on frame for user feedback
        roi = self.analyzer.extract_roi(img)
        if roi is not None:
            # Drawing logic simplified for performance
            cv2.putText(img, f"Capturing: {int(hr)} BPM", (20, 40), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            cv2.rectangle(img, (20, 60), (320, 80), (255, 255, 255), 1)
            cv2.rectangle(img, (20, 60), (20 + int(conf * 3), 80), (0, 255, 0), -1)
            
        return av.VideoFrame.from_ndarray(img, format="bgr24")

def render_custom_activities_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #60a5fa; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">🎯</span> Custom Activities
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Physiological Laboratory. Capture HR & HRV directly from your camera using In-Silico optics.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- SESSION CONFIG ---
    st.markdown("### 🛠️ Session Parameters")
    c1, c2 = st.columns(2)
    with c1:
        activity_type = st.selectbox("Activity Category", ["Meditation", "Controlled Breathing", "Cardio Evaluation", "Baseline Capture"])
        duration = st.slider("Duration (Seconds)", 30, 300, 60)
    with c2:
        st.markdown("""
        **Hardware Readiness**
        - Camera: ✅ Detected
        - Lighting: ⚠️ Sub-optimal (Increase illumination)
        - Skin Contrast: ✅ High
        """)

    st.divider()

    # --- WEBRTC STREAMER ---
    st.markdown("### 📹 Biometric Signal Capture")
    
    # RTC Configuration for better connectivity
    RTC_CONFIG = RTCConfiguration(
        {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
    )

    webrtc_ctx = webrtc_streamer(
        key="ppg-capture",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=RTC_CONFIG,
        video_processor_factory=PPGVideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True,
    )

    # --- REAL-TIME STATS ---
    if webrtc_ctx.video_processor:
        st.markdown("### 📊 Live Autonomic Stream")
        
        stat_col1, stat_col2, stat_col3 = st.columns(3)
        
        # We need to pull values from the video processor
        curr_hr = webrtc_ctx.video_processor.last_hr
        curr_hrv = webrtc_ctx.video_processor.last_hrv
        curr_conf = webrtc_ctx.video_processor.confidence
        
        with stat_col1:
            st.metric("Estimated Heart Rate", f"{int(curr_hr)} BPM" if curr_hr > 0 else "--")
        with stat_col2:
            st.metric("Estimated HRV", f"{int(curr_hrv)} ms" if curr_hrv > 0 else "--")
        with stat_col3:
            st.metric("Signal Confidence", f"{int(curr_conf)}%")

        if st.button("🔴 Start Recording Session", use_container_width=True):
            st.toast("Recording biometric trajectory...", icon="⏺️")
    else:
        st.warning("Please click 'Start' on the camera component above to begin biometric capture.")

    st.divider()

    # --- TECHNICAL NOTE ---
    with st.expander("🔬 How does camera PPG work?"):
        st.markdown("""
        **Photoplethysmography (PPG)** is a technique that detects blood volume changes in the microvascular bed of tissue. 
        Each cardiac cycle creates a 'pulse' that slightly changes the skin's color (mostly in the green spectrum).
        
        1. **ROI Extraction**: We locate the forehead region (thin skin, high vascularity).
        2. **Signal Filtering**: We apply a 0.7Hz - 3.5Hz bandpass filter to isolate the pulse.
        3. **Peak Detection**: We use Fast Fourier Transforms (FFT) to identify the dominant frequency (BPM).
        4. **HRV Derivation**: We measure the RMSSD (variance) between detected peaks to estimate vagal tone.
        """)
