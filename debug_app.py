import streamlit as st
import sys
import os
import time

st.set_page_config(page_title="DEBUG MODE", layout="wide")

st.title("🛠️ DEBUGGING MODE")
st.write("If you can see this, Streamlit is working!")

st.write(f"**Current Directory:** `{os.getcwd()}`")
st.write(f"**Python Version:** `{sys.version}`")

st.divider()

st.subheader("1. Testing Sensor Manager Import")
try:
    from modules.sensor_manager import sensor_manager
    st.success("✅ SensorManager Imported Successfully")
    
    st.write(f"**Strategy:** `{sensor_manager.strategy}`")
    
    if st.button("Activate Webcam Mode"):
        sensor_manager.set_strategy("WEBCAM")
        st.success("Strategy set to WEBCAM")
        
    if sensor_manager.strategy == "WEBCAM":
        st.write("Reading Frames...")
        frame = sensor_manager.get_latest_frame()
        if frame is not None:
            st.image(frame, caption="Live Feed")
        else:
            st.warning("No Frame Data")
            
except Exception as e:
    st.error(f"❌ Import Failed: {e}")
    st.exception(e)

st.divider()
st.write("End of Debug Script")
