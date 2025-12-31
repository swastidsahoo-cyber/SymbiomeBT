import streamlit as st
import os
import sys
import time

# --- 1. FORCE VISIBLE HEADER ---
st.set_page_config(page_title="EMERGENCY DIAGNOSTIC", page_icon="🚨", layout="wide")
st.markdown("""
<style>
    .big-alert {
        background-color: #ff4b4b;
        color: white;
        padding: 30px;
        border-radius: 10px;
        text-align: center;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
    }
    .path-box {
        background-color: #1e1e1e;
        color: #00ff00;
        font-family: monospace;
        padding: 15px;
        border-radius: 5px;
        margin: 10px 0;
    }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="big-alert">🚨 IF YOU SEE THIS, I AM WORKING! 🚨</div>', unsafe_allow_html=True)

# --- 2. PRINT EXECUTION CONTEXT ---
st.write("### 📂 WHERE AM I RUNNING?")
current_path = os.getcwd()
st.code(current_path, language="bash")
st.write(f"**Script Location:** `{__file__}`")

# --- 3. DIRECT CAMERA TEST (INLINE LOGIC) ---
st.divider()
st.write("### 📷 DIRECT CAMERA TEST")

if st.checkbox("✅ ACTIVATE CAMERA NOW", value=True):
    try:
        # Try importing dependencies dynamically
        import cv2
        import numpy as np
        
        # Open Camera directly (Bypass SensorManager for test)
        cap = cv2.VideoCapture(0)
        
        if not cap.isOpened():
            st.error("❌ Camera Hardware NOT Found (cv2.VideoCapture returned False)")
        else:
            ret, frame = cap.read()
            if ret:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                st.image(frame_rgb, caption="Direct Feed Success!", width=400)
                st.success("✅ Camera Hardware IS Functioning!")
            else:
                st.warning("⚠️ Camera Found but returned no frame.")
            cap.release()
            
    except ImportError:
        st.error("❌ OpenCV (cv2) not installed.")
    except Exception as e:
        st.error(f"❌ Camera Crash: {e}")

# --- 4. ATTEMPT TO LOAD SENSOR MANAGER ---
st.divider()
st.write("### 🧩 MODULE CONNECTION TEST")
try:
    from modules.sensor_manager import sensor_manager
    st.success(f"✅ SensorManager Module Found! Strategy: {sensor_manager.strategy}")
    
    if st.button("Enable SensorManager Webcam Mode"):
        sensor_manager.set_strategy("WEBCAM")
        st.rerun()

    if sensor_manager.strategy == "WEBCAM":
        f = sensor_manager.get_latest_frame()
        if f is not None:
             st.image(f, caption="SensorManager Feed (Processed)", width=400)
        else:
             st.write("Waiting for frames...")
             time.sleep(1)
             st.rerun()
             
except ImportError as e:
    st.error(f"❌ Could not import SensorManager: {e}")
    st.info("This means 'modules/sensor_manager.py' is missing or broken in this folder.")
except Exception as e:
    st.error(f"❌ SensorManager Error: {e}")
