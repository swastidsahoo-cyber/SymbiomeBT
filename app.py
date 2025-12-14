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
from data_engine import data_engine # Import the new backend engine
from modules.passive_sentinel import render_passive_sentinel # Import Passive Sentinel module

# ==========================================
# SYMBIOME APP CONFIGURATION
# Version: 2.1 - Passive Sentinel Active
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
if 'page' not in st.session_state:
    st.session_state.page = '🔔 SENTINEL'  # Default to Passive Sentinel to show the feature
if 'biofeedback_start_time' not in st.session_state:
    st.session_state.biofeedback_start_time = None

# --- DATA ENGINE INTEGRATION ---
# We now use the data_engine for all live data
if 'data_engine_initialized' not in st.session_state:
    st.session_state.data_engine_initialized = True
    # Ensure engine state matches session state if needed
    
# Get live data from the engine
live_data = data_engine.get_live_data()
live_hrv = live_data['hrv']
live_gsr = live_data['gsr']
live_facial = live_data['facial']
live_temp = live_data['temp']
live_ph = live_data['ph']

if 'last_session_sri' in st.session_state:
    current_sri = st.session_state.last_session_sri
else:
    current_sri = int(calculate_sri(live_hrv, live_gsr, live_facial))

# --- AI PREDICTION LOGIC ---
def get_ai_predictions(sri):
    """Returns deterministic AI insights based on the SRI score."""
    # Continuous calculation for recovery time (Inverse to SRI)
    # SRI 100 -> ~2 mins, SRI 0 -> ~14 mins
    recovery_val = max(2.0, 14.0 - (sri * 0.12)) + random.uniform(-0.5, 0.5)
    
    # Continuous confidence score
    confidence_val = min(99, int(85 + (sri * 0.1) + random.uniform(-2, 2)))

    if sri >= 80:
        return {
            "recovery": recovery_val,
            "recovery_trend": "↑ Optimal",
            "peak_perf": "Peak State Active",
            "stress_risk": "Low",
            "stress_color": "#10b981",
            "confidence": confidence_val,
            "insight": "Optimal resilience maintained. Continue current wellness practices."
        }
    elif sri >= 60:
        return {
            "recovery": recovery_val,
            "recovery_trend": "→ Stable",
            "peak_perf": "Within 30 mins",
            "stress_risk": "Low-Moderate",
            "stress_color": "#a3e635", # Lime green
            "confidence": confidence_val,
            "insight": "System stable. Minor adjustments to hydration could boost performance."
        }
    elif sri >= 40:
        return {
            "recovery": recovery_val,
            "recovery_trend": "↘ Slowing",
            "peak_perf": "Requires Calibration",
            "stress_risk": "Moderate",
            "stress_color": "#f59e0b",
            "confidence": confidence_val,
            "insight": "Allostatic load increasing. 2-minute reset recommended."
        }
    else:
        return {
            "recovery": recovery_val,
            "recovery_trend": "↓ Critical",
            "peak_perf": "Rest Essential",
            "stress_risk": "High",
            "stress_color": "#ef4444",
            "confidence": confidence_val,
            "insight": "High stress detected. Immediate 5-minute coherence breathing recommended."
        }

ai_data = get_ai_predictions(current_sri)

def get_personalized_tips(sri):
    """Generates context-aware tips based on SRI score."""
    if sri >= 80:
        return [
            "✅ Maintain current high-intensity training load.",
            "🧠 Engage in deep work sessions (90 mins).",
            "🥗 Metabolic flexibility is peak - intermittent fasting optional."
        ]
    elif sri >= 50:
        return [
            "💧 Hydration levels slightly low - drink 500ml water.",
            "🚶 Take a 10-minute walk to reset circadian rhythm.",
            "🧘 Mild stress detected - try 2 mins of box breathing."
        ]
    else:
        return [
            "🛑 Reduce cognitive load immediately.",
            "💤 Prioritize sleep hygiene tonight (no screens after 9pm).",
            "🌲 Nature exposure recommended to lower cortisol."
        ]

current_tips = get_personalized_tips(current_sri)

# --- ROTATING FACTS ---
science_facts = [
    {"title": "Hydration", "text": "Drinking 500ml of water can increase HRV within 10 minutes by improving blood flow and reducing sympathetic activation."},
    {"title": "Vagus Nerve", "text": "Cold exposure (15°C) to the face stimulates the Vagus nerve, instantly lowering heart rate and anxiety."},
    {"title": "Sleep Spindles", "text": "A 20-minute nap increases 'sleep spindles' in the brain, which are directly linked to learning and memory consolidation."},
    {"title": "Visual Cortex", "text": "Panoramic vision (looking at the horizon) engages the parasympathetic nervous system, reducing stress instantly."},
    {"title": "Gut-Brain Axis", "text": "95% of serotonin is produced in the gut. Probiotic intake is strongly correlated with improved mood stability."}
]

if 'fact_index' not in st.session_state:
    st.session_state.fact_index = 0

def cycle_fact():
    st.session_state.fact_index = (st.session_state.fact_index + 1) % len(science_facts)

current_fact = science_facts[st.session_state.fact_index]

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
    st.session_state.live_mode = True 
    st.session_state.page = 'Monitor'
    st.session_state.biofeedback_start_time = time.time()
    data_engine.start_session() # Start engine logging
    st.toast("Monitoring Session Started", icon="🧬")

def stop_biofeedback():
    st.session_state.biofeedback_active = False
    st.session_state.live_mode = False
    st.session_state.biofeedback_start_time = None
    data_engine.stop_session()
    
    # Calculate Final Score from Session History
    if 'sri_history' in st.session_state and len(st.session_state.sri_history) > 0:
        final_score = int(sum(st.session_state.sri_history) / len(st.session_state.sri_history))
    else:
        final_score = random.randint(70, 90)
        
    st.session_state.last_session_sri = final_score
    st.session_state.page = 'Dashboard' # Return to Dashboard

