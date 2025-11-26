import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.science_logic import calculate_sri
import time
import os
import random
from datetime import datetime
import math

# ==========================================
# SYMBIOME APP CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Symbiome | AI Resilience Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ==========================================
# CSS & ASSETS
# ==========================================
def load_css():
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: style.css not found at {css_path}")

load_css()

# ==========================================
# SESSION STATE MANAGEMENT
# ==========================================
if 'show_coach' not in st.session_state:
    st.session_state.show_coach = True # Default open for demo
if 'biofeedback_active' not in st.session_state:
    st.session_state.biofeedback_active = False
if 'hydration_active' not in st.session_state:
    st.session_state.hydration_active = False
if 'tip_index' not in st.session_state:
    st.session_state.tip_index = 0
if 'live_mode' not in st.session_state:
    st.session_state.live_mode = False

# --- DYNAMIC DATA SIMULATION ---
def simulate_live_data():
    """Generates 'live' biometric data with natural fluctuations."""
    now = time.time()
    # Create a sine wave fluctuation based on time for "breathing" effect
    fluctuation = (random.random() - 0.5) * 5
    
    # Base values with noise
    hrv = 65 + (10 * math.sin(now / 10)) + fluctuation
    gsr = 12 + (2 * math.cos(now / 15)) + (fluctuation / 2)
    facial = 85 + fluctuation
    temp = 36.6 + (random.random() - 0.5) * 0.2
    ph = 7.35 + (random.random() - 0.5) * 0.05
    
    return hrv, gsr, facial, temp, ph

# Get live data
live_hrv, live_gsr, live_facial, live_temp, live_ph = simulate_live_data()
current_sri = int(calculate_sri(live_hrv, live_gsr, live_facial))

# --- AI COACH TIPS ---
# --- AI COACH TIPS ---
tips = [
    {"title": "Maintain Balance", "text": "Good resilience! A quick coherent breathing session (1-2 min) can push you into optimal range."},
    {"title": "Hydration Alert", "text": "Your GSR indicates mild dehydration. Drinking 200ml of water can improve cognitive focus by 12%."},
    {"title": "Circadian Sync", "text": "Light exposure now will boost your cortisol awakening response for better energy tomorrow."},
    {"title": "Vagal Tone", "text": "Humming for 60 seconds stimulates the Vagus nerve and lowers heart rate instantly."},
    {"title": "Screen Fatigue", "text": "Blink rate has decreased. Look at an object 20ft away for 20 seconds to reset eye strain."},
    {"title": "Flow State", "text": "HRV coherence is high. You are in an optimal state for deep work and complex problem solving."},
    {"title": "Cortisol Flush", "text": "A 5-minute walk can lower circulating cortisol levels by up to 20%, restoring mental clarity."},
    {"title": "Sleep Debt", "text": "Recovery metrics suggest sleep debt. A 20-min power nap now can restore alertness without grogginess."},
    {"title": "Nutrient Timing", "text": "Glucose levels are stable. Ideal time for complex cognitive tasks before the post-prandial dip."},
    {"title": "Breath Focus", "text": "Box breathing (4-4-4-4) for 2 minutes can reduce acute stress response by 40%."},
    {"title": "Social Coherence", "text": "Positive social interaction releases oxytocin, which directly counteracts cortisol effects."},
    {"title": "Thermal Regulation", "text": "Slightly lowering ambient temperature can improve focus and alertness during mental work."},
    {"title": "Posture Check", "text": "Upright posture increases testosterone and decreases cortisol compared to slouching."},
    {"title": "Binaural Beats", "text": "Listening to 40Hz binaural beats can enhance focus and memory retention."},
    {"title": "Blue Light", "text": "Reduce blue light exposure 2 hours before bed to protect melatonin production."},
    {"title": "Gratitude", "text": "Practicing gratitude for 2 minutes increases HRV and emotional resilience."},
    {"title": "Nature Exposure", "text": "Viewing fractals in nature (trees, leaves) reduces stress markers by up to 60%."}
]

def next_tip():
    st.session_state.tip_index = (st.session_state.tip_index + 1) % len(tips)

