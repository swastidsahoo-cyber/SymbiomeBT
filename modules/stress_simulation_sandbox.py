"""
Stress Simulation Sandbox
Experimental "What-If" environment simulator - Adjust parameters and see predicted resilience impact
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np

def render_stress_simulation_sandbox_page():
    # Header
    st.markdown('<div style="text-align: center; margin-bottom: 30px;"><h2 style="color: #06b6d4; font-size: 2.5rem; margin-bottom: 10px;">Stress Simulation Sandbox</h2><p style="color: #94a3b8; font-size: 0.95rem;">Experimental "What-If" environment simulator - Adjust parameters and see predicted resilience impact</p></div>', unsafe_allow_html=True)
    
    # Quick Scenarios
    st.markdown('<h3 style="color: #f59e0b; margin-bottom: 16px;">⚡ Quick Scenarios</h3>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    scenarios = {
        'optimal': {'light': 75, 'noise': 30, 'temp': 22, 'sleep': 8, 'caffeine': 1, 'screen': 3},
        'school': {'light': 85, 'noise': 50, 'temp': 20, 'sleep': 6, 'caffeine': 0, 'screen': 2},
        'baby': {'light': 60, 'noise': 70, 'temp': 24, 'sleep': 5, 'caffeine': 2, 'screen': 1},
        'late_night': {'light': 40, 'noise': 20, 'temp': 19, 'sleep': 4, 'caffeine': 3, 'screen': 8},
        'meditation': {'light': 50, 'noise': 15, 'temp': 23, 'sleep': 8, 'caffeine': 0, 'screen': 1},
        'reset': {'light': 75, 'noise': 30, 'temp': 22, 'sleep': 8, 'caffeine': 1, 'screen': 3}
    }
    
    with col1:
        if st.button("🌟 Optimal Environment", use_container_width=True, type="secondary"):
            apply_scenario(scenarios['optimal'])
    with col2:
        if st.button("🏫 School Morning", use_container_width=True, type="secondary"):
            apply_scenario(scenarios['school'])
    with col3:
        if st.button("👶 Baby Commute", use_container_width=True, type="secondary"):
            apply_scenario(scenarios['baby'])
    with col4:
        if st.button("💡 Late Night Study", use_container_width=True, type="secondary"):
            apply_scenario(scenarios['late_night'])
    with col5:
        if st.button("🧘 Meditation Session", use_container_width=True, type="secondary"):
            apply_scenario(scenarios['meditation'])
    with col6:
        if st.button("🔄 Reset", use_container_width=True, type="secondary"):
            apply_scenario(scenarios['reset'])
    
    # Initialize session state
    if 'sim_light' not in st.session_state:
        st.session_state.sim_light = 75
    if 'sim_noise' not in st.session_state:
        st.session_state.sim_noise = 30
    if 'sim_temp' not in st.session_state:
        st.session_state.sim_temp = 22
    if 'sim_sleep' not in st.session_state:
        st.session_state.sim_sleep = 8
    if 'sim_caffeine' not in st.session_state:
        st.session_state.sim_caffeine = 1
    if 'sim_screen' not in st.session_state:
        st.session_state.sim_screen = 3
    
    # Main layout: Left panel (parameters) and Right panel (predictions)
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.markdown('<h3 style="color: #cbd5e1; margin-top: 30px; margin-bottom: 20px;">Environmental & Behavioral Parameters</h3>', unsafe_allow_html=True)
        
        # Light Intensity
        st.markdown(f'<div style="margin-bottom: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #fbbf24;">💡 Light Intensity</span><span style="color: #06b6d4; font-weight: 700;">{st.session_state.sim_light}%</span></div></div>', unsafe_allow_html=True)
        st.session_state.sim_light = st.slider("", 0, 100, st.session_state.sim_light, key="light_slider", label_visibility="collapsed")
        st.markdown('<p style="color: #64748b; font-size: 0.75rem; margin-top: -10px;">Optimal: 60-80% (bright indoor light)</p>', unsafe_allow_html=True)
        
        # Ambient Noise
        st.markdown(f'<div style="margin-bottom: 20px; margin-top: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #06b6d4;">🔊 Ambient Noise</span><span style="color: #06b6d4; font-weight: 700;">{st.session_state.sim_noise} dB</span></div></div>', unsafe_allow_html=True)
        st.session_state.sim_noise = st.slider("", 0, 100, st.session_state.sim_noise, key="noise_slider", label_visibility="collapsed")
        st.markdown('<p style="color: #64748b; font-size: 0.75rem; margin-top: -10px;">Optimal: <40 dB (library quiet)</p>', unsafe_allow_html=True)
        
        # Temperature
        st.markdown(f'<div style="margin-bottom: 20px; margin-top: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #f59e0b;">🌡️ Temperature</span><span style="color: #06b6d4; font-weight: 700;">{st.session_state.sim_temp}°C</span></div></div>', unsafe_allow_html=True)
        st.session_state.sim_temp = st.slider("", 15, 30, st.session_state.sim_temp, key="temp_slider", label_visibility="collapsed")
        st.markdown('<p style="color: #64748b; font-size: 0.75rem; margin-top: -10px;">Optimal: 20-24°C</p>', unsafe_allow_html=True)
        
        # Sleep
        st.markdown(f'<div style="margin-bottom: 20px; margin-top: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #a78bfa;">😴 Sleep (last night)</span><span style="color: #06b6d4; font-weight: 700;">{st.session_state.sim_sleep}h</span></div></div>', unsafe_allow_html=True)
        st.session_state.sim_sleep = st.slider("", 0, 12, st.session_state.sim_sleep, key="sleep_slider", label_visibility="collapsed")
        st.markdown('<p style="color: #64748b; font-size: 0.75rem; margin-top: -10px;">Optimal: 7-9h</p>', unsafe_allow_html=True)
        
        # Caffeine
        st.markdown(f'<div style="margin-bottom: 20px; margin-top: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #f59e0b;">☕ Caffeine Intake</span><span style="color: #06b6d4; font-weight: 700;">{st.session_state.sim_caffeine} cups</span></div></div>', unsafe_allow_html=True)
        st.session_state.sim_caffeine = st.slider("", 0, 5, st.session_state.sim_caffeine, key="caffeine_slider", label_visibility="collapsed")
        st.markdown('<p style="color: #64748b; font-size: 0.75rem; margin-top: -10px;">Optimal: 1-2 cups</p>', unsafe_allow_html=True)
        
        # Screen Time
        st.markdown(f'<div style="margin-bottom: 20px; margin-top: 20px;"><div style="display: flex; justify-content: space-between; margin-bottom: 8px;"><span style="color: #3b82f6;">📱 Screen Time Today</span><span style="color: #06b6d4; font-weight: 700;">{st.session_state.sim_screen}h</span></div></div>', unsafe_allow_html=True)
        st.session_state.sim_screen = st.slider("", 0, 12, st.session_state.sim_screen, key="screen_slider", label_visibility="collapsed")
        st.markdown('<p style="color: #64748b; font-size: 0.75rem; margin-top: -10px;">Optimal: <6h (especially before bed)</p>', unsafe_allow_html=True)
    
    with col_right:
        # Calculate predicted SRI
        params = {
            'light': st.session_state.sim_light,
            'noise': st.session_state.sim_noise,
            'temp': st.session_state.sim_temp,
            'sleep': st.session_state.sim_sleep,
            'caffeine': st.session_state.sim_caffeine,
            'screen': st.session_state.sim_screen
        }
        
        predicted_sri, factors = calculate_predicted_sri(params)
        baseline_sri = 72
        change = predicted_sri - baseline_sri
        
        # Predicted Resilience Impact
        st.markdown('<h3 style="color: #a78bfa; margin-top: 30px; margin-bottom: 20px;">📊 Predicted Resilience Impact</h3>', unsafe_allow_html=True)
        
        st.markdown(f'<div style="background: linear-gradient(135deg, rgba(167, 139, 250, 0.2) 0%, rgba(139, 92, 246, 0.1) 100%); border: 2px solid rgba(167, 139, 250, 0.4); border-radius: 16px; padding: 30px; text-align: center;"><div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 8px;">Predicted SRI</div><div style="color: #e2e8f0; font-size: 4rem; font-weight: 900; margin-bottom: 12px;">{predicted_sri}</div><div style="color: #06b6d4; font-size: 1.1rem; font-weight: 700;">{change:+.1f} from baseline</div></div>', unsafe_allow_html=True)
        
        # Factor Analysis
        st.markdown('<div style="margin-top: 20px; margin-bottom: 10px;"><span style="color: #cbd5e1; font-weight: 700;">Factor Analysis:</span></div>', unsafe_allow_html=True)
        
        for factor, value in factors.items():
            color = '#10b981' if value > 0 else '#ef4444' if value < 0 else '#64748b'
            st.markdown(f'<div style="display: flex; justify-content: space-between; padding: 8px 12px; margin: 6px 0; background: rgba(30, 41, 59, 0.5); border-radius: 8px;"><span style="color: #cbd5e1;">{factor}</span><span style="color: {color}; font-weight: 700;">{value:+d}</span></div>', unsafe_allow_html=True)
        
        # Predicted HRV Response
        st.markdown('<h4 style="color: #10b981; margin-top: 30px; margin-bottom: 16px;">Predicted HRV Response</h4>', unsafe_allow_html=True)
        
        time_points = np.linspace(0, 60, 100)
        hrv_response = 50 + 10 * np.sin(time_points / 10) + (predicted_sri - 72) / 5 + np.random.normal(0, 2, 100)
        
        fig_hrv = go.Figure()
        fig_hrv.add_trace(go.Scatter(x=time_points, y=hrv_response, mode='lines', line=dict(color='#10b981', width=2), fill='tozeroy', fillcolor='rgba(16, 185, 129, 0.1)'))
        
        fig_hrv.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.9)',
            height=200,
            xaxis=dict(title="", showgrid=False, showticklabels=False),
            yaxis=dict(title="", showgrid=False, showticklabels=False),
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False
        )
        
        st.plotly_chart(fig_hrv, use_container_width=True)
        
        # Predicted GSR Response
        st.markdown('<h4 style="color: #f59e0b; margin-top: 20px; margin-bottom: 16px;">Predicted GSR Response</h4>', unsafe_allow_html=True)
        
        gsr_response = 3 + 0.5 * np.sin(time_points / 8) - (predicted_sri - 72) / 20 + np.random.normal(0, 0.1, 100)
        
        fig_gsr = go.Figure()
        fig_gsr.add_trace(go.Scatter(x=time_points, y=gsr_response, mode='lines', line=dict(color='#f59e0b', width=2)))
        
        fig_gsr.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.9)',
            height=200,
            xaxis=dict(title="", showgrid=False, showticklabels=False),
            yaxis=dict(title="", showgrid=False, showticklabels=False),
            margin=dict(l=10, r=10, t=10, b=10),
            showlegend=False
        )
        
        st.plotly_chart(fig_gsr, use_container_width=True)
    
    # AI Simulation Explanation
    st.markdown('<div style="margin-top: 40px;"><h3 style="color: #06b6d4; margin-bottom: 16px;">🤖 AI Simulation Explanation</h3></div>', unsafe_allow_html=True)
    
    explanation = generate_explanation(params, predicted_sri)
    
    st.markdown(f'<div style="background: rgba(6, 182, 212, 0.1); border-left: 4px solid #06b6d4; padding: 20px; border-radius: 8px;"><p style="color: #cbd5e1; line-height: 1.8;">{explanation}</p></div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([6, 1])
    with col2:
        st.button("Quick Session", use_container_width=True, type="secondary")
        st.button("Note Tip", use_container_width=True, type="secondary")


def apply_scenario(scenario):
    """Apply a quick scenario preset"""
    st.session_state.sim_light = scenario['light']
    st.session_state.sim_noise = scenario['noise']
    st.session_state.sim_temp = scenario['temp']
    st.session_state.sim_sleep = scenario['sleep']
    st.session_state.sim_caffeine = scenario['caffeine']
    st.session_state.sim_screen = scenario['screen']
    st.rerun()


def calculate_predicted_sri(params):
    """Calculate predicted SRI based on parameters"""
    base_sri = 72
    factors = {}
    
    # Light factor
    if 60 <= params['light'] <= 80:
        base_sri += 5
        factors['Optimal light'] = 5
    elif params['light'] < 40:
        base_sri -= 3
        factors['Low light'] = -3
    
    # Noise factor
    if params['noise'] < 40:
        # Quiet is good
        pass
    elif params['noise'] > 60:
        base_sri -= 5
        factors['High noise'] = -5
    
    # Temperature factor
    if 20 <= params['temp'] <= 24:
        # Optimal temp
        pass
    else:
        base_sri -= 2
        factors['Suboptimal temp'] = -2
    
    # Sleep factor (most important)
    if 7 <= params['sleep'] <= 9:
        base_sri += 5
        factors['Optimal sleep'] = 5
    elif params['sleep'] < 6:
        base_sri -= 8
        factors['Sleep deprivation'] = -8
    elif params['sleep'] > 10:
        base_sri -= 3
        factors['Oversleep'] = -3
    
    # Caffeine factor
    if 1 <= params['caffeine'] <= 2:
        # Moderate caffeine is fine
        pass
    elif params['caffeine'] > 3:
        base_sri -= 4
        factors['High caffeine'] = -4
    
    # Screen time factor
    if params['screen'] < 6:
        # Acceptable screen time
        pass
    else:
        base_sri -= 5
        factors['Excessive screen time'] = -5
    
    return base_sri, factors


def generate_explanation(params, predicted_sri):
    """Generate AI explanation based on parameters"""
    explanations = []
    
    if 60 <= params['light'] <= 80:
        explanations.append("Excellent environmental conditions detected.")
    
    if 7 <= params['sleep'] <= 9:
        explanations.append("Your current parameter combination supports optimal autonomic balance.")
    elif params['sleep'] < 6:
        explanations.append("Sleep deprivation detected - this significantly impacts cognitive performance and stress resilience.")
    
    if params['screen'] > 6:
        explanations.append("High screen time may affect sleep quality and increase sympathetic activation.")
    
    if predicted_sri > 75:
        explanations.append("HRV is predicted to remain elevated with minimal sympathetic activation.")
    elif predicted_sri < 65:
        explanations.append("Current conditions may lead to decreased HRV and increased stress markers.")
    
    return " ".join(explanations) if explanations else "Your current parameter combination supports moderate stress resilience."
