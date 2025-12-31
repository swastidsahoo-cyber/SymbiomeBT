import streamlit as st
import pandas as pd
import numpy as np

# --- SAFE MODE HEADER ---
st.set_page_config(page_title="Symbiome - Safe Mode", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
.stApp { background-color: #0f172a; color: white; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ Symbiome: Recovery Mode")
st.warning("The application encountered a critical startup error. We have entered Safe Mode to protect your data.")
st.info("System diagnostics are running. Please wait while we restore functionality.")

# --- DIAGNOSTICS ---
st.subheader("System Status")
col1, col2, col3 = st.columns(3)
col1.metric("Streamlit Core", "Active", "OK")
col2.metric("Data Engine", "Standby", "Checking...")
col3.metric("Sensor Array", "Disabled", "OFF")

# --- ATTEMPT DATA LOAD ---
st.markdown("---")
st.write("Attempting to reconnect modules...")

try:
    import plotly.graph_objects as go
    st.success("✅ Plotly Graphing Engine: Connected")
except ImportError as e:
    st.error(f"❌ Plotly Error: {e}")

try:
    from data_engine import data_engine
    if data_engine:
        st.success("✅ Data Engine: Connected")
        st.write(f"Live Data Probe: {data_engine.get_live_data()}")
    else:
        st.warning("⚠️ Data Engine: Loaded but inactive (SensorManager missing)")
except Exception as e:
    st.error(f"❌ Data Engine Critical Failure: {e}")

# --- RE-INJECT ORIGINAL APP CONTENT BUTTON ---
if st.button("🔄 Attempt Full System Restore"):
    st.write("Please ask the AI Assistant to re-deploy the full 'app.py' now that diagnostics are complete.")