def toggle_coach():
    st.session_state.show_coach = not st.session_state.show_coach

def start_biofeedback():
    st.session_state.biofeedback_active = True
    st.toast("Biofeedback Sensors Calibrated", icon="🧬")

def start_hydration():
    st.session_state.hydration_active = True

def toggle_live_mode():
    st.session_state.live_mode = not st.session_state.live_mode

# ==========================================
# MAIN DASHBOARD LAYOUT
# ==========================================

# --- NAVIGATION BAR ---
st.markdown("""
<div class="nav-container">
    <a href="#" class="nav-item active">Dashboard</a>
    <a href="#" class="nav-item">Monitor</a>
    <a href="#" class="nav-item">Training</a>
    <a href="#" class="nav-item">Digital Twin</a>
    <a href="#" class="nav-item">Journal</a>
    <a href="#" class="nav-item">Research</a>
    <a href="#" class="nav-item">Community</a>
</div>
""", unsafe_allow_html=True)

# --- HEADER ---
c1, c2 = st.columns([3, 1])
with c1:
    st.markdown("# Symbiome Resilience System")
    st.markdown("AI-Powered Biological Intelligence Platform")
with c2:
    # Live Mode Toggle
    if st.button(f"{'🔴 STOP LIVE' if st.session_state.live_mode else '🟢 GO LIVE'}", use_container_width=True):
        toggle_live_mode()
        st.rerun()
    
    if st.session_state.live_mode:
        st.caption("Live Monitoring Active: Auto-refreshing...")
        time.sleep(3) # Simulate 3s refresh rate
        st.rerun()

st.markdown("---")

# --- SECTION 1: HERO (SRI GAUGE) ---
# Dynamic Status Text
if current_sri >= 75:
    sri_color, status_text, glow_color = "#00f2fe", "OPTIMAL STATE", "rgba(0, 242, 254, 0.6)"
    advice_text = "System functioning at peak efficiency. Engage in high-focus tasks."
elif current_sri >= 50:
    sri_color, status_text, glow_color = "#f2c94c", "BALANCED", "rgba(242, 201, 76, 0.6)"
    advice_text = "Your resilience is stable. Small adjustments can optimize performance."
else:
    sri_color, status_text, glow_color = "#ff4b1f", "HIGH STRESS", "rgba(255, 75, 31, 0.6)"
    advice_text = "System load high. Recommended: 5-minute recovery break."

col_hero_1, col_hero_2, col_hero_3 = st.columns([1, 2, 1])

with col_hero_2:
    st.markdown(f"""
    <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; margin: 40px 0;">
        <div style="
            width: 260px; height: 260px; 
            border-radius: 50%; 
            background: conic-gradient({sri_color} {current_sri}%, rgba(255,255,255,0.05) 0);
            display: flex; justify-content: center; align-items: center;
            box-shadow: 0 0 80px {glow_color};
            animation: pulse-glow 3s infinite;
        ">
            <div style="
                width: 240px; height: 240px; 
                background: #050511; 
                border-radius: 50%;
                display: flex; flex-direction: column;
                justify-content: center; align-items: center;
            ">
                <span style="font-size: 5rem; font-weight: 700; color: white; line-height: 1;">{current_sri}</span>
                <span style="font-size: 1rem; color: #94a3b8; letter-spacing: 2px; margin-top: 10px;">SRI SCORE</span>
            </div>
        </div>
        <div style="margin-top: 25px; font-size: 1.5rem; font-weight: 700; color: {sri_color}; letter-spacing: 3px; text-shadow: 0 0 20px {glow_color};">
            {status_text}
        </div>
        <div style="color: #64748b; margin-top: 5px; text-align: center;">{advice_text}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Biofeedback Button Logic
    if st.session_state.biofeedback_active:
        st.success("✅ Biofeedback Session Active")
        st.progress(65, text="Calibrating Sensors...")
    else:
        # Using a target-like unicode symbol to match the mockup
        st.button("◎ START BIOFEEDBACK SESSION", on_click=start_biofeedback, type="primary", use_container_width=True)

# --- SECTION 2: REAL-TIME BIOMETRICS STRIP ---
st.markdown("### ⚡ Real-Time Biological Readings")
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Heart Rate", f"{int(live_hrv)}", "bpm", "#ff4b1f"),
    ("GSR (Stress)", f"{live_gsr:.1f}", "µS", "#f2c94c"),
    ("pH Level", f"{live_ph:.2f}", "pH", "#00f2fe"),
    ("Temperature", f"{live_temp:.1f}", "°C", "#a8ff78")
]

for col, (label, val, unit, color) in zip([m1, m2, m3, m4], metrics):
    with col:
        st.markdown(f"""
        <div class="glass-card">
            <div class="metric-label">{label}</div>
            <div style="display: flex; align-items: baseline;">
                <span class="metric-value" style="font-size: 2.2rem;">{val}</span>
                <span style="color: {color}; margin-left: 5px; font-weight: 600;">{unit}</span>
            </div>
            <div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); margin-top: 15px; border-radius: 2px;">
                <div style="width: {int(float(val)/100*100) if label != 'pH Level' else 70}%; height: 100%; background: {color}; border-radius: 2px; box-shadow: 0 0 10px {color};"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- SECTION 3: BEHAVIORAL FEEDBACK LOOP ---
