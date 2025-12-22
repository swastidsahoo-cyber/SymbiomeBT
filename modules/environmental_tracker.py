"""
Environmental Tracker Interface.
Correlates external stressors (noise, light, temperature) with physiological resilience.
"""
import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np

def render_environmental_tracker_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #10b981; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">🌍</span> Environmental Tracker
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Quantifying the 'Exposome'. How your surroundings dictate your autonomic state.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- SENSOR LOGGING ---
    st.markdown("### 🎙️ Ambient Signal Capture")
    
    col1, col2 = st.columns(2)
    with col1:
        noise = st.slider("Ambient Noise (dB)", 30, 110, 55)
        temp = st.slider("Temperature (°C)", 15, 35, 22)
    with col2:
        light = st.slider("Lux Level (lm)", 0, 2000, 400)
        co2 = st.slider("CO2 Levels (ppm)", 400, 2000, 600)

    if st.button("🛰️ Sync Environmental Data", use_container_width=True):
        st.success(f"Snapshot Captured at {pd.Timestamp.now().strftime('%H:%M:%S')}")
        st.info("Cross-referencing with HRV baseline...")

    st.divider()

    # --- CORRELATION ANALYSIS ---
    st.markdown("### 🧬 Environmental Correlation Matrix")
    
    # Mock correlation data
    data = {
        'Factor': ['Noise', 'Blue Light', 'Temperature', 'CO2', 'Humidity'],
        'SRI Correlation': [-0.65, -0.45, -0.12, -0.25, 0.05],
        'Vagal Impact': ['High Suppression', 'Moderate Suppression', 'Neutral', 'Low Suppression', 'Neutral']
    }
    df = pd.DataFrame(data)
    
    fig = px.bar(
        df, x='SRI Correlation', y='Factor', 
        orientation='h',
        color='SRI Correlation',
        color_continuous_scale='RdYlGn',
        range_color=[-1, 1],
        title="Impact of External Factors on Resilience"
    )
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        coloraxis_showscale=False
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- INSIGHTS ---
    st.markdown("### 💡 Exposome Insights")
    
    st.markdown(f"""
    <div style="background: rgba(16, 185, 129, 0.1); border-left: 5px solid #10b981; padding: 20px; border-radius: 8px;">
        <div style="font-weight: 700; color: #10b981; margin-bottom: 10px;">PROACTIVE ADJUSTMENT DETECTED</div>
        <p style="color: #cbd5e1; margin: 0;">
            Current ambient noise ({noise}dB) is 15% above your individual "Focus Threshold". 
            <b>Recommendation:</b> Active noise cancellation or relocation advised for deep recovery windows.
        </p>
    </div>
    """, unsafe_allow_html=True)
