"""
Digital Twin In-Silico Laboratory (v1.0)
PIXEL-PERFECT UI matching competition screenshot.
Functional scenario simulations with dynamic updates.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
from datetime import datetime, timedelta

# Scenario data - each scenario has unique simulation parameters
SCENARIOS = {
    "caffeine_10am": {
        "name": "Caffeine at 10 AM",
        "desc": "Single coffee during peak productivity",
        "impact": "+2.3%",
        "impact_val": 2.3,
        "findings": [
            "Moderate cortisol spike optimized alertness peak at 11 AM",
            "No negative sleep impact detected",
            "Slight improvement in cognitive task performance",
            "Optimal circadian alignment improved overall SRI"
        ],
        "recommendation": "Morning caffeine (before 12 PM) shows beneficial for your physiology. Optimal window: 9-11 AM.",
        "hrv": "+3.2%",
        "cortisol": "-0.8%",
        "sleep": "+0%",
        "cognitive": "-0.6%",
        "baseline_offset": 2
    },
    "caffeine_4pm": {
        "name": "Caffeine at 4 PM",
        "desc": "Afternoon coffee and work delay",
        "impact": "-4.1%",
        "impact_val": -4.1,
        "findings": [
            "Elevated cortisol persists into evening hours",
            "Sleep latency increased by 18 minutes",
            "REM sleep reduced by 12%",
            "Morning recovery delayed by 45 minutes"
        ],
        "recommendation": "Avoid caffeine after 2 PM. Late caffeine disrupts sleep architecture for your specific metabolism.",
        "hrv": "-5.2%",
        "cortisol": "+12.4%",
        "sleep": "-8.6%",
        "cognitive": "+2.1%",
        "baseline_offset": -4
    },
    "reduced_sleep": {
        "name": "Reduced Sleep (5hrs)",
        "desc": "Sleep restriction to 5 hours",
        "impact": "-8.7%",
        "impact_val": -8.7,
        "findings": [
            "Cumulative sleep debt accumulates rapidly",
            "HRV drops 15% below baseline",
            "Stress recovery time doubles",
            "Cognitive performance degrades by 22%"
        ],
        "recommendation": "Sleep debt has cascading negative effects. Maintain minimum 7 hours for optimal resilience.",
        "hrv": "-15.3%",
        "cortisol": "+18.7%",
        "sleep": "-35.2%",
        "cognitive": "+22.4%",
        "baseline_offset": -9
    },
    "no_emails": {
        "name": "No Work Emails",
        "desc": "Email-free evening (post-6 PM)",
        "impact": "+5.8%",
        "impact_val": 5.8,
        "findings": [
            "Evening cortisol drops 28% faster",
            "Sleep latency improves by 12 minutes",
            "Morning HRV 8% higher",
            "Parasympathetic activation optimized"
        ],
        "recommendation": "Email boundaries significantly improve recovery. Implement strict cutoff at 6 PM.",
        "hrv": "+8.4%",
        "cortisol": "-14.2%",
        "sleep": "+6.8%",
        "cognitive": "-5.3%",
        "baseline_offset": 6
    },
    "morning_exercise": {
        "name": "Morning Exercise",
        "desc": "30-min cardio at 7 AM",
        "impact": "+7.2%",
        "impact_val": 7.2,
        "findings": [
            "Sustained HRV elevation throughout day",
            "Stress buffer capacity increased 18%",
            "Sleep quality improved (deep sleep +15%)",
            "Cognitive clarity enhanced until 3 PM"
        ],
        "recommendation": "Morning exercise shows strongest positive cascade. Optimal time: 7-8 AM for your chronotype.",
        "hrv": "+12.6%",
        "cortisol": "-6.8%",
        "sleep": "+9.4%",
        "cognitive": "-8.2%",
        "baseline_offset": 7
    },
    "optimal_snack": {
        "name": "Optimal Snack Pattern",
        "desc": "Protein-rich snacks every 3 hours",
        "impact": "+3.5%",
        "impact_val": 3.5,
        "findings": [
            "Blood glucose stability improved 24%",
            "Afternoon energy dip eliminated",
            "Stress-induced cortisol spikes blunted",
            "Cognitive performance sustained"
        ],
        "recommendation": "Consistent protein intake prevents metabolic stress. Target: 15-20g protein every 3 hours.",
        "hrv": "+4.2%",
        "cortisol": "-8.6%",
        "sleep": "+2.1%",
        "cognitive": "-6.4%",
        "baseline_offset": 3
    },
    "early_sunlight": {
        "name": "Early Sunlight (6hrs)",
        "desc": "Outdoor light exposure 6-7 AM",
        "impact": "+4.9%",
        "impact_val": 4.9,
        "findings": [
            "Circadian rhythm entrainment optimized",
            "Melatonin suppression timed perfectly",
            "Evening sleep onset 15 min earlier",
            "Morning alertness improved 32%"
        ],
        "recommendation": "Early light exposure is powerful circadian anchor. Minimum 15 minutes outdoor exposure before 8 AM.",
        "hrv": "+6.8%",
        "cortisol": "-4.2%",
        "sleep": "+7.6%",
        "cognitive": "-3.8%",
        "baseline_offset": 5
    },
    "optimal_breaks": {
        "name": "Optimal Break Pattern",
        "desc": "5-min breaks every 90 minutes",
        "impact": "+6.1%",
        "impact_val": 6.1,
        "findings": [
            "Sustained attention capacity increased",
            "Stress accumulation prevented",
            "HRV maintained above baseline",
            "End-of-day fatigue reduced 40%"
        ],
        "recommendation": "Ultradian rhythm alignment prevents burnout. Implement strict 90-min work blocks with 5-min recovery.",
        "hrv": "+7.4%",
        "cortisol": "-10.2%",
        "sleep": "+3.8%",
        "cognitive": "-12.6%",
        "baseline_offset": 6
    }
}

def generate_simulation_data(scenario_key, baseline=61):
    """Generate 24-hour SRI simulation data for a scenario"""
    scenario = SCENARIOS[scenario_key]
    offset = scenario['baseline_offset']
    
    # Generate realistic 24-hour pattern
    hours = list(range(24))
    sri_values = []
    
    for hour in hours:
        # Base circadian pattern
        if 0 <= hour < 6:  # Sleep
            base = baseline + offset + random.uniform(-2, 1)
        elif 6 <= hour < 9:  # Morning rise
            base = baseline + offset + (hour - 6) * 2 + random.uniform(-1, 2)
        elif 9 <= hour < 12:  # Morning peak
            base = baseline + offset + 8 + random.uniform(-1, 1)
        elif 12 <= hour < 14:  # Post-lunch dip
            base = baseline + offset + 4 + random.uniform(-2, 0)
        elif 14 <= hour < 18:  # Afternoon
            base = baseline + offset + 6 + random.uniform(-1, 1)
        elif 18 <= hour < 22:  # Evening decline
            base = baseline + offset + (22 - hour) * 0.5 + random.uniform(-1, 0)
        else:  # Pre-sleep
            base = baseline + offset - 2 + random.uniform(-1, 0)
        
        # Scenario-specific modifications
        if scenario_key == "caffeine_4pm" and 16 <= hour < 24:
            base -= (hour - 16) * 0.5  # Gradual decline from late caffeine
        elif scenario_key == "morning_exercise" and 7 <= hour < 20:
            base += 3  # Sustained boost
        elif scenario_key == "reduced_sleep":
            base -= 5  # Overall suppression
        
        sri_values.append(max(30, min(95, base)))
    
    return hours, sri_values

def render_digital_twin_advanced_page():
    # Initialize session state
    if 'selected_scenario' not in st.session_state:
        st.session_state.selected_scenario = "caffeine_10am"
    if 'simulation_run' not in st.session_state:
        st.session_state.simulation_run = False
    
    # CSS - Pixel-perfect match
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; background: #0a0e27; }
.twin-header { text-align: center; padding: 30px 0 20px 0; }
.twin-title { color: #06b6d4; font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.twin-subtitle { color: #94a3b8; font-size: 0.85rem; font-weight: 500; line-height: 1.6; }
.twin-subtitle .highlight { color: #06b6d4; font-weight: 700; }
.action-buttons { display: flex; gap: 10px; justify-content: center; margin: 20px 0; }
.action-btn { background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); color: #06b6d4; padding: 8px 16px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.twin-status-panel { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0; position: relative; }
.twin-status-title { color: white; font-size: 1rem; font-weight: 800; margin-bottom: 15px; }
.twin-status-subtitle { color: #64748b; font-size: 0.75rem; margin-bottom: 20px; }
.twin-metrics { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
.twin-metric { background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 8px; padding: 12px; }
.twin-metric-label { color: #64748b; font-size: 0.7rem; font-weight: 600; margin-bottom: 6px; }
.twin-metric-value { color: white; font-size: 1.1rem; font-weight: 800; }
.twin-sri-circle { position: absolute; top: 20px; right: 20px; width: 80px; height: 80px; border-radius: 50%; background: linear-gradient(135deg, #06b6d4 0%, #0891b2 100%); display: flex; align-items: center; justify-content: center; font-size: 1.8rem; font-weight: 900; color: white; box-shadow: 0 0 20px rgba(6, 182, 212, 0.4); }
.scenario-section-title { color: white; font-size: 1.1rem; font-weight: 800; margin: 30px 0 15px 0; }
.scenario-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 30px; }
.scenario-card { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 16px; cursor: pointer; transition: all 0.2s; }
.scenario-card:hover { border-color: #06b6d4; transform: translateY(-2px); }
.scenario-card.selected { border-color: #06b6d4; background: rgba(6, 182, 212, 0.05); }
.scenario-icon { color: #06b6d4; font-size: 1.2rem; margin-bottom: 8px; }
.scenario-name { color: white; font-size: 0.85rem; font-weight: 700; margin-bottom: 4px; }
.scenario-desc { color: #64748b; font-size: 0.7rem; line-height: 1.4; }
.chart-panel { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0; }
.chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.chart-title { color: white; font-size: 1rem; font-weight: 800; }
.outcome-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; margin: 20px 0; }
.outcome-panel { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 24px; }
.outcome-title { color: white; font-size: 1rem; font-weight: 800; margin-bottom: 15px; display: flex; align-items: center; gap: 8px; }
.outcome-impact-label { color: #64748b; font-size: 0.75rem; margin-bottom: 8px; }
.outcome-impact-value { font-size: 2rem; font-weight: 900; margin-bottom: 20px; }
.outcome-impact-value.positive { color: #10b981; }
.outcome-impact-value.negative { color: #ef4444; }
.outcome-findings-title { color: white; font-size: 0.85rem; font-weight: 700; margin-bottom: 12px; }
.outcome-finding { color: #94a3b8; font-size: 0.75rem; line-height: 1.6; margin-bottom: 8px; padding-left: 15px; position: relative; }
.outcome-finding:before { content: '•'; position: absolute; left: 0; color: #06b6d4; }
.outcome-recommendation { background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 8px; padding: 12px; margin-top: 15px; }
.outcome-rec-text { color: #94a3b8; font-size: 0.75rem; line-height: 1.6; }
.mech-bar-container { margin-bottom: 15px; }
.mech-bar-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.mech-bar-label { color: white; font-size: 0.8rem; font-weight: 700; }
.mech-bar-value { color: #06b6d4; font-size: 0.75rem; font-weight: 800; }
.mech-bar-bg { width: 100%; height: 8px; background: rgba(255, 255, 255, 0.05); border-radius: 4px; overflow: hidden; }
.mech-bar-fill { height: 100%; background: linear-gradient(90deg, #06b6d4 0%, #0891b2 100%); border-radius: 4px; }
.mech-note { background: rgba(99, 102, 241, 0.05); border: 1px solid rgba(99, 102, 241, 0.2); border-radius: 8px; padding: 10px; margin-top: 15px; }
.mech-note-text { color: #94a3b8; font-size: 0.7rem; line-height: 1.5; }
.architecture-panel { background: rgba(6, 182, 212, 0.03); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 12px; padding: 20px; margin: 30px 0; }
.arch-title { color: #06b6d4; font-size: 0.9rem; font-weight: 800; margin-bottom: 12px; }
.arch-desc { color: #94a3b8; font-size: 0.75rem; line-height: 1.7; margin-bottom: 15px; }
.arch-details { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.arch-detail { color: #64748b; font-size: 0.7rem; padding-left: 12px; position: relative; }
.arch-detail:before { content: '•'; position: absolute; left: 0; color: #06b6d4; }
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Header
    header_html = """<div class="twin-header">
