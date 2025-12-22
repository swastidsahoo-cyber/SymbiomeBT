import streamlit as st
import plotly.graph_objects as go
import numpy as np
import time
from modules.twin_model import TwinModel

# Initialize Twin Model
if 'twin_model' not in st.session_state:
    st.session_state.twin_model = TwinModel()

twin = st.session_state.twin_model

def render_digital_twin_page():
    """
    Renders the complete Digital Twin Interface.
    Structure:
    1. Header (Title + Subtitle)
    2. Identity Panel (Twin Profile)
    3. Resilience Quotient (RQ) Dashboard
    4. Simulation Engine (Sliders + Forecast)
    5. Explainability Layer (Feature Importance)
    6. Recovery Kinetics
    7. Intervention Readiness
    """
    
    # --- 1. HEADER ---
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <div style="font-size: 2.2rem; font-weight: 700; color: white;">Symbiome: Autonomic Digital Twin</div>
        <div style="font-size: 1.1rem; color: #94a3b8; font-style: italic;">
            "A real-time physiological simulation that models nervous-system resilience, forecasts vulnerability windows, and quantifies recovery capacity."
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # --- 2. IDENTITY PANEL ---
    # Non-editable fingerprint
    render_identity_panel()
    
    # --- 3. RESILIENCE QUOTIENT (RQ) ---
    render_rq_dashboard()
    
    # --- 4. TWIN SCENARIO SIMULATOR ---
    render_scenario_simulator()
    
    # --- 5. EXPLAINABILITY ---
    render_explainability()

    # --- 6. RECOVERY KINETICS ---
    render_recovery_kinetics()

    # --- 7. INTERVENTION READINESS ---
    render_intervention_readiness()
    
    # --- 8. ETHICS FOOTER ---
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #64748b; font-size: 0.8rem; margin-top: 20px;">
        <strong>ETHICAL SAFEGUARDS ACTIVE</strong><br>
        Models are probabilistic simulations based on user data patterns.<br>
        • No diagnostic claims • No raw biometric storage • Human-in-the-loop design
    </div>
    """, unsafe_allow_html=True)

def render_identity_panel():
    """Renders the Digital Twin Fingerprint."""
    cols = st.columns([1, 1, 1])
    
    # ANS Sensitivty Class
    with cols[0]:
        st.markdown(f"""
        <div style="background: #020617; border: 1px solid #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #c084fc;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">ANS Sensitivity Class</div>
            <div style="font-size: 1.1rem; font-weight: 700; color: white;">{twin.identity}</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 5px;">Inferred from regulation patterns</div>
        </div>
        """, unsafe_allow_html=True)
        
    # Baseline Stability
    with cols[1]:
        st.markdown(f"""
        <div style="background: #020617; border: 1px solid #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #2dd4bf;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Baseline Stability Index</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white;">{twin.baseline_stability:.1f}</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 5px;">Variance at rest (Low = Resilient)</div>
        </div>
        """, unsafe_allow_html=True)

    # Model Confidence
    with cols[2]:
        st.markdown(f"""
        <div style="background: #020617; border: 1px solid #1e293b; padding: 15px; border-radius: 10px; border-left: 4px solid #f59e0b;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase;">Model Confidence</div>
            <div style="font-size: 1.5rem; font-weight: 700; color: white;">{twin.confidence_score}%</div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 5px;">Reliability of current forecast</div>
        </div>
        """, unsafe_allow_html=True)

def render_rq_dashboard():
    """Renders the Resilience Quotient metrics."""
    # Calculate dummy history for RQ for now
    hrv_hist = st.session_state.get('hrv_history', [])
    rq = twin.calculate_rq(hrv_hist, None)
    breakdown = twin.get_rq_breakdown(rq)
    
    st.markdown("### 🧬 Resilience Quotient (RQ)")
    st.markdown("""
    <div style="font-size: 0.9rem; color: #cbd5e1; margin-bottom: 20px;">
        Quantifies nervous-system performance availability. High RQ = High capacity to absorb stress.
    </div>
    """, unsafe_allow_html=True)
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
        # Big Score Card
        color = "#10b981" if rq > 70 else "#f59e0b" if rq > 40 else "#ef4444"
        st.markdown(f"""
        <div style="
            background: radial-gradient(circle at center, rgba(16, 185, 129, 0.1) 0%, #0f172a 70%); 
            border: 2px solid {color}; 
            border-radius: 50%; width: 200px; height: 200px; 
            display: flex; flex-direction: column; justify-content: center; align-items: center;
            margin: auto;
            box-shadow: 0 0 30px {color}40;
        ">
            <div style="font-size: 3.5rem; font-weight: 700; color: white;">{int(rq)}</div>
            <div style="font-size: 1rem; color: {color}; font-weight: 600;">{breakdown['trend']} Stable</div>
            <div style="font-size: 0.8rem; color: #64748b; margin-top: 5px;">RQ SCORE</div>
        </div>
        """, unsafe_allow_html=True)
        
    with c2:
        # Breakdown Bars
        st.markdown("#### Component Analysis")
        
        def render_bar(label, val, max_val, color):
            pct = (val / max_val) * 100
            st.markdown(f"""
            <div style="margin-bottom: 15px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                    <span style="color: #e2e8f0; font-size: 0.9rem;">{label}</span>
                    <span style="color: {color}; font-weight: 700;">{val}/{max_val}</span>
                </div>
                <div style="background: #1e293b; height: 8px; border-radius: 4px; overflow: hidden;">
                    <div style="background: {color}; width: {pct}%; height: 100%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
        render_bar("Resistance (Stress Absorption)", breakdown['resistance'], 40, "#60a5fa")
        render_bar("Recovery Velocity (Bounce Back)", breakdown['recovery'], 40, "#34d399")
        render_bar("Stability (Long-term)", breakdown['stability'], 20, "#a78bfa")

def render_scenario_simulator():
    """Renders the What-If simulation engine."""
    st.markdown("---")
    st.markdown("### 🔮 Twin Scenario Simulator (Counterfactual Engine)")
    st.markdown("""
    <div style="background: #1e293b; padding: 15px; border-radius: 8px; border-left: 4px solid #3b82f6; margin-bottom: 20px;">
        <strong>RESEARCH MODE:</strong> Simulating future trajectories. This system does not wait for stress to happen — it simulates futures to prevent it.
    </div>
    """, unsafe_allow_html=True)
    
    input_col, chart_col = st.columns([1, 2])
    
    with input_col:
        st.markdown("#### Scenario Variables")
        sleep = st.slider("Sleep Deviation (Hours)", 4.0, 10.0, 7.0, 0.5)
        caffeine = st.slider("Caffeine Load (Std. Cups)", 0, 5, 1)
        screen = st.slider("nocturnal Screen Exposure (Hours)", 0, 6, 2)
        noise = st.slider("Environmental Noise Index", 0, 10, 3)
        
        # Calculate modifiers
        modifiers = {
            "sleep": sleep,
            "caffeine": caffeine,
            "screen": screen,
            "noise": noise
        }
        
    with chart_col:
        st.markdown("#### 48-Hour Vulnerability Forecast")
        
        # Get Predictions
        curr_rq = 75 # Baseline
        forecast = twin.predict_future(curr_rq, modifiers)
        baseline_forecast = twin.predict_future(curr_rq, {"sleep": 7.5, "caffeine": 1}) # Optimal reference
        
        # Plot
        fig = go.Figure()
        
        # Scenario Line
        fig.add_trace(go.Scatter(
            x=list(range(48)), 
            y=forecast, 
            mode='lines', 
            name='Counterfactual (Simulated)',
            line=dict(color='#3b82f6', width=3)
        ))
        
        # Baseline Line (Dotted)
        fig.add_trace(go.Scatter(
            x=list(range(48)), 
            y=baseline_forecast, 
            mode='lines', 
            name='Optimal Trajectory',
            line=dict(color='rgba(255,255,255,0.3)', width=2, dash='dot')
        ))
        
        # Vulnerability Zones
        fig.add_hrect(y0=0, y1=40, fillcolor="rgba(239, 68, 68, 0.1)", layer="below", line_width=0)
        fig.add_annotation(x=2, y=35, text="VULNERABILITY WINDOW", showarrow=False, font=dict(color="#ef4444", size=10))

        fig.update_layout(
            height=300,
            margin=dict(l=0, r=0, t=20, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#94a3b8'),
            xaxis_title="Time Horizon (Hours)",
            yaxis_title="Resilience Quotient (RQ)",
            yaxis=dict(range=[0, 100]),
            legend=dict(orientation="h", y=1.1)
        )
        st.plotly_chart(fig, use_container_width=True)

def render_explainability():
    """Renders SHAP-style attribution."""
    st.markdown("### Causal Attribution Engine (SHAP Values)")
    
    # Get current modifiers from session state if possible, or use defaults for demo
    # For this prototype, we'll re-calculate based on what we would have passed
    # In a full react app, we'd hoist state. Here, we just assume "Current State" values
    modifiers = {"sleep": 6.5, "caffeine": 3, "screen": 4} 
    shap = twin.get_shap_explanation(modifiers)
    
    # Sort by impact
    sorted_features = sorted(shap.items(), key=lambda x: x[1], reverse=True)
    
    for feature, impact in sorted_features:
        # Normalize impact for visual bar length
        bar_len = min(100, int(impact * 200)) # Scale up
        color = "#f43f5e" if "Caffeine" in feature or "Screen" in feature else "#ec4899"
        
        st.markdown(f"""
        <div style="margin-bottom: 15px;">
            <div style="display: flex; justify-content: space-between; font-size: 0.8rem; color: #e2e8f0; font-family: monospace;">
                <span>{feature.upper()}</span>
                <span>{int(impact * 100)}% REL. CONTRIB.</span>
            </div>
            <div style="background: #1e293b; height: 4px; border-radius: 2px; margin-top: 5px;">
                <div style="background: {color}; width: {bar_len}%; height: 100%; border-radius: 2px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_recovery_kinetics():
    """Renders the Recovery Half-Life and Kinetics."""
    st.markdown("---")
    st.markdown("### Recovery Kinetics Analysis")
    
    metrics = twin.calculate_recovery_kinetics()
    
    c1, c2 = st.columns([1, 2])
    
    with c1:
         st.markdown(f"""
        <div style="background: #020617; border: 1px solid #1e293b; padding: 20px; border-radius: 12px; height: 100%;">
            <div style="font-size: 0.8rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Recovery Half-Life</div>
            <div style="font-size: 2.5rem; font-weight: 700; color: white;">{metrics['half_life']:.1f} <span style="font-size: 1rem; color: #64748b;">min</span></div>
            <div style="font-size: 0.8rem; color: #10b981; margin-top: 5px;">{metrics['historical_comparison']}</div>
            <div style="color: #64748b; font-size: 0.8rem; margin-top: 15px; font-style: italic;">
                "Time required to recover 50% of baseline HRV after acute stressor."
            </div>
        </div>
        """, unsafe_allow_html=True)
         
    with c2:
        # Simulate Recovery Curve
        x_time = list(range(0, 20))
        # Exponential decay: y = A * e^(-kt)
        y_stress = [100 * np.exp(-0.25 * t) for t in x_time] 
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x_time, y=y_stress, mode='lines', name='Stress Dissipation', line=dict(color='#2dd4bf', width=3)))
        
        # Annotation for Half-life
        half_life_idx = 3 # Approx
        fig.add_vline(x=metrics['half_life'], line_dash="dash", line_color="rgba(255,255,255,0.3)")
        fig.add_annotation(x=metrics['half_life'], y=60, text=f"t½ = {metrics['half_life']:.1f}m", showarrow=True, arrowhead=1)

        fig.update_layout(
             height=200,
             margin=dict(l=0, r=0, t=10, b=0),
             paper_bgcolor='rgba(0,0,0,0)',
             plot_bgcolor='rgba(0,0,0,0)',
             font=dict(color='#94a3b8'),
             xaxis_title="Time Post-Stressor (min)",
             yaxis_title="% Load Remaining",
             showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

def render_intervention_readiness():
    """Renders the Closed-Loop Readiness State."""
    # Get current state from somewhere, strictly assuming dummy for UI dev as per TwinModel
    # In real app, we pass the actual RQ
    rq_score = 65 
    status = twin.get_intervention_readiness(rq_score)
    
    st.markdown("### Intervention Readiness State")
    
    st.markdown(f"""
    <div style="
        background: radial-gradient(circle at left, rgba(15, 23, 42, 1) 0%, rgba(30, 41, 59, 0.5) 100%); 
        border: 1px solid {status['color']}; 
        border-left: 6px solid {status['color']};
        border-radius: 8px; 
        padding: 20px; 
        display: flex; 
        justify-content: space-between; 
        align-items: center;
    ">
        <div>
            <div style="color: {status['color']}; font-weight: 700; letter-spacing: 2px; font-size: 0.9rem;">{status['label']}</div>
            <div style="color: white; font-size: 1.2rem; font-weight: 700; margin-top: 5px;">Suggested Action: {status['action']}</div>
            <div style="color: #94a3b8; font-size: 0.8rem; margin-top: 5px;">Confidence: {status['confidence']}</div>
        </div>
        <div>
             <button style="
                background: {status['color']}20; 
                color: {status['color']}; 
                border: 1px solid {status['color']}; 
                padding: 10px 20px; 
                border-radius: 6px; 
                font-weight: 600; 
                cursor: pointer;
            ">INITIATE PROTOCOL</button>
        </div>
    </div>
    """, unsafe_allow_html=True)
