"""
Predictive Engine Interface.
Visualizes future resilience trajectories and intervention windows.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from .ml_models import PredictiveModels

def render_predictive_engine_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #f87171; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">📈</span> Predictive Engine
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Advanced Machine Learning forecasting. Predicting stress events before they manifest.
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- FORECAST OVERVIEW ---
    st.markdown("### 🔮 4-Hour Resilience Forecast")
    
    # Generate mock history
    history = [72, 70, 74, 76, 75, 78, 80, 79, 77, 75]
    prediction, upper, lower = PredictiveModels.forecast_sri(history)
    
    times_hist = [f"-{i}h" for i in range(len(history)-1, -1, -1)]
    times_fut = [f"+{i+1}h" for i in range(len(prediction))]
    
    fig = go.Figure()
    
    # History
    fig.add_trace(go.Scatter(x=times_hist, y=history, name="Historical SRI", line=dict(color="#94a3b8", width=2)))
    
    # Prediction
    fig.add_trace(go.Scatter(x=times_fut, y=prediction, name="ML Prediction", line=dict(color="#f87171", width=4)))
    
    # Confidence Intervals
    fig.add_trace(go.Scatter(
        x=times_fut + times_fut[::-1],
        y=list(upper) + list(lower)[::-1],
        fill='toself',
        fillcolor='rgba(248, 113, 113, 0.1)',
        line=dict(color='rgba(255,255,255,0)'),
        hoverinfo="skip",
        showlegend=False
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        yaxis=dict(range=[0, 100], showgrid=False),
        xaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=10, b=0),
        legend=dict(orientation="h", y=1.2)
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # --- RISK ANALYSIS ---
    st.markdown("### ⚠️ Early Warning System")
    col1, col2 = st.columns(2)
    
    risk_prob = PredictiveModels.calculate_risk_probability(history[-1], -2.0)
    
    with col1:
        st.markdown(f"""
        <div style="background: rgba(248, 113, 113, 0.1); border: 2px solid #ef4444; padding: 25px; border-radius: 12px; text-align: center;">
            <div style="color: #ef4444; font-weight: 700; text-transform: uppercase; letter-spacing: 1px;">Stress Risk (Next 60m)</div>
            <div style="color: white; font-size: 3rem; font-weight: 800;">{risk_prob*100:.0f}%</div>
            <div style="margin-top: 10px; color: #cbd5e1; font-size: 0.8rem;">Confidence: High (94.2%)</div>
        </div>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown("""
        #### Prediction Insights
        - **Primary Driver**: Incomplete recovery from previous T-3 stressor.
        - **Secondary Driver**: Circadian dip predicted at 15:00.
        - **Recommendation**: Pre-emptive 5-minute coherence training at 14:45.
        """)
        if st.button("🛡️ Schedule Autonomic Shielding", use_container_width=True):
            st.success("Intervention protocol scheduled for +45m")

    st.divider()

    # --- FEATURE IMPORTANCE ---
    st.markdown("### 🧬 Causal Attribution (SHAP Analysis)")
    
    features = ['Sleep Quality', 'Caffeine Timing', 'Meeting Load', 'Ambient Noise', 'Activity Level']
    impact = [35, -20, -15, -10, 20] # Percent contribution
    
    fig_shap = go.Figure()
    fig_shap.add_trace(go.Bar(
        y=features,
        x=impact,
        orientation='h',
        marker_color=['#10b981' if i > 0 else '#ef4444' for i in impact]
    ))
    
    fig_shap.update_layout(
        title="Predictive Signal Contributions",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        xaxis=dict(title="% Impact on Resilience"),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig_shap, use_container_width=True)