st.markdown("### 🔄 Behavioral Feedback Loop")

# Hydration/Break Tips
hydration_tips = [
    {"title": "💧 Hydration Break", "text": "Your pH is slightly acidic. Drink 250ml of alkaline water.", "meta": "⏱️ 2 min • ⚖️ Balances pH levels"},
    {"title": "🧠 Brain Boost", "text": "Cognitive fatigue detected. Take 500mg of Lion's Mane mushroom extract.", "meta": "⏱️ 1 min • 🍄 Neurogenesis support"},
    {"title": "👀 Vision Reset", "text": "Digital eye strain high. Practice the 20-20-20 rule immediately.", "meta": "⏱️ 2 min • 👁️ Reduces myopia risk"},
    {"title": "🫁 Oxygen Flood", "text": "SpO2 levels slightly low. Do 30 rounds of Wim Hof breathing.", "meta": "⏱️ 5 min • ⚡ Alkalizes blood"},
    {"title": "🧘‍♀️ Micro-Meditation", "text": "Alpha waves low. Close eyes and focus on breath sensation.", "meta": "⏱️ 3 min • 🌊 Restores focus"}
]

if 'hydration_index' not in st.session_state:
    st.session_state.hydration_index = 0

def cycle_hydration_advice():
    st.session_state.hydration_index = (st.session_state.hydration_index + 1) % len(hydration_tips)
    # Also trigger the "Active" state for visual feedback
    st.session_state.hydration_active = True
    # In a real app, this might start a timer, but for now we just show the active state
    # We can toggle it back off after a delay if we had a proper async loop, 
    # but for this interaction, let's just let the user click "Next" to cycle.

current_hydro_tip = hydration_tips[st.session_state.hydration_index]

# Hydration Card with Button Logic
c_hydro_1, c_hydro_2 = st.columns([3, 1])
with c_hydro_1:
    st.markdown(f"""
    <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
        <div style="font-weight: 600; font-size: 1.1rem; color: white; margin-bottom: 5px;">{current_hydro_tip['title']}</div>
        <div style="color: #94a3b8;">{current_hydro_tip['text']}</div>
        <div style="font-size: 0.8rem; color: #00f2fe; margin-top: 10px;">{current_hydro_tip['meta']}</div>
    </div>
    """, unsafe_allow_html=True)
with c_hydro_2:
    st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True) # Spacer
    # We change the button to "Next Advice" to allow cycling
    st.button("Next Advice", on_click=cycle_hydration_advice, use_container_width=True)

# --- SECTION 4: DETAILED AI PREDICTION ENGINE ---
st.markdown("### 🔮 AI Prediction Engine")