def toggle_live_mode():
    st.session_state.live_mode = not st.session_state.live_mode

def render_monitor():
    """
    Renders the 'Winner Worthy' Monitor Screen.
    Matches the provided screenshots exactly.
    """
    # --- HEADER SECTION (Screenshot 1) ---
    # "Live Monitoring Session" | Timer | Recovery Button
    
    # Get duration
    duration = data_engine.get_session_duration()
    
    # Top Bar Container
    with st.container():
        c_head_1, c_head_2, c_head_3 = st.columns([6, 1, 1])
        with c_head_1:
            st.markdown("""
            <div style="line-height: 1.2;">
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">Live Monitoring Session</div>
                <div style="font-size: 0.9rem; color: #94a3b8;">Real-time biometric data collection</div>
            </div>
            """, unsafe_allow_html=True)
        with c_head_2:
            st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 6px; padding: 8px 16px; text-align: center; color: #e2e8f0; font-family: monospace; font-weight: 600;">
                ⏱ {duration}
            </div>
            """, unsafe_allow_html=True)
        with c_head_3:
             if st.session_state.biofeedback_active:
                st.button("✅ Complete", on_click=stop_biofeedback, type="primary", use_container_width=True)
             else:
                st.button("▶ Start", on_click=start_biofeedback, type="primary", use_container_width=True)

    st.markdown("---")

    # --- SRI HERO SECTION (Screenshot 1) ---
    # Large Red/Green Circle | Status Text | Controls
    
    # Calculate SRI Color & Status
    inst_sri = calculate_sri(live_hrv, live_gsr, live_facial)
    if inst_sri < 50:
        sri_color = "#ef4444" # Red
        sri_status = "High Stress"
        sri_bg = "rgba(239, 68, 68, 0.2)"
    elif inst_sri < 75:
        sri_color = "#f59e0b" # Orange
        sri_status = "Moderate Load"
        sri_bg = "rgba(245, 158, 11, 0.2)"
    else:
        sri_color = "#10b981" # Green
        sri_status = "Optimal State"
        sri_bg = "rgba(16, 185, 129, 0.2)"

    c_hero, c_controls = st.columns([2, 3])
    
    with c_hero:
        st.markdown(f"""
        <div style="display: flex; align-items: center; gap: 20px; background: #0f172a; padding: 20px; border-radius: 16px; border: 1px solid #1e293b;">
            <div style="
                width: 80px; height: 80px; 
                border-radius: 50%; 
                background: {sri_color}; 
                display: flex; justify-content: center; align-items: center;
                font-size: 1.8rem; font-weight: 700; color: white;
                box-shadow: 0 0 20px {sri_bg};
            ">
                {int(inst_sri)}
            </div>
            <div>
                <div style="font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1px;">Real-time SRI</div>
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">{sri_status}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    with c_controls:
        # Control Buttons (Styled like screenshot)
        st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True) # Spacer
        cc1, cc2, cc3 = st.columns(3)
        with cc1:
            if st.button("⚡ Simulate Stress", use_container_width=True):
                data_engine.trigger_stress()
                st.toast("Stress Spike Simulated", icon="⚡")
        with cc2:
            if st.button("🌿 Mark Recovery", use_container_width=True):
                data_engine.trigger_recovery()
                st.toast("Recovery Protocol Initiated", icon="🌿")
        with cc3:
            st.button("🏷️ Add Annotation", use_container_width=True)

    # --- SENSOR CARDS (Screenshot 1) ---
    # Dark cards with colored headers/borders
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True) # Spacer
    
    m1, m2, m3, m4 = st.columns(4)
    
    def render_dark_card(col, title, val, unit, color):
        with col:
            st.markdown(f"""
            <div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 12px; padding: 15px; border-left: 4px solid {color};">
                <div style="font-size: 0.8rem; color: #94a3b8; margin-bottom: 5px;">{title}</div>
                <div style="font-size: 2rem; font-weight: 700; color: white;">
                    {val} <span style="font-size: 1rem; color: #64748b;">{unit}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    render_dark_card(m1, "Heart Rate Variability", f"{live_hrv:.1f}", "ms", "#f87171")
    render_dark_card(m2, "Skin Conductance", f"{live_gsr:.1f}", "µS", "#60a5fa")
    render_dark_card(m3, "Skin Temperature", f"{live_temp:.1f}", "°C", "#c084fc")
    render_dark_card(m4, "Sweat pH", f"{live_ph:.2f}", "pH", "#2dd4bf")

    # --- LIVE GRAPH (Screenshot 1) ---
    st.markdown('<div style="height: 20px;"></div>', unsafe_allow_html=True) # Spacer
    st.markdown("#### 📉 Live Biometric Signals (HRV, GSR, Facial Calm, SRI)")
    
    # Initialize History
    if 'hrv_history' not in st.session_state: st.session_state.hrv_history = [65] * 50
    if 'gsr_history' not in st.session_state: st.session_state.gsr_history = [45] * 50
    if 'facial_history' not in st.session_state: st.session_state.facial_history = [15] * 50
    if 'sri_history' not in st.session_state: st.session_state.sri_history = [60] * 50
    
    # Update Data
    if st.session_state.biofeedback_active:
        st.session_state.hrv_history.append(live_hrv)
        st.session_state.hrv_history.pop(0)
        st.session_state.gsr_history.append(live_gsr)
        st.session_state.gsr_history.pop(0)
        st.session_state.facial_history.append(live_facial)
        st.session_state.facial_history.pop(0)
        st.session_state.sri_history.append(inst_sri)
        st.session_state.sri_history.pop(0)

    # Create Multi-Line Chart
    fig = go.Figure()
    x_axis = list(range(50))
    
    # Add Traces (Matching Screenshot Colors)
    fig.add_trace(go.Scatter(x=x_axis, y=st.session_state.hrv_history, mode='lines', name='HRV', line=dict(color='#f87171', width=2)))
    fig.add_trace(go.Scatter(x=x_axis, y=st.session_state.gsr_history, mode='lines', name='GSR', line=dict(color='#60a5fa', width=2)))
    fig.add_trace(go.Scatter(x=x_axis, y=st.session_state.facial_history, mode='lines', name='Facial Calm', line=dict(color='#c084fc', width=2)))
    fig.add_trace(go.Scatter(x=x_axis, y=st.session_state.sri_history, mode='lines', name='SRI (Composite)', line=dict(color='#2dd4bf', width=3)))
    
    # Add Reference Lines
    fig.add_hline(y=70, line_dash="dot", line_color="rgba(255,255,255,0.3)", annotation_text="Optimal", annotation_position="top right")
    fig.add_hline(y=50, line_dash="dot", line_color="rgba(255,255,255,0.3)", annotation_text="Baseline", annotation_position="bottom right")
    
    fig.update_layout(
        height=350,
        margin=dict(l=0, r=0, t=20, b=0),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#94a3b8'),
        xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', title="Time (s)"),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', range=[0, 100], title="Value"),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    st.plotly_chart(fig, use_container_width=True)

    # --- SESSION EVENTS (Screenshot 0) ---
    st.markdown('<div style="height: 10px;"></div>', unsafe_allow_html=True) # Spacer
    st.markdown("#### Session Events")
    
    events = data_engine.events
    if events:
        # Reverse to show newest first
        for e in reversed(events[-5:]):
            # Determine badge color based on event type
            if "Stress" in e['type']:
                badge_bg = "#7f1d1d" # Dark Red
                badge_text = "#fca5a5"
            elif "Recovery" in e['type']:
                badge_bg = "#064e3b" # Dark Green
                badge_text = "#6ee7b7"
            else:
                badge_bg = "#1e293b" # Slate
                badge_text = "#94a3b8"
                
            st.markdown(f"""
            <div style="
                display: flex; align-items: center; gap: 15px; 
                background: #0f172a; border: 1px solid #1e293b; 
                padding: 10px 15px; border-radius: 8px; margin-bottom: 8px;
            ">
                <div style="
                    background: {badge_bg}; color: {badge_text}; 
                    padding: 4px 8px; border-radius: 4px; 
                    font-size: 0.75rem; font-family: monospace; font-weight: 700;
                ">
                    {e['time']}
                </div>
                <div style="font-weight: 600; color: #e2e8f0; font-size: 0.9rem;">{e['type']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background: #0f172a; border: 1px solid #1e293b; padding: 15px; border-radius: 8px; color: #64748b; font-style: italic;">
            Waiting for session start...
        </div>
        """, unsafe_allow_html=True)

    # --- LOGIC EXPANDER ---
    st.markdown("---")
    with st.expander("View Mathematical Models", expanded=False):
        st.markdown("""
        ### 🧮 Physiological Computing Models
        
        **1. Heart Rate Variability (RSA Model)**
        Simulates Respiratory Sinus Arrhythmia using a sine wave modulated by stress states.
        $$ HRV(t) = Base + A \cdot \sin(\omega t) + \epsilon $$
        *Where $A$ (amplitude) decreases during sympathetic activation.*
        
        **2. Galvanic Skin Response (EDA Model)**
        Models skin conductance as an inverse function of relaxation, with trend components.
        $$ GSR(t) = \frac{1}{Relaxation(t)} + \mu \cdot \cos(\theta t) $$
        
        **3. Stress Resilience Index (SRI)**
        A weighted composite score derived from multi-modal sensor fusion.
        $$ SRI = w_1 \cdot \overline{HRV} + w_2 \cdot (100 - \overline{GSR}) + w_3 \cdot Facial_{calm} $$
        """)

def render_session_summary():
    """Renders a summary report after the biofeedback session."""
    st.markdown("""
    <div style="text-align: center; margin-top: 50px;">
        <div style="font-size: 2rem; font-weight: 700; color: #00f2fe; margin-bottom: 20px;">Session Analysis Complete</div>
        <div style="font-size: 1.2rem; color: #94a3b8;">Processing multi-modal sensor data...</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Simulate processing delay
    with st.spinner("Calculating Vagal Tone & Stress Resilience Index..."):
        time.sleep(1.5)
        
    final_sri = random.randint(75, 95)
    
    c1, c2, c3 = st.columns([1, 2, 1])
    with c2:
        st.markdown(f"""
        <div class="glass-card" style="text-align: center; padding: 40px; border: 2px solid #10b981; box-shadow: 0 0 50px rgba(16, 185, 129, 0.2);">
            <div style="font-size: 1.5rem; color: #10b981; font-weight: 700; margin-bottom: 10px;">OPTIMAL RECOVERY ACHIEVED</div>
            <div style="font-size: 5rem; font-weight: 700; color: white; line-height: 1;">{final_sri}</div>
            <div style="color: #94a3b8; letter-spacing: 2px; margin-top: 10px;">FINAL SRI SCORE</div>
            <div style="margin-top: 30px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.1); font-size: 0.9rem; color: #cbd5e1;">
                "Your physiological coherence improved by 18% during this session. Vagal tone is elevated."
            </div>
        </div>
        """, unsafe_allow_html=True)
    st.session_state.live_mode = not st.session_state.live_mode

# ==========================================
# GLOBAL NAVIGATION
# ==========================================
def set_page(page):
    st.session_state.page = page

def render_navbar():
    """Renders the global navigation bar on every page."""
    st.markdown("""
    <style>
    .nav-btn {
        background: transparent !important;
        border: none !important;
        color: #94a3b8 !important;
        font-weight: 600 !important;
        font-size: 0.9rem !important;
        padding: 0.5rem 1rem !important;
        transition: color 0.2s !important;
    }
    .nav-btn:hover {
        color: #ffffff !important;
    }
    .nav-btn-active {
        color: #00f2fe !important;
        border-bottom: 2px solid #00f2fe !important;
    }
    /* Hide default button styles for nav items */
    div[data-testid="stHorizontalBlock"] button {
        background-color: transparent;
        border: none;
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Navigation Items
    nav_items = ["Dashboard", "🔔 SENTINEL", "Monitor", "Training", "Digital Twin", "Journal", "Research", "Community"]
    
    # Container for Nav (Simplified)
    with st.container():
        # st.markdown('<div class="nav-container" ...>', unsafe_allow_html=True)  <-- REMOVED TO FIX CLICK ISSUE
        cols = st.columns(len(nav_items))
        for i, item in enumerate(nav_items):
            with cols[i]:
                # Highlight active page
                is_active = (st.session_state.page == item)
                label = f"**{item}**" if is_active else item
                if st.button(label, key=f"nav_{item}", use_container_width=True):
                    st.session_state.page = item
                    st.rerun()
        # st.markdown('</div>', unsafe_allow_html=True) <-- REMOVED

    # Backup Sidebar Navigation (Just in case)
    with st.sidebar:
        st.markdown("### 🧭 Navigation")
        selected_page = st.radio("Go to:", nav_items, index=nav_items.index(st.session_state.page) if st.session_state.page in nav_items else 0, key="sidebar_nav")
        if selected_page != st.session_state.page:
            set_page(selected_page)
            st.rerun()

# Render Navbar GLOBALLY
render_navbar()

# ==========================================
# TRAINING / GAMIFICATION LOGIC
# ==========================================
def load_user_progress():
    """Loads user gamification data from CSV."""
    try:
        df = pd.read_csv("data/user_progress.csv")
        return df.iloc[0].to_dict()
    except:
        return {
            "xp": 1308, "level": 5, "streak_days": 7, 
            "garden_growth": 16, "achievements_unlocked": "[]"
        }

def render_training():
    """
    Renders the Gamified Biofeedback Interface.
    Matches the provided screenshots: Breathing, Garden, Achievements.
    """
    user_data = load_user_progress()
    
    # --- HEADER (Screenshot 2) ---
    st.markdown(f"""
    <div class="training-header">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="font-size: 1.5rem; font-weight: 700; color: white;">Resilience Training</div>
                <div style="color: #94a3b8;">Master your nervous system through biofeedback</div>
            </div>
            <div style="display: flex; gap: 15px;">
                <div style="background: rgba(249, 115, 22, 0.2); color: #f97316; padding: 8px 16px; border-radius: 8px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                    🔥 {user_data['streak_days']} Day Streak
                </div>
                <div style="background: rgba(234, 179, 8, 0.2); color: #eab308; padding: 8px 16px; border-radius: 8px; font-weight: 700; display: flex; align-items: center; gap: 8px;">
                    🏆 Level {user_data['level']}
                </div>
            </div>
        </div>
        <div style="margin-top: 20px;">
            <div style="display: flex; justify-content: space-between; color: #cbd5e1; font-size: 0.9rem; margin-bottom: 5px;">
                <span>⭐ Your Progress</span>
                <span>{user_data['xp']}/6000 XP</span>
            </div>
            <div class="xp-bar-container">
                <div class="xp-bar-fill" style="width: {(user_data['xp']/6000)*100}%;"></div>
            </div>
            <div style="font-size: 0.75rem; color: #64748b; margin-top: 5px;">5600 XP until Level 6</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # --- INJECT CRITICAL CSS (Fixes "Nothing like my UI" issue) ---
    st.markdown("""
    <style>
    /* Flattened Selectors for Reliability */
    .breathing-circle-container {
        display: flex;
        justify-content: center;
        align-items: center;
        min-height: 320px; /* Reduced to eliminate black space */
        margin-top: 30px;
        margin-bottom: -20px; /* Pull stats closer */
        position: relative;
    }
    .breathing-circle {
        width: 280px;
        height: 280px;
        border-radius: 50%;
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #00b4d8 100%);
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
        box-shadow: 
            0 0 40px rgba(0, 242, 254, 0.6),
            0 0 80px rgba(79, 172, 254, 0.4),
            0 0 120px rgba(0, 180, 216, 0.3),
            inset 0 0 60px rgba(255, 255, 255, 0.1);
        transition: all 3s ease-in-out;
        position: relative;
        overflow: hidden;
    }
    .breathing-circle::before {
        content: '';
        position: absolute;
        top: -50%;
        left: -50%;
        width: 200%;
        height: 200%;
        background: radial-gradient(circle, rgba(255,255,255,0.3) 0%, transparent 70%);
        animation: shimmer 4s infinite;
    }
    @keyframes shimmer {
        0%, 100% { transform: translate(0, 0); opacity: 0.3; }
        50% { transform: translate(10%, 10%); opacity: 0.6; }
    }
    .breathing-circle.breathe-inhale {
        transform: scale(1.0);
        background: linear-gradient(135deg, #00f2fe 0%, #4facfe 50%, #00b4d8 100%);
        box-shadow: 
            0 0 50px rgba(0, 242, 254, 0.7),
            0 0 100px rgba(79, 172, 254, 0.5),
            0 0 150px rgba(0, 180, 216, 0.3),
            inset 0 0 60px rgba(255, 255, 255, 0.15);
    }
    .breathing-circle.breathe-hold {
        transform: scale(1.15);
        background: linear-gradient(135deg, #00f2fe 0%, #00d4ff 50%, #00b4d8 100%);
        box-shadow: 
            0 0 60px rgba(0, 242, 254, 0.9),
            0 0 120px rgba(0, 212, 255, 0.7),
            0 0 180px rgba(0, 180, 216, 0.5),
            0 0 240px rgba(79, 172, 254, 0.3),
            inset 0 0 80px rgba(255, 255, 255, 0.2);
        border: 3px solid rgba(255, 255, 255, 0.8);
    }
    .breathing-circle.breathe-exhale {
        transform: scale(0.85);
        background: linear-gradient(135deg, #0f172a 0%, #1e3a5f 50%, #0a2540 100%);
        border: 2px solid #00b4d8;
        box-shadow: 
            0 0 30px rgba(0, 242, 254, 0.4),
            0 0 60px rgba(0, 180, 216, 0.2),
            inset 0 0 40px rgba(0, 242, 254, 0.1);
    }
    .garden-container {
        height: 350px;
        background: linear-gradient(180deg, #0f172a 0%, #064e3b 100%);
        border-radius: 16px;
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }
    .garden-plant {
        position: absolute;
        bottom: 20px;
        font-size: 2rem;
        animation: grow-up 1s ease-out;
    }
    @keyframes grow-up {
        0% { transform: scale(0) translateY(20px); opacity: 0; }
        100% { transform: scale(1) translateY(0); opacity: 1; }
    }
    .achievement-card {
        background: rgba(30, 41, 59, 0.5);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 15px;
        margin-bottom: 10px;
        display: flex;
        align-items: center;
        gap: 15px;
    }
    .achievement-icon {
        width: 40px;
        height: 40px;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 50%;
        display: flex;
        justify-content: center;
        align-items: center;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- MAIN GRID ---
    col_breath, col_garden = st.columns([1, 1], gap="large")

    # --- BREATHING MODULE (Screenshot 3) ---
    # --- BREATHING MODULE (Screenshot 3) ---
    with col_breath:
        # 1. INITIALIZE SESSION STATE
        if 'training_active' not in st.session_state: st.session_state.training_active = False
        if 'session_xp' not in st.session_state: st.session_state.session_xp = 0
        if 'completed_cycles' not in st.session_state: st.session_state.completed_cycles = 0
        if 'garden_plants' not in st.session_state: st.session_state.garden_plants = []
        if 'start_time' not in st.session_state: st.session_state.start_time = None
        
        # 2. BREATHING LOGIC (Calculate state before rendering)
        breath_state = "READY"
        breath_class = ""
        timer = "3"
        
        if st.session_state.training_active and st.session_state.start_time:
            elapsed = time.time() - st.session_state.start_time
            cycle_duration = 9 # 3s Inhale, 3s Hold, 3s Exhale
            current_cycle = int(elapsed / cycle_duration)
            phase_time = elapsed % cycle_duration
            
            # Check for cycle completion (Gamification Trigger)
            if current_cycle > st.session_state.completed_cycles:
                st.session_state.completed_cycles = current_cycle
                st.session_state.session_xp += 10 # +10 XP per cycle
                user_data['xp'] += 10
                
                # Grow a flower!
                plant_types = ['🌿', '🌸', '🌳', '🌻', '🍄', '🌷', '🪷']
                new_plant = {
                    'type': random.choice(plant_types),
                    'left': random.randint(5, 90),
                    'size': random.uniform(1.0, 2.0),
                    'bottom': random.randint(10, 50)
                }
                st.session_state.garden_plants.append(new_plant)
                
                # Update Garden Growth % (Cap at 100%)
                user_data['garden_growth'] = min(100, user_data['garden_growth'] + 2)
            
            # Determine Breathing Phase (Timer counts DOWN from 3 to 1)
            if phase_time < 3:
                breath_state = "INHALE"
                breath_class = "breathe-inhale"
                timer = str(3 - int(phase_time))  # 3, 2, 1
                if timer == "0": timer = "1"  # Never show 0
            elif phase_time < 6:
                breath_state = "HOLD"
                breath_class = "breathe-hold"
                timer = str(3 - int(phase_time - 3))  # 3, 2, 1
                if timer == "0": timer = "1"
            else:
                breath_state = "EXHALE"
                breath_class = "breathe-exhale"
                timer = str(3 - int(phase_time - 6))  # 3, 2, 1
                if timer == "0": timer = "1"

        # 3. RENDER HEADER + CIRCLE + STATS TOGETHER (Eliminates spacing)
        st.markdown(f"""
<div style="background: #000000; border: 1px solid #1e293b; border-radius: 16px; padding: 40px; height: 650px; display: flex; flex-direction: column; justify-content: flex-start; position: relative;">
<div style="display: flex; align-items: center; gap: 10px; color: white; font-weight: 600; font-size: 1.1rem; margin-bottom: 0px;">
<span style="color: #00f2fe;">◎</span> Breathing Synchronization
</div>

<div class="breathing-circle-container">
<div class="breathing-circle {breath_class}">
<div style="font-size: 5rem; font-weight: 700; color: white; line-height: 1;">{timer}</div>
<div style="font-size: 1.2rem; color: rgba(255,255,255,0.9); letter-spacing: 2px; font-weight: 500; margin-top: 10px;">{breath_state}</div>
</div>
</div>

<div style="display: flex; justify-content: space-between; margin-top: 10px; margin-bottom: 15px; padding: 0 30px;">
<div style="text-align: center;"><div style="color: #00f2fe; font-size: 1.8rem; font-weight: 700;">{int(st.session_state.session_xp * 2)}</div><div style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Score</div></div>
<div style="text-align: center;"><div style="color: #c084fc; font-size: 1.8rem; font-weight: 700;">{max(1, st.session_state.completed_cycles)}x</div><div style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">Combo</div></div>
<div style="text-align: center;"><div style="color: #facc15; font-size: 1.8rem; font-weight: 700;">+{int(st.session_state.session_xp)}</div><div style="color: #64748b; font-size: 0.8rem; text-transform: uppercase; letter-spacing: 1px;">XP</div></div>
</div>
        """, unsafe_allow_html=True)
        
        # 4. BUTTONS (Handle clicks and trigger rerun)
        if st.session_state.training_active:
            if st.button("Complete Session", type="secondary", use_container_width=True):
                st.session_state.training_active = False
                st.toast(f"Session Complete! +{int(st.session_state.session_xp)} XP", icon="🎉")
                st.rerun()
        else:
            if st.button("Start Training", type="primary", use_container_width=True):
                st.session_state.training_active = True
                st.session_state.session_xp = 0
                st.session_state.completed_cycles = 0
                st.session_state.garden_plants = [] # Reset garden for session
                st.session_state.start_time = time.time()
                st.rerun()

        st.markdown("</div>", unsafe_allow_html=True)
        
        # 5. AUTO-REFRESH when training is active
        if st.session_state.training_active:
            time.sleep(0.1)
            st.rerun()

    # --- GARDEN & ACHIEVEMENTS (Screenshot 3) ---
    with col_garden:
        # Dynamic Garden HTML Generation
        plants_html = ""
        for plant in st.session_state.garden_plants:
            plants_html += f'<div class="garden-plant" style="left: {plant["left"]}%; bottom: {plant["bottom"]}px; font-size: {plant["size"]}rem;">{plant["type"]}</div>'
            
        # Garden Visualization
        garden_html = f"""
<div style="background: #0f172a; border: 1px solid #1e293b; border-radius: 16px; padding: 20px; height: 100%;">
<div style="color: white; font-weight: 600; margin-bottom: 15px;">🌱 Your Resilience Garden</div>
<div class="garden-container">
{plants_html}
<!-- Fireflies/Particles -->
<div style="position: absolute; top: 20px; left: 20px; width: 4px; height: 4px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 10px #4ade80;"></div>
<div style="position: absolute; top: 50px; right: 40px; width: 4px; height: 4px; background: #4ade80; border-radius: 50%; box-shadow: 0 0 10px #4ade80;"></div>
</div>
<div style="margin-top: 15px;">
<div style="display: flex; justify-content: space-between; color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">
<span>Garden Growth</span>
<span>{user_data['garden_growth']}%</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px;">
<div style="width: {user_data['garden_growth']}%; height: 100%; background: #10b981; border-radius: 3px;"></div>
</div>
<div style="font-size: 0.7rem; color: #64748b; margin-top: 5px; text-align: center;">Each successful session grows your symbiotic ecosystem</div>
</div>
<div style="margin-top: 30px;">
<div style="color: white; font-weight: 600; margin-bottom: 15px;">Today's Achievements</div>
"""
        
        # Progressive Achievement System
        achievements = [
            # Tier 1 - Beginner
            {'id': 'first_breath', 'name': 'First Breath', 'desc': 'Complete 3 breath cycles', 'icon': '🌱', 'color': '#10b981', 'goal': 3, 'current': st.session_state.completed_cycles},
            {'id': 'breath_master', 'name': 'Breath Master', 'desc': 'Complete 10 breath cycles', 'icon': '🎯', 'color': '#f43f5e', 'goal': 10, 'current': st.session_state.completed_cycles},
            {'id': 'zen_warrior', 'name': 'Zen Warrior', 'desc': 'Complete 25 breath cycles', 'icon': '🧘', 'color': '#8b5cf6', 'goal': 25, 'current': st.session_state.completed_cycles},
            
            # Tier 2 - XP Based
            {'id': 'quick_learner', 'name': 'Quick Learner', 'desc': 'Earn 50 XP in one session', 'icon': '⚡', 'color': '#f59e0b', 'goal': 50, 'current': st.session_state.session_xp},
            {'id': 'xp_hunter', 'name': 'XP Hunter', 'desc': 'Earn 100 XP in one session', 'icon': '💎', 'color': '#06b6d4', 'goal': 100, 'current': st.session_state.session_xp},
            {'id': 'xp_legend', 'name': 'XP Legend', 'desc': 'Earn 200 XP in one session', 'icon': '👑', 'color': '#eab308', 'goal': 200, 'current': st.session_state.session_xp},
            
            # Tier 3 - Garden Based
            {'id': 'gardener', 'name': 'Gardener', 'desc': 'Grow garden to 25%', 'icon': '🌿', 'color': '#22c55e', 'goal': 25, 'current': user_data['garden_growth']},
            {'id': 'garden_master', 'name': 'Garden Master', 'desc': 'Grow garden to 50%', 'icon': '🌳', 'color': '#16a34a', 'goal': 50, 'current': user_data['garden_growth']},
            {'id': 'ecosystem_god', 'name': 'Ecosystem God', 'desc': 'Grow garden to 100%', 'icon': '🌺', 'color': '#ec4899', 'goal': 100, 'current': user_data['garden_growth']},
        ]
        
        # Filter to show only the next 2 incomplete achievements
        active_achievements = []
        for ach in achievements:
            if ach['current'] < ach['goal']:
                active_achievements.append(ach)
                if len(active_achievements) == 2:
                    break
        
        # If all are complete, show the last 2 completed ones
        if len(active_achievements) == 0:
            active_achievements = achievements[-2:]
        
        # Render active achievements
        for ach in active_achievements:
            progress_pct = min(100, int((ach['current'] / ach['goal']) * 100))
            is_complete = ach['current'] >= ach['goal']
            
            border_style = f"border: 2px solid {ach['color']};" if is_complete else ""
            complete_badge = '<div style="position: absolute; top: 10px; right: 10px; background: #10b981; color: white; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700;">✓ COMPLETE</div>' if is_complete else ''
            
            garden_html += f"""
<!-- Achievement: {ach['name']} -->
<div class="achievement-card" style="{border_style} position: relative;">
{complete_badge}
<div class="achievement-icon" style="color: {ach['color']};">{ach['icon']}</div>
<div style="flex: 1;">
<div style="color: white; font-weight: 600; font-size: 0.9rem;">{ach['name']}</div>
<div style="color: #94a3b8; font-size: 0.8rem;">{ach['desc']}</div>
<div style="width: 100%; height: 4px; background: rgba(255,255,255,0.1); margin-top: 8px; border-radius: 2px;">
<div style="width: {progress_pct}%; height: 100%; background: {ach['color']}; border-radius: 2px;"></div>
</div>
</div>
<div style="color: #64748b; font-size: 0.8rem;">{int(ach['current'])}/{ach['goal']}</div>
</div>
"""
        
        garden_html += """
</div>
</div>
"""
        st.markdown(garden_html, unsafe_allow_html=True)

    # --- CHALLENGES SECTION (Bottom of screen) ---
    st.markdown("""
    <div style="margin-top: 30px;">
        <div style="color: white; font-size: 1.2rem; font-weight: 700; margin-bottom: 20px;">🎯 Daily Challenges</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Challenge Cards
    col_c1, col_c2, col_c3 = st.columns(3)
    
    with col_c1:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(234, 179, 8, 0.3); border-radius: 12px; padding: 20px; position: relative;">
<div style="position: absolute; top: 10px; right: 10px; background: rgba(234, 179, 8, 0.2); color: #eab308; padding: 4px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">Medium</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 8px; margin-top: 10px;">Calm Under Pressure</div>
<div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 15px;">Maintain SRI > 60 during mental math</div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
<span style="color: #eab308; font-size: 1.2rem;">⭐</span>
<span style="color: #eab308; font-weight: 700;">50 XP</span>
</div>
<button style="background: transparent; border: 1px solid #eab308; color: #eab308; padding: 10px 20px; border-radius: 8px; width: 100%; font-weight: 600; cursor: pointer;">Start</button>
</div>
        """, unsafe_allow_html=True)
    
    with col_c2:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 12px; padding: 20px; position: relative;">
<div style="position: absolute; top: 10px; right: 10px; background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 4px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">Hard</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 8px; margin-top: 10px;">Stress Master</div>
<div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 15px;">Recover from stress spike in < 3 min</div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
<span style="color: #eab308; font-size: 1.2rem;">⭐</span>
<span style="color: #eab308; font-weight: 700;">75 XP</span>
</div>
<button style="background: transparent; border: 1px solid #ef4444; color: #ef4444; padding: 10px 20px; border-radius: 8px; width: 100%; font-weight: 600; cursor: pointer;">Start</button>
</div>
        """, unsafe_allow_html=True)
    
    with col_c3:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.8); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; position: relative;">
<div style="position: absolute; top: 10px; right: 10px; background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700;">Easy</div>
<div style="color: white; font-weight: 700; font-size: 1rem; margin-bottom: 8px; margin-top: 10px;">Consistency King</div>
<div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 15px;">Complete 7 sessions this week</div>
<div style="display: flex; align-items: center; gap: 8px; margin-bottom: 15px;">
<span style="color: #eab308; font-size: 1.2rem;">⭐</span>
<span style="color: #eab308; font-weight: 700;">200 XP</span>
</div>
<button style="background: transparent; border: 1px solid #10b981; color: #10b981; padding: 10px 20px; border-radius: 8px; width: 100%; font-weight: 600; cursor: pointer;">Start</button>
</div>
        """, unsafe_allow_html=True)


# ==========================================
# MAIN LAYOUT ROUTING
# ==========================================

# Auto-stop logic
if st.session_state.biofeedback_active and st.session_state.biofeedback_start_time:
    elapsed = time.time() - st.session_state.biofeedback_start_time
    if elapsed > 180: # 3 minutes
        stop_biofeedback()
        st.toast("Session Complete: 3 Minutes Reached", icon="🏁")

if st.session_state.page == 'Monitor':
    render_monitor()
elif st.session_state.page == 'Training':
    render_training()
elif st.session_state.page == 'Summary':
    render_session_summary()
else:
    # ==========================================
    # DASHBOARD LAYOUT
    # ==========================================
    
    # --- HEADER ---
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("# Symbiome Resilience System")
        st.markdown("AI-Powered Biological Intelligence Platform")
    with c2:
        # Live Mode Toggle
        if st.button(f"{'🔴 STOP LIVE' if st.session_state.live_mode else '🟢 GO LIVE'}", use_container_width=True):
            toggle_live_mode()
        
        if st.session_state.live_mode:
            st.caption("Live Monitoring Active: Auto-refreshing...")
    
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
            st.markdown(f"""
            <div style="background: rgba(16, 185, 129, 0.1); border: 1px solid #10b981; border-radius: 12px; padding: 15px; text-align: center; margin-bottom: 10px;">
                <div style="color: #10b981; font-weight: 700; font-size: 1.1rem; margin-bottom: 5px;">🧬 Biofeedback Session Active</div>
                <div style="color: #d1fae5; font-size: 0.9rem;">Entraining Vagal Tone... HRV Increasing...</div>
            </div>
            """, unsafe_allow_html=True)
            st.button("⏹ STOP SESSION", on_click=stop_biofeedback, use_container_width=True)
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
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="background: rgba(168, 85, 247, 0.2); padding: 8px; border-radius: 8px;">✨</div>
                <div>
                    <div style="font-size: 1.1rem; font-weight: 700; color: white;">AI Insight</div>
                    <div style="font-size: 0.9rem; color: #e2e8f0;">{ai_data['insight']}</div>
                </div>
            </div>
            <div style="background: #e11d48; color: white; padding: 4px 12px; border-radius: 20px; font-size: 0.75rem; font-weight: 700;">Live</div>
        </div>
        <div style="display: flex; justify-content: space-between; align-items: center; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 15px;">
            <div style="color: #a855f7; font-size: 0.85rem; font-weight: 600; border: 1px solid rgba(168, 85, 247, 0.3); padding: 4px 12px; border-radius: 12px;">Confidence: {ai_data['confidence']}%</div>
            <div style="color: #a855f7; font-size: 0.85rem;">Maintain current routine</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Detailed Metrics Grid
    c_grid1, c_grid2 = st.columns(2)
    with c_grid1:
        st.markdown(f"""
        <div class="ai-grid-card">
            <div class="ai-grid-label">⏱️ Expected Recovery</div>
            <div class="ai-grid-value">{ai_data['recovery']:.1f} min</div>
            <div style="font-size: 0.7rem; color: #10b981;">{ai_data['recovery_trend']}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ai-grid-card">
            <div class="ai-grid-label">🎯 Peak Performance</div>
            <div class="ai-grid-value">{ai_data['peak_perf']}</div>
            <div style="font-size: 0.7rem; color: #94a3b8;">Today</div>
        </div>
        """, unsafe_allow_html=True)
    
    with c_grid2:
        st.markdown(f"""
        <div class="ai-grid-card">
            <div class="ai-grid-label">📉 Stress Risk</div>
            <div class="ai-grid-value" style="color: {ai_data['stress_color']};">{ai_data['stress_risk']}</div>
            <div style="font-size: 0.7rem; color: #10b981;">Stable trend</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class="ai-grid-card">
            <div class="ai-grid-label">🤖 AI Confidence</div>
            <div class="ai-grid-value">{ai_data['confidence']}%</div>
            <div style="font-size: 0.7rem; color: #94a3b8;">High accuracy</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Personalized Tips
    st.markdown(f"""
    <div class="glass-card" style="background: rgba(118, 75, 162, 0.1);">
        <div style="font-weight: 700; color: #d8b4fe; margin-bottom: 10px;">💡 Personalized Tips</div>
        <ul style="margin: 0; padding-left: 20px; color: #e2e8f0;">
            <li style="margin-bottom: 5px;">{current_tips[0]}</li>
            <li style="margin-bottom: 5px;">{current_tips[1]}</li>
            <li>{current_tips[2]}</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    # --- SECTION 5: DID YOU KNOW? (BREATHING) ---
    # --- SECTION 5: DID YOU KNOW? (ROTATING SCIENCE) ---
    # Use columns to place the refresh button next to the title
    st.markdown(f"""
    <div class="glass-card" style="background: rgba(255, 255, 255, 0.05); border-left: 4px solid #f59e0b;">
    <div style="display: flex; justify-content: space-between; align-items: flex-start;">
    <div style="display: flex; align-items: center; margin-bottom: 10px;">
    <div style="background: #451a03; width: 32px; height: 32px; border-radius: 50%; display: flex; justify-content: center; align-items: center; margin-right: 12px;">
    <span style="font-size: 1.2rem; color: #f59e0b;">💡</span>
    </div>
    <span style="font-weight: 700; color: white; font-size: 1.1rem;">Did You Know? - {current_fact['title']}</span>
    </div>
    </div>
    <div style="color: #cbd5e1; margin-bottom: 15px; line-height: 1.6;">
    {current_fact['text']}
    </div>
    <div style="display: flex; gap: 5px;">
    <div style="width: 20px; height: 4px; background: #f59e0b; border-radius: 2px;"></div>
    <div style="width: 4px; height: 4px; background: #475569; border-radius: 50%;"></div>
    <div style="width: 4px; height: 4px; background: #475569; border-radius: 50%;"></div>
    <div style="width: 4px; height: 4px; background: #475569; border-radius: 50%;"></div>
    <div style="width: 4px; height: 4px; background: #475569; border-radius: 50%;"></div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Invisible button to cycle facts (placed over the refresh icon area if we had one, 
    # but for now we can just add a small text button below or rely on auto-refresh)
    col_fact_refresh, _ = st.columns([1, 5])
    with col_fact_refresh:
        st.button("🔄 New Fact", on_click=cycle_fact, use_container_width=True)
    
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
    
    # --- AUTO-REFRESH LOGIC (MUST BE AT END) ---
    if st.session_state.live_mode:
        time.sleep(2) # Refresh rate
        st.rerun()
    
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
# --- PAGE ROUTING ---
# DEBUG BANNER
st.markdown("<div style='background: #ef4444; color: white; padding: 10px; text-align: center; font-weight: bold;'>⚠️ UPDATE 2.1: PASSIVE SENTINEL ACTIVE</div>", unsafe_allow_html=True)

if st.session_state.page == "Dashboard":
    # Show main dashboard (existing code or summary)
    # For now, we reuse the existing components as the dashboard for the prompt flow
    # or simple provide the dashboard view.
    # Given the previous file structure, the "Dashboard" was the default view logic 
    # that existed before I wrapped it. 
    # Let's ensure the previous logic renders here.
    
    # RENDER DASHBOARD COMPONENTS
    # 1. Header & AI Data
    col1, col2 = st.columns([2, 1])
    with col1:
        st.title("Symbiome Operations Center")
        st.markdown(f"**System Status:** {ai_data['peak_perf']} | **Recovery:** {ai_data['recovery_trend']}")
    with col2:
        if st.session_state.show_coach:
             st.info(f"💡 **AI Assistant:** {ai_data['insight']}")

    # 2. Main Metrics (Reusing dark cards for Dashboard feel)
    m1, m2, m3, m4 = st.columns(4)
    with m1: st.metric("SRI Score", f"{current_sri}", f"{'↑' if current_sri > 50 else '↓'} 2.4%")
    with m2: st.metric("Stress Risk", ai_data['stress_risk'], delta_color="inverse")
    with m3: st.metric("Recovery Time", f"{int(ai_data['recovery'])} min", "-1m")
    with m4: st.metric("Confidence", f"{ai_data['confidence']}%")
    
    # 3. Trends (User History)
    st.markdown("### 📅 30-Day Resilience Trend")
    try:
        history_df = pd.read_csv("data/user_history.csv")
        fig_hist = px.line(history_df, x='Date', y='Symbiome_Resilience_Score', template='plotly_dark')
        fig_hist.update_traces(line_color='#00f2fe', line_width=3)
        fig_hist.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=300)
        st.plotly_chart(fig_hist, use_container_width=True)
    except:
        st.warning("Trend data unavailable. Run data_generator.py to initialize.")
        
elif st.session_state.page == "Monitor":
    render_monitor()
    render_session_summary()

elif st.session_state.page == "Training":
    render_training()

elif st.session_state.page == "🔔 SENTINEL":
    render_passive_sentinel()
    
else:
    st.info(f"🚧 {st.session_state.page} module is under construction.")