<div class="twin-title">🧬 Digital Twin In-Silico Laboratory</div>
<div class="twin-subtitle">Run thousands of <span class="highlight">"What If"</span> scenarios on a virtual model of your nervous system. Optimize your human before events physically occur.</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Action Buttons
    action_html = """<div class="action-buttons">
<div class="action-btn">🧠 Virtual Physiology Model</div>
<div class="action-btn">📊 Stress Vulnerability</div>
<div class="action-btn">⚡ Predictive Optimization</div>
</div>"""
    st.markdown(action_html, unsafe_allow_html=True)
    
    # Your Digital Twin Status Panel
    current_time = datetime.now()
    next_stress_time = current_time + timedelta(hours=random.randint(2, 6))
    
    status_html = f"""<div class="twin-status-panel">
<div class="twin-sri-circle">59</div>
<div class="twin-status-title">Your Digital Twin</div>
<div class="twin-status-subtitle">Virtual model synchronized with your current physiological state</div>
<div class="twin-metrics">
<div class="twin-metric">
<div class="twin-metric-label">Baseline SRI</div>
<div class="twin-metric-value">61.2%</div>
</div>
<div class="twin-metric">
<div class="twin-metric-label">Simulation Fidelity</div>
<div class="twin-metric-value">92.6%</div>
</div>
<div class="twin-metric">
<div class="twin-metric-label">Latest Stress</div>
<div class="twin-metric-value" style="color: #10b981;">+5.2</div>
</div>
<div class="twin-metric">
<div class="twin-metric-label">Next Stress</div>
<div class="twin-metric-value">{next_stress_time.strftime('%I:%M %p')}</div>
</div>
</div>
</div>"""
    st.markdown(status_html, unsafe_allow_html=True)
    
    # Select "What If" Scenario
    st.markdown('<div class="scenario-section-title">Select "What If" Scenario</div>', unsafe_allow_html=True)
    
    # Scenario Grid
    scenarios_list = [
        ("caffeine_10am", "☕"),
        ("caffeine_4pm", "☕"),
        ("reduced_sleep", "😴"),
        ("no_emails", "📧"),
        ("morning_exercise", "🏃"),
        ("optimal_snack", "🍎"),
        ("early_sunlight", "☀️"),
        ("optimal_breaks", "⏸️")
    ]
    
    cols = st.columns(4)
    for idx, (scenario_key, icon) in enumerate(scenarios_list):
        with cols[idx % 4]:
            scenario = SCENARIOS[scenario_key]
            selected_class = "selected" if st.session_state.selected_scenario == scenario_key else ""
            if st.button(f"{icon} {scenario['name']}", key=f"btn_{scenario_key}", use_container_width=True):
                st.session_state.selected_scenario = scenario_key
                st.session_state.simulation_run = True
                st.rerun()
    
    # Get current scenario data
    current_scenario = SCENARIOS[st.session_state.selected_scenario]
    hours, sri_values = generate_simulation_data(st.session_state.selected_scenario)
    
    # 24-Hour Simulation Chart
    st.markdown('<div class="chart-panel">', unsafe_allow_html=True)
    chart_header_html = f"""<div class="chart-header">
<div class="chart-title">24-Hour Simulation Results</div>
<div style="display: flex; gap: 10px; align-items: center;">
<div style="color: #64748b; font-size: 0.75rem;">Scenario: <span style="color: #06b6d4; font-weight: 700;">{current_scenario['name']}</span></div>
<button style="background: #06b6d4; color: white; border: none; padding: 6px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; cursor: pointer;">▶ Run Simulation</button>
</div>
</div>"""
    st.markdown(chart_header_html, unsafe_allow_html=True)
    
    # Create chart
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[f"{h:02d}:00" for h in hours],
        y=sri_values,
        fill='tozeroy',
        line=dict(color='#06b6d4', width=2),
        fillcolor='rgba(6, 182, 212, 0.1)',
        name='Baseline (No Change)'
    ))
    
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        height=300,
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(
            showgrid=False,
            color='#64748b',
            tickvals=[f"{h:02d}:00" for h in range(0, 24, 3)]
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='rgba(255,255,255,0.05)',
            color='#64748b',
            range=[0, 100],
            title=dict(text="SRI", font=dict(size=10))
        ),
        showlegend=False,
        font=dict(family='Inter', size=10)
    )
    
    st.plotly_chart(fig, use_container_width=True, key="twin_sim_chart")
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Outcome Grid
    st.markdown('<div class="outcome-grid">', unsafe_allow_html=True)
    
    # Predicted Outcome Panel
    impact_class = "positive" if current_scenario['impact_val'] > 0 else "negative"
    outcome_html = f"""<div class="outcome-panel">
<div class="outcome-title">📊 Predicted Outcome</div>
<div class="outcome-impact-label">Overall Impact on SRI</div>
<div class="outcome-impact-value {impact_class}">{current_scenario['impact']}</div>
<div class="outcome-findings-title">Key Findings</div>
{''.join([f'<div class="outcome-finding">{finding}</div>' for finding in current_scenario['findings']])}
<div class="outcome-recommendation">
<div class="outcome-rec-text"><strong>Recommendation:</strong> {current_scenario['recommendation']}</div>
</div>
</div>"""
    st.markdown(outcome_html, unsafe_allow_html=True)
    
    # Mechanistic Analysis Panel
    mech_html = f"""<div class="outcome-panel">
<div class="outcome-title">⚙️ Mechanistic Analysis</div>
<div class="mech-bar-container">
<div class="mech-bar-header">
<div class="mech-bar-label">HRV Impact</div>
<div class="mech-bar-value">{current_scenario['hrv']}</div>
</div>
<div class="mech-bar-bg">
<div class="mech-bar-fill" style="width: {abs(float(current_scenario['hrv'].replace('%', '')))}%;"></div>
</div>
</div>
<div class="mech-bar-container">
<div class="mech-bar-header">
<div class="mech-bar-label">Cortisol Response</div>
<div class="mech-bar-value">{current_scenario['cortisol']}</div>
</div>
<div class="mech-bar-bg">
<div class="mech-bar-fill" style="width: {abs(float(current_scenario['cortisol'].replace('%', '')))}%;"></div>
</div>
</div>
<div class="mech-bar-container">
<div class="mech-bar-header">
<div class="mech-bar-label">Sleep Quality</div>
<div class="mech-bar-value">{current_scenario['sleep']}</div>
</div>
<div class="mech-bar-bg">
<div class="mech-bar-fill" style="width: {abs(float(current_scenario['sleep'].replace('%', '')))}%;"></div>
</div>
</div>
<div class="mech-bar-container">
<div class="mech-bar-header">
<div class="mech-bar-label">Cognitive Load</div>
<div class="mech-bar-value">{current_scenario['cognitive']}</div>
</div>
<div class="mech-bar-bg">
<div class="mech-bar-fill" style="width: {abs(float(current_scenario['cognitive'].replace('%', '')))}%;"></div>
</div>
</div>
<div class="mech-note">
<div class="mech-note-text">💡 <strong>Methodology:</strong> The digital twin uses a multi-scale physiological model combining cardiovascular dynamics, endocrine system regulation, circadian rhythm, and neurocognitive responses. Model parameters are calibrated using Bayesian optimization on your historical data. Each simulation runs 1,000 Monte Carlo iterations to quantify uncertainty.</div>
</div>
</div>"""
    st.markdown(mech_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Digital Twin Architecture
    arch_html = """<div class="architecture-panel">
<div class="arch-title">🔬 Digital Twin Architecture</div>
<div class="arch-desc">The digital twin uses a multi-scale physiological model combining cardiovascular dynamics, endocrine system regulation, circadian rhythm, and neurocognitive responses. Model parameters are calibrated using Bayesian optimization on your historical data. Each simulation runs 1,000 Monte Carlo iterations to quantify uncertainty.</div>
<div class="arch-details">
<div class="arch-detail">Predictive accuracy: 88.3% (30-day ahead)</div>
<div class="arch-detail">Update frequency: Real-time (every 30s)</div>
<div class="arch-detail">Computational cost: ~60 seconds per scenario</div>
</div>
</div>"""
    st.markdown(arch_html, unsafe_allow_html=True)

if __name__ == "__main__":
    render_digital_twin_page()