# Main AI Insight Card
st.markdown(f"""
<div class="glass-card" style="background: linear-gradient(135deg, rgba(118, 75, 162, 0.2) 0%, rgba(24, 24, 27, 0.5) 100%); border: 1px solid rgba(118, 75, 162, 0.4);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 1.1rem; font-weight: 700; color: white;">✨ AI Insight</div>
        <div style="background: #e11d48; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700;">LIVE</div>
    </div>
    <div style="font-size: 1.2rem; color: #e2e8f0; margin-bottom: 10px;">{advice_text}</div>
    <div style="color: #a855f7; font-size: 0.9rem; font-weight: 600;">Confidence: {random.randint(88, 95)}%</div>
</div>
""", unsafe_allow_html=True)

# Detailed Metrics Grid
c_grid1, c_grid2 = st.columns(2)
with c_grid1:
    st.markdown(f"""
    <div class="ai-grid-card">
        <div class="ai-grid-label">⏱️ Expected Recovery</div>
        <div class="ai-grid-value">{random.uniform(3.5, 5.5):.1f} min</div>
        <div style="font-size: 0.7rem; color: #10b981;">↑ 19% from last week</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="ai-grid-card">
        <div class="ai-grid-label">🎯 Peak Performance</div>
        <div class="ai-grid-value">14:00 - 16:00</div>
        <div style="font-size: 0.7rem; color: #94a3b8;">Today</div>
    </div>
    """, unsafe_allow_html=True)

