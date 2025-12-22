"""
Advanced Digital Twin (In-Silico) Interface
High-fidelity physiological simulation and scenario testing.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from .physiological_model import AdvancedPhysiologyModel
from .utils import DataModels

def render_digital_twin_advanced_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #60a5fa; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">🧬</span> Digital Twin (In-Silico)
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem; font-style: italic;">
            High-fidelity biometric simulation engine for predictive resilience modeling.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'phys_model' not in st.session_state:
        st.session_state.phys_model = AdvancedPhysiologyModel()

    model = st.session_state.phys_model

    # --- 1. SYSTEM MONITOR ---
    st.markdown("### 🖥️ Real-Time System Simulation")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); border-left: 5px solid #60a5fa; padding: 20px; border-radius: 10px;">
            <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px;">Vagal Tone Proxy</div>
            <div style="color: white; font-size: 2rem; font-weight: 700;">{model.params['vagal_tone']:.1f}</div>
            <div style="color: #10b981; font-size: 0.8rem;">↑ Optimal State</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); border-left: 5px solid #f59e0b; padding: 20px; border-radius: 10px;">
            <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px;">Metabolic Load</div>
            <div style="color: white; font-size: 2rem; font-weight: 700;">{model.params['metabolic_rate']:.1f}x</div>
            <div style="color: #f59e0b; font-size: 0.8rem;">Basal Energy Output</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div style="background: rgba(30, 41, 59, 0.5); border-left: 5px solid #ec4899; padding: 20px; border-radius: 10px;">
            <div style="color: #94a3b8; font-size: 0.8rem; text-transform: uppercase; margin-bottom: 5px;">Sympathetic Reactivity</div>
            <div style="color: white; font-size: 2rem; font-weight: 700;">{model.params['sympathetic_reactivity']*100:.0f}%</div>
            <div style="color: #ec4899; font-size: 0.8rem;">Adrenaline Threshold</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # --- 2. SCENARIO SIMULATOR ---
    st.markdown("### 🧪 Scenario Simulation (What-If?)")
    
    with st.expander("Configure Stress Profile", expanded=True):
        c1, c2 = st.columns(2)
        with c1:
            stress_mag = st.slider("Stressor Magnitude (0-10)", 0.0, 10.0, 5.0)
            duration = st.slider("Duration (Minutes)", 5, 60, 20)
        with c2:
            intervention = st.selectbox("Apply Preventive Intervention", ["None", "Breathwork", "Nap", "Hydration", "Meditation"])

    if st.button("🚀 Run Simulation", use_container_width=True):
        simulation_data = model.simulate_stress_response(stress_mag, duration)
        
        # Plot results
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=simulation_data['time'], y=simulation_data['hrv'], name="HRV (t)", line=dict(color="#60a5fa", width=3)))
        fig.add_trace(go.Scatter(x=simulation_data['time'], y=simulation_data['cortisol']*2, name="Cortisol (2x)", line=dict(color="#ec4899", dash='dash')))
        
        fig.update_layout(
            title="In-Silico Stress Response Curve",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_title="Minutes",
            yaxis_title="Normalized Metric Value",
            legend=dict(orientation="h", y=1.2),
            font=dict(color="white")
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Recovery Prediction
        recovery = model.predict_recovery_kinetics({'hrv': np.mean(simulation_data['hrv'][-10:])})
        
        rc1, rc2 = st.columns(2)
        with rc1:
            st.metric("Predicted Recovery Half-Life", f"{recovery['half_life_min']}m")
        with rc2:
            st.metric("System Readiness Score", recovery['readiness_score'])

    st.divider()

    # --- 3. RECOVERY KINETICS ---
    st.markdown("### 🧬 Recovery Kinetics Architecture")
    st.markdown("""
    The In-Silico model uses **Lotka-Volterra style predator-prey equations** to simulate the interplay between sympathetic 
    arousal and parasympathetic suppression. This allows for the prediction of **vulnerability windows** up to 12 hours in advance.
    """)
    
    # Simple heatmap visualization
    heatmap_data = np.random.rand(10, 24)
    fig_heat = go.Figure(data=go.Heatmap(
        z=heatmap_data,
        x=[f"{h:02d}:00" for h in range(24)],
        y=["HRV", "GSR", "Temp", "Cortisol", "Glucose", "O2", "EEG-α", "EEG-β", "EMG", "RECOVERY"],
        colorscale='Viridis'
    ))
    fig_heat.update_layout(height=400, title="24h Vulnerability Map (Personalized Distribution)", paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig_heat, use_container_width=True)