with c_grid2:
    st.markdown(f"""
    <div class="ai-grid-card">
        <div class="ai-grid-label">📉 Stress Risk</div>
        <div class="ai-grid-value" style="color: {'#10b981' if current_sri > 50 else '#ff4b1f'};">{'Low' if current_sri > 50 else 'Moderate'}</div>
        <div style="font-size: 0.7rem; color: #10b981;">Stable trend</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown(f"""
    <div class="ai-grid-card">
        <div class="ai-grid-label">🤖 AI Confidence</div>
        <div class="ai-grid-value">{random.randint(90, 98)}%</div>
        <div style="font-size: 0.7rem; color: #94a3b8;">High accuracy</div>
    </div>
    """, unsafe_allow_html=True)

# Personalized Tips
st.markdown("""
<div class="glass-card" style="background: rgba(118, 75, 162, 0.1);">
    <div style="font-weight: 700; color: #d8b4fe; margin-bottom: 10px;">💡 Personalized Tips</div>
    <ul style="margin: 0; padding-left: 20px; color: #e2e8f0;">
        <li style="margin-bottom: 5px;">Maintain current exercise routine</li>
        <li style="margin-bottom: 5px;">Stress levels optimal</li>
        <li>Metabolic function excellent</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# --- SECTION 5: DID YOU KNOW? (BREATHING) ---
st.markdown("""
<div class="glass-card" style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #f59e0b;">
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
        <span style="font-size: 1.5rem; margin-right: 10px;">💡</span>
        <span style="font-weight: 700; color: #f59e0b;">Did You Know? - Breathing</span>
    </div>
    <div style="color: #cbd5e1; margin-bottom: 10px;">
        6 breaths per minute (5s in, 5s out) is the optimal rate for maximizing heart rate variability and vagal tone.
    </div>
    <div style="display: flex; gap: 5px;">
        <div style="width: 20px; height: 4px; background: #f59e0b; border-radius: 2px;"></div>
        <div style="width: 4px; height: 4px; background: #475569; border-radius: 50%;"></div>
        <div style="width: 4px; height: 4px; background: #475569; border-radius: 50%;"></div>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SECTION 6: SYSTEM ANALYSIS & TRENDS ---
st.markdown("### 📊 System Analysis & Trends")
col_radar, col_zones = st.columns([1, 1])

with col_radar:
    categories = ['Cardiovascular', 'Neurological', 'Metabolic', 'Thermal', 'Stress Resilience']
    r_values = [
        min(100, live_hrv + 20),
        min(100, live_facial),
        80,
        90,
        current_sri
    ]
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(r=r_values, theta=categories, fill='toself', line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.2)'))
    fig.update_layout(polar=dict(radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='rgba(255,255,255,0.1)'), angularaxis=dict(tickfont=dict(color='#94a3b8', size=10)), bgcolor='rgba(0,0,0,0)'), paper_bgcolor='rgba(0,0,0,0)', showlegend=False, height=300, margin=dict(l=40, r=40, t=20, b=20))
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_zones:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">7-DAY RESILIENCE TREND</div>', unsafe_allow_html=True)
    # Generate dynamic trend data
    dates = pd.date_range(end=datetime.now(), periods=7).strftime('%a')
    trend_values = [random.randint(50, 90) for _ in range(6)] + [current_sri]
    
    fig = px.area(x=dates, y=trend_values, template='plotly_dark')
    fig.update_traces(line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.1)')
    fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)', range=[0, 100]))
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 7: SIF FRAMEWORK ---
st.markdown("### 🚀 Symbiome Intelligence Framework (SIF)")
features = [
    ("Resilience Mirror", "Transform stress into art", "✨"),
    ("Digital Twin", "AI model of your physiology", "🤖"),
    ("Env × Body", "Surroundings impact analysis", "☁️"),
    ("Resilience Game", "Gamified stress control", "🎮"),
    ("Emotion Journal", "Physiological mapping", "❤️"),
    ("Stress Forecast", "Predictive weather for health", "🌧️")
]
cols = st.columns(3)
for i, (title, desc, icon) in enumerate(features):
    with cols[i % 3]:
        st.markdown(f"""
        <div class="glass-card" style="min-height: 150px; cursor: pointer;">
            <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
            <div style="font-weight: 700; color: white; margin-bottom: 5px;">{title}</div>
            <div style="font-size: 0.85rem; color: #94a3b8;">{desc}</div>
            <div style="margin-top: 10px; color: #00f2fe; font-size: 0.8rem; font-weight: 600;">EXPLORE →</div>
        </div>
        """, unsafe_allow_html=True)

# --- FOOTER ---
st.markdown("""
<div class="footer-container">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 40px;">
        <div class="footer-col" style="flex: 1; min-width: 200px;">
            <h4>✨ About Symbiome</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
                An AI-enhanced, non-invasive biofeedback platform measuring how body and environment interact to shape stress and gut-related wellbeing.
            </p>
        </div>
        <div class="footer-col" style="flex: 1; min-width: 150px;">
            <h4>Core Features</h4>
            <ul>
                <li>HRV, GSR, Facial Calm tracking</li>
                <li>Digital Twin AI prediction</li>
                <li>Environmental correlation</li>
                <li>Gut-brain axis logging</li>
            </ul>
        </div>
        <div class="footer-col" style="flex: 1; min-width: 150px;">
            <h4>Research Ethics</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
                All data is anonymized and stored securely. This platform is designed for research and educational purposes.
            </p>
            <p style="font-size: 0.8rem; color: #00f2fe; margin-top: 10px;">Privacy-first • Consent-driven • Transparent</p>
        </div>
        <div class="footer-col" style="flex: 1; min-width: 150px;">
            <h4>Future Vision</h4>
            <ul>
                <li>Symbiome Glove (BLE wearable)</li>
                <li>Cloud-based AI learning</li>
                <li>Global resilience mapping</li>
                <li>Clinical validation studies</li>
            </ul>
        </div>
    </div>
    <div class="bottom-bar">
        🏆 Built for BTYSTE & Science Competition Excellence <br>
        Multi-modal biometrics - AI prediction - Environmental correlation - Gut-brain research - Community health mapping <br>
        Symbiome Research Platform © 2025 • Advancing the science of human resilience
    </div>
</div>
""", unsafe_allow_html=True)

# --- AI COACH (INTERACTIVE & DYNAMIC) ---
# Floating Bubble CSS (Hidden button overlay)
# Floating Bubble CSS (Hidden button overlay)
# Styles are now handled in the main CSS block below using .st-key selectors

# Toggle logic
st.button("🍃", key="coach_btn", on_click=toggle_coach, type="secondary")

# Tip Popup (Styled EXACTLY like UI)
if st.session_state.show_coach:
    current_tip = tips[st.session_state.tip_index]
    
    # Render the card using HTML/CSS
    # IMPORTANT: We use a single f-string with NO indentation for the HTML content to prevent Markdown code block rendering
    st.markdown(f"""
<div class="ai-coach-card">
<div class="coach-header">
<div style="display: flex; align-items: center; gap: 12px;">
<div class="coach-icon-box">
<svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
<path d="M12 2C8.13 2 5 5.13 5 9C5 11.38 6.19 13.47 8 14.74V17C8 17.55 8.45 18 9 18H15C15.55 18 16 17.55 16 17V14.74C17.81 13.47 19 11.38 19 9C19 5.13 15.87 2 12 2ZM14 22H10C9.45 22 9 21.55 9 21V20H15V21C15 21.55 14.55 22 14 22Z" fill="#ccfbf1"/>
</svg>
</div>
<div>
<div style="font-size: 0.75rem; color: #14b8a6; font-weight: 700; letter-spacing: 1px; text-transform: uppercase;">AI Coach</div>
<div style="font-size: 1.1rem; color: white; font-weight: 700; margin-top: 2px;">Did You Know?</div>
</div>
</div>
<div style="cursor: pointer; color: #ccfbf1; font-size: 1.2rem;">✕</div>
</div>
<div class="coach-content">
{current_tip['text']}
</div>
<div class="coach-footer">
<button class="quick-session-btn">Learn More</button>
<div class="next-tip-btn-container" style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
<span style="color: #ccfbf1; font-weight: 600; font-size: 0.9rem;">Next Tip</span>
</div>
</div>
<div style="display: flex; justify-content: center; margin-top: 20px; gap: 6px;">
<div class="progress-dot {'active' if st.session_state.tip_index % 3 == 0 else ''}"></div>
<div class="progress-dot {'active' if st.session_state.tip_index % 3 == 1 else ''}"></div>
<div class="progress-dot {'active' if st.session_state.tip_index % 3 == 2 else ''}"></div>
</div>
</div>
""", unsafe_allow_html=True)
    
    # Invisible buttons to trigger logic
    # We use absolute positioning to place Streamlit buttons over the HTML design
    st.markdown("""
    <style>
    /* Toggle Button - Targeted by Key */
    .st-key-coach_btn button {
        position: fixed !important;
        bottom: 30px !important;
        right: 30px !important;
        width: 60px !important;
        height: 60px !important;
        border-radius: 50% !important;
        background: linear-gradient(135deg, #0f766e 0%, #14b8a6 100%) !important;
        color: white !important;
        font-size: 24px !important;
        border: none !important;
        box-shadow: 0 4px 20px rgba(15, 118, 110, 0.4) !important;
        z-index: 9999 !important;
        transition: transform 0.3s ease !important;
    }
    .st-key-coach_btn button:hover {
        transform: scale(1.1) !important;
        box-shadow: 0 8px 30px rgba(15, 118, 110, 0.6) !important;
    }

    /* Invisible Buttons - Targeted by Key */
    /* We use opacity: 0 to make them completely invisible but still clickable */
    /* This avoids issues where global text styles override transparency */
    .st-key-next_tip_btn button {
        position: fixed !important;
        bottom: 135px !important;
        right: 50px !important;
        opacity: 0 !important;
        z-index: 99999 !important;
        height: 30px !important;
        width: 80px !important;
    }
    .st-key-next_tip_btn button:hover {
        opacity: 0 !important;
    }

    .st-key-learn_more_btn button {
        position: fixed !important;
        bottom: 135px !important;
        right: 180px !important;
        opacity: 0 !important;
        z-index: 99999 !important;
        height: 40px !important;
        width: 120px !important;
    }
    .st-key-learn_more_btn button:hover {
        opacity: 0 !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.button("Next Tip", key="next_tip_btn", on_click=next_tip)
    if st.button("Learn More", key="learn_more_btn"):
        st.toast("Opening detailed research...", icon="📚")
        time.sleep(1)
        st.toast("Insight saved to Journal", icon="✅")

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=50)
    st.markdown("### Symbiome")
    with st.expander("📄 Scientific Documentation"):
        try:
            with open("science_whitepaper.md", "r") as f:
                st.download_button("Download Whitepaper", f, file_name="Symbiome_Whitepaper.md")
        except FileNotFoundError:
            st.error("Whitepaper file not found.")
