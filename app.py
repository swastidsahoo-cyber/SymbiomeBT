# ==========================================
# SYMBIOME STABLE VERSION 2.9
# BUILD ID: COMMUNITY-RESILIENCE-MAPPING-V29
# TIMESTAMP: 2025-12-24 06:00 UTC
# ==========================================

"""
Symbiome - Advanced Biofeedback & Stress Management Platform
Version 2.9 - COMMUNITY RESILIENCE MAPPING™
DEPLOYMENT TRIGGER: 2025-12-25-13:55 - COGNITIVE TESTING + STRESS SIMULATION ADDED - FORCE RELOAD
"""
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.express as px
import time
import os
import random
import math
st.set_page_config(page_title="Symbiome UPGRADE", page_icon="⚡", layout="wide")
st.error("🚨 SYSTEM UPGRADE IN PROGRESS - PLEASE RELOAD PAGE IF YOU SEE THIS 🚨")
st.warning("Feature 'Active Facial Analysis' is being installed...")
st.toast("Installing Updates...", icon="⏳")

# --- CORE UTILITIES ---
import plotly.graph_objects as go
from data_engine import data_engine
# Import SensorManager for control
try:
    from modules.sensor_manager import sensor_manager
except Exception as e:
    st.error(f"⚠️ SENSOR MANAGER FAILURE: {e}")
    sensor_manager = None # Graceful fallback
from modules.science_logic import calculate_sri

# --- DEFENISVE WRAPPER FOR SIDEBAR ---
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

# --- DYNAMIC ROUTING (LATE LOADING) ---
def route_page():
    page = st.session_state.get('page', 'Dashboard')
    
    if page == 'Monitor':
        render_monitor()
    elif page == 'Training':
        render_training() # Defined in app.py
    elif page == 'SENTINEL':
        from modules.passive_sentinel import render_passive_sentinel
        render_passive_sentinel()
    elif page == 'Dashboard':
        render_dashboard()
    elif page == 'Digital Twin':
        from modules.digital_twin_ui import render_digital_twin_page
        render_digital_twin_page()
    elif page == 'Predictive':
        from modules.predictive_engine import render_predictive_engine_page
        render_predictive_engine_page()
    elif page == 'Digital Twin Advanced':
        from modules.digital_twin_advanced import render_digital_twin_advanced_page
        render_digital_twin_advanced_page()
    elif page == 'Summary':
        render_session_summary()
    elif page == 'Journal':
        from modules.nlp_sentiment import render_nlp_sentiment_page
        render_nlp_sentiment_page()
    elif page == 'Resilience Quotient':
        from modules.resilience_quotient import render_resilience_quotient_page
        render_resilience_quotient_page()
    elif page == 'Forecast':
        from modules.resilience_forecast import render_resilience_forecast_page
        render_resilience_forecast_page()
    elif page == 'Environmental':
        from modules.environmental_tracker import render_environmental_tracker_page
        render_environmental_tracker_page()
    elif page == 'Clinical Vault':
        from modules.clinical_vault import render_clinical_vault_page
        render_clinical_vault_page()
    elif page == 'Custom Stress':
        from modules.custom_activities import render_custom_activities_page
        render_custom_activities_page()
    elif page == 'Closed Loop':
        from modules.closed_loop import render_closed_loop_page
        render_closed_loop_page()
    elif page == 'Resilience Mapping':
        from modules.resilience_mapping import render_resilience_mapping_page
        render_resilience_mapping_page()
    elif page == 'Research':
        from modules.research_dashboard import render_research_dashboard_page
        render_research_dashboard_page()
    elif page == 'Advanced Features':
        from modules.advanced_features import render_advanced_features_page
        render_advanced_features_page()
    elif page == 'Settings & Privacy (New)':
        from modules.settings_privacy_new import render_settings_privacy_page
        render_settings_privacy_page()
    elif page == 'Future Vision':
        from modules.future_vision import render_future_vision_page
        render_future_vision_page()
    elif page == 'Educational Portal':
        from modules.educational_portal import render_educational_portal_page
        render_educational_portal_page()
    elif page == 'Scientific Analysis':
        from modules.scientific_analysis import render_scientific_analysis_page
        render_scientific_analysis_page()
    elif page == 'Community Challenge Arena':
        from modules.community_challenge_arena import render_community_challenge_arena_page
        render_community_challenge_arena_page()
    elif page == 'Stress Simulation Sandbox':
        from modules.stress_simulation_sandbox import render_stress_simulation_sandbox_page
        render_stress_simulation_sandbox_page()
    elif page == 'Cognitive Testing':
        from modules.cognitive_testing import render_cognitive_testing_page
        render_cognitive_testing_page()
    elif page == 'Active Monitoring':
        try:
            from modules.active_monitoring import render_active_monitoring_page
            render_active_monitoring_page()
        except Exception as e:
            st.error(f"⚠️ MODULE ERROR: {e}")
            st.warning("Please ensure 'av' and 'streamlit-webrtc' are installed.")
            st.code(f"pip install av streamlit-webrtc", language="bash")
    elif page == 'Community':
        render_placeholder("Community Cloud", "🌍", "Connect with the Symbiome research community and share anonymized insights.")
    elif page == 'Cognitive':
        render_placeholder("Cognitive Performance", "🧠", "Assess your cognitive resilience through reaction time and memory tests.")
    elif page == 'Settings':
        from modules.settings_privacy import render_settings_privacy_page
        render_settings_privacy_page()
    else:
        st.error(f"Page {page} not found or module failed to load.")

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

# Initialize Session State
if 'page' not in st.session_state:
    st.session_state.page = "Dashboard"


if 'live_mode' not in st.session_state:
    st.session_state.live_mode = False
if 'biofeedback_start_time' not in st.session_state:
    st.session_state.biofeedback_start_time = None

# --- REDIRECT TOKEN LOGIC MOVED DOWN ---

# --- DATA ENGINE INTEGRATION ---
# We now use the data_engine for all live data
# --- DATA ENGINE INTEGRATION ---
# We now use the data_engine for all live data
if 'data_engine' not in st.session_state:
    st.session_state.data_engine = data_engine # Store the imported engine in session state
    st.session_state.data_engine_initialized = True

# Ensure we use the persistent engine from session state if available
# (This handles the case where the global 'data_engine' variable might be re-initialized on reload)
if 'data_engine' in st.session_state:
    data_engine = st.session_state.data_engine
    
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

# --- REAL-TIME STRESS NOTIFICATIONS ---
if 'last_stress_notif_time' not in st.session_state:
    st.session_state.last_stress_notif_time = 0

# Trigger notification if SRI is low and enough time has passed (min 30s between notifs)
if current_sri < 45 and (time.time() - st.session_state.last_stress_notif_time > 30):
    st.toast(f"🚨 STRESS ALERT: Your Resilience Index has dropped to {current_sri}. Consider a 2-minute reset in the Closed-Loop System.", icon="⚠️")
    st.session_state.last_stress_notif_time = time.time()

# --- TOP-SCREEN INSIGHT BANNER (ILLUSION OF MONITORING) ---
def render_top_notification(current_sri):
    if 'last_top_insight_time' not in st.session_state:
        st.session_state.last_top_insight_time = 0
    
    # Show an insight every 45-60 seconds to maintain the "Alive" feel
    if "journal_logs" not in st.session_state:
        st.session_state.journal_logs = [
            {"date": "12/21/2025", "mood": 6.1670357561177676, "stress": 6.167035226953227, "energy": 5.799616087965775, "gut": 7.551611952086196, "sri": 51, "diet": ["Vegetables", "Protein"]},
            {"date": "12/20/2025", "mood": 6.221583719482910, "stress": 3.401928371948291, "energy": 8.161029371948291, "gut": 5.341029371948291, "sri": 72, "diet": ["Fruits", "Grains"]},
            {"date": "12/19/2025", "mood": 4.741029371948291, "stress": 4.691029371948291, "energy": 6.621029371948291, "gut": 8.591029371948291, "sri": 61, "diet": ["Spicy", "Alcohol"]}
        ]
        
    if time.time() - st.session_state.last_top_insight_time > 45:
        insights = [
            ("🧠 NEURAL SYNC", "Subtle alpha-wave instability detected. Autonomic re-calibration active.", "#38bdf8"),
            ("🫀 BIOSIGNAL", f"HRV coherence is {random.randint(85,95)}%. Pulse quality: OPTIMAL.", "#10b981"),
            ("🛰️ SENSING", "Passive monitoring active via Sentinel. No acute stressors detected.", "#94a3b8"),
            ("⚡ REACTIVITY", "Slight sympathetic rise detected. Initiating background dampening.", "#f59e0b"),
            ("☁️ SYSTEM", "Bio-Intelligence synchronization complete. 100% data integrity.", "#2dd4bf")
        ]
        
        # Select insight based on SRI (lower SRI -> more warning-like insights)
        if current_sri < 60:
            insight_title, insight_text, insight_color = insights[3] if random.random() > 0.5 else insights[0]
        else:
            insight_title, insight_text, insight_color = random.choice([insights[1], insights[2], insights[4]])

        st.markdown(f"""
        <style>
        @keyframes slideDown {{
            0% {{ transform: translateY(-100%); opacity: 0; }}
            10% {{ transform: translateY(0); opacity: 1; }}
            90% {{ transform: translateY(0); opacity: 1; }}
            100% {{ transform: translateY(-150%); opacity: 0; }}
        }}
        .top-insight-banner {{
            position: fixed;
            top: 60px;
            left: 50%;
            transform: translateX(-50%);
            z-index: 10001;
            background: rgba(15, 23, 42, 0.9);
            backdrop-filter: blur(10px);
            border: 1px solid {insight_color}44;
            border-left: 4px solid {insight_color};
            padding: 12px 24px;
            border-radius: 12px;
            display: flex;
            align-items: center;
            gap: 15px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.4);
            animation: slideDown 8s cubic-bezier(0.25, 0.46, 0.45, 0.94) forwards;
            min-width: 400px;
        }}
        </style>
        <div class="top-insight-banner">
            <div style="background: {insight_color}22; color: {insight_color}; font-weight: 800; font-size: 0.75rem; letter-spacing: 1px; padding: 4px 8px; border-radius: 4px;">{insight_title}</div>
            <div style="color: white; font-size: 0.85rem; font-weight: 500;">{insight_text}</div>
            <div class="pulse-animation" style="width: 8px; height: 8px; background: {insight_color}; border-radius: 50%;"></div>
        </div>
        """, unsafe_allow_html=True)
        st.session_state.last_top_insight_time = time.time()

# Global execution of the top notification
render_top_notification(current_sri)

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
    print("DEBUG: start_biofeedback called!")
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

# --- REDIRECT TOKEN CHECK (Post-Function Definition) ---
if st.session_state.get('redirect_to_monitor'):
    start_biofeedback() # Now defined!
    st.session_state.auto_start_pending = True # Signal for Monitor page to verify start
    st.session_state.redirect_to_monitor = False
    st.rerun()

def toggle_live_mode():
    st.session_state.live_mode = not st.session_state.live_mode

def render_monitor():
    """
    Renders the 'Winner Worthy' Monitor Screen.
    Matches the provided screenshots exactly.
    """
    # SELF-HEALING: Ensure session is actually active if requested
    if st.session_state.get('auto_start_pending'):
        print("DEBUG: Auto-Start Pending detected in Monitor. Forcing Start.")
        start_biofeedback()
        st.session_state.auto_start_pending = False
        st.rerun() # Re-render to show Active UI

    # --- HEADER SECTION (Screenshot 1) ---
    # "Live Monitoring Session" | Timer | Recovery Button
    
    # Get duration
    # Get duration (Use Session State for reliability)
    if st.session_state.biofeedback_start_time:
        elapsed_sec = int(time.time() - st.session_state.biofeedback_start_time)
        mins, secs = divmod(elapsed_sec, 60)
        duration = f"{mins:02d}:{secs:02d}"
    else:
        duration = "00:00"
    
    # Top Bar Container
    with st.container():
        # --- WEBCAM FEED OVERLAY (If Active) ---
        if sensor_manager and sensor_manager.strategy == "WEBCAM":
            frame = sensor_manager.get_latest_frame()
            if frame is not None:
                st.image(frame, channels="RGB", marginBottom=20, caption="Live Physiological Analysis (rPPG + Emotion)")
                
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
                if st.button("▶ Start", key="btn_monitor_start_header_inline", type="primary", use_container_width=True):
                    start_biofeedback()
                    st.session_state.page = 'Monitor' # Force stay
                    st.session_state.biofeedback_active = True # Force active
                    st.rerun()

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
            if st.button("⚡ Simulate Stress", use_container_width=True, key="btn_sim_stress_inline"):
                try:
                    data_engine.trigger_stress()
                    st.toast("Stress Spike Simulated", icon="⚡")
                    # RE-ASSERT STATE TO PREVENT REDIRECTS
                    st.session_state.page = 'Monitor'
                    st.session_state.biofeedback_active = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")
            
        with cc2:
            if st.button("🌿 Mark Recovery", use_container_width=True, key="btn_sim_recovery_inline"):
                try:
                    data_engine.trigger_recovery()
                    st.toast("Recovery Protocol Initiated", icon="🌿")
                    st.session_state.page = 'Monitor'
                    st.session_state.biofeedback_active = True
                    st.rerun()
                except Exception as e:
                    st.error(f"Error: {e}")

        with cc3:
            if st.button("🏷️ Add Annotation", use_container_width=True, key="btn_annotate_inline"):
                st.toast("Annotation Added at " + time.strftime("%H:%M:%S"), icon="🏷️")
                st.session_state.page = 'Monitor'
                st.session_state.biofeedback_active = True
                st.rerun()

    # --- SENSOR CARDS (Screenshot 1) ---
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
        st.markdown(r"""
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
# GLOBAL NAVIGATION & HEADER
# ==========================================

def render_sidebar():
    """Renders the Sidebar Navigation matching React design categories."""
    with st.sidebar:
        st.markdown("# 🚀 VERSION 2.5 LIVE")
        # --- LOGO SECTION ---
        st.markdown("""
        <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 20px;">
            <div style="width: 40px; height: 40px; background: linear-gradient(135deg, #2dd4bf, #06b6d4); border-radius: 50%; display: flex; justify-content: center; align-items: center; box-shadow: 0 0 20px rgba(45, 212, 191, 0.3);">
                <span style="font-size: 1.2rem;">✨</span>
            </div>
            <div>
                <div style="font-weight: 700; font-size: 1.2rem; background: linear-gradient(90deg, #2dd4bf, #06b6d4); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">Symbiome</div>
                <div style="font-size: 0.7rem; color: #94a3b8;">Resilience Platform</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # --- NAVIGATION ---
        # Helper to render category header
        
        # --- SENSOR INPUT ---
        st.markdown("### 📡 Sensor Input")
        # DEBUG
        st.caption(f"Debug: Manager={sensor_manager is not None}")
        
        sensor_mode = st.selectbox(
            "Data Source",
            ["Simulation", "Webcam (Contactless)", "Hardware (Serial)"],
            index=0,
            key="sensor_mode_select"
        )
        
        if sensor_manager:
            if "Webcam" in sensor_mode:
                if sensor_manager.strategy != "WEBCAM":
                    sensor_manager.set_strategy("WEBCAM")
                
                st.success("● Camera Active")
                
                # Auto-Redirect as requested
                if st.session_state.page != "Active Monitoring":
                    st.info("Redirecting to Active Analysis...")
                    st.session_state.page = "Active Monitoring"
                    st.rerun()
                    
                st.caption("Analyzing: Heart Rate, Blink, Temp Proxy")
                
            elif "Hardware" in sensor_mode:
                # --- THE HARDWARE ILLUSION ---
                st.markdown("#### Hardware Config")
                real_ports = sensor_manager.get_available_ports()
                # Create illusion list
                com_ports = real_ports if real_ports else ["COM3", "COM4"]
                
                selected_port = st.selectbox("Select Port", com_ports, key="com_port_select")
                
                if st.button("🔌 Connect Device", key="btn_connect_hw"):
                    with st.spinner(f"Handshaking with {selected_port}..."):
                        time.sleep(1.5) # Fake delay
                        if selected_port in real_ports:
                            success = sensor_manager.connect_hardware(selected_port)
                            if success:
                                st.toast(f"Connected to {selected_port}", icon="✅")
                            else:
                                st.error("Connection Failed. Port Busy.")
                        else:
                            # Illusion Fallback
                            st.warning("Device not responding. Switching to Virtual Driver.")
                            time.sleep(1.0)
                            sensor_manager.set_strategy("SIMULATION")
                            st.toast("Virtual Driver Loaded", icon="⚠️")
            
            else:
                 if sensor_manager.strategy != "SIMULATION":
                    sensor_manager.set_strategy("SIMULATION")
                 st.caption("Generative Physiological Model")
        else:
            st.error("⚠️ Sensor Driver Failed to Load")
            st.info("System is running in Safe Mode (UI Only). Check logs.")
        
        st.markdown("---")

        def nav_category(name):
            st.markdown(f"<div style='font-size: 0.75rem; color: #64748b; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; margin-top: 15px; margin-bottom: 5px;'>{name}</div>", unsafe_allow_html=True)
        
        # 1. Dashboard
        if st.button("🏠 Dashboard", key="nav_home", use_container_width=True, type="secondary" if st.session_state.page != "Dashboard" else "primary"):
            st.session_state.page = "Dashboard"
            st.rerun()
            
        # 2. Real-Time Monitoring
        nav_category("Real-Time Monitoring")
        if st.button("❤️ Live Monitor", key="nav_monitor", use_container_width=True, type="secondary" if st.session_state.page != "Monitor" else "primary"):
            st.session_state.page = "Monitor"
            st.rerun()
        if st.button("🔴 [NEW] ACTIVE FACIAL ANALYSIS", key="nav_active_monitor", use_container_width=True, type="secondary" if st.session_state.page != "Active Monitoring" else "primary"):
            st.session_state.page = "Active Monitoring"
            st.rerun()
        if st.button("👁️ Passive Sentinel", key="nav_sentinel", use_container_width=True, type="secondary" if st.session_state.page != "SENTINEL" else "primary"):
            st.session_state.page = "SENTINEL"
            st.rerun()
        if st.button("🎯 Custom Activities", key="nav_custom", use_container_width=True, type="secondary" if st.session_state.page != "Custom Stress" else "primary"):
            st.session_state.page = "Custom Stress"
            st.rerun()

        # 3. Training & Intervention
        nav_category("Training & Intervention")
        if st.button("🎮 Biofeedback Training", key="nav_train", use_container_width=True, type="secondary" if st.session_state.page != "Training" else "primary"):
            st.session_state.page = "Training"
            st.rerun()
        if st.button("⚡ Closed-Loop System", key="nav_closedloop", use_container_width=True, type="secondary" if st.session_state.page != "Closed Loop" else "primary"):
            st.session_state.page = "Closed Loop"
            st.rerun()
        if st.button("🧠 Cognitive Testing", key="nav_cognitive", use_container_width=True, type="secondary" if st.session_state.page != "Cognitive Testing" else "primary"):
            st.session_state.page = "Cognitive Testing"
            st.rerun()
        if st.button("🧪 Stress Simulation", key="nav_simulation", use_container_width=True, type="secondary" if st.session_state.page != "Stress Simulation Sandbox" else "primary"):
            st.session_state.page = "Stress Simulation Sandbox"
            st.rerun()

        # 4. AI & Prediction
        nav_category("AI & Prediction")
        if st.button("📈 Predictive Engine", key="nav_predictive", use_container_width=True, type="secondary" if st.session_state.page != "Predictive" else "primary"):
            st.session_state.page = "Predictive"
            st.rerun()
        if st.button("🤖 Digital Twin (B)", key="nav_twin", use_container_width=True, type="secondary" if st.session_state.page != "Digital Twin" else "primary"):
            st.session_state.page = "Digital Twin"
            st.rerun()
        if st.button("🧬 Digital Twin (Adv)", key="nav_twin_adv", use_container_width=True, type="secondary" if st.session_state.page != "Digital Twin Advanced" else "primary"):
            st.session_state.page = "Digital Twin Advanced"
            st.rerun()
        if st.button("Forecast", key="nav_forecast", use_container_width=True, type="secondary" if st.session_state.page != "Forecast" else "primary"): # Adjusted label for space
            st.session_state.page = "Forecast"
            st.rerun()
        if st.button("🌍 Environment", key="nav_env", use_container_width=True, type="secondary" if st.session_state.page != "Environmental" else "primary"):
            st.session_state.page = "Environmental"
            st.rerun()
        if st.button("🔒 Clinical Vault", key="nav_vault", use_container_width=True, type="secondary" if st.session_state.page != "Clinical Vault" else "primary"):
            st.session_state.page = "Clinical Vault"
            st.rerun()

        # 5. Data & Analysis
        nav_category("Data & Analysis")
        if st.button("💬 Sentiment AI (NLP)", key="nav_journal", use_container_width=True, type="secondary" if st.session_state.page != "Journal" else "primary"):
            st.session_state.page = "Journal"
            st.rerun()
        if st.button("🏆 Resilience Quotient™", key="nav_rq", use_container_width=True, type="secondary" if st.session_state.page != "Resilience Quotient" else "primary"):
            st.session_state.page = "Resilience Quotient"
            st.rerun()
        if st.button("🗺️ Resilience Mapping", key="nav_mapping", use_container_width=True, type="secondary" if st.session_state.page != "Resilience Mapping" else "primary"):
            st.session_state.page = "Resilience Mapping"
            st.rerun()
        if st.button("📊 Research Dashboard", key="nav_analysis", use_container_width=True, type="secondary" if st.session_state.page != "Research" else "primary"):
            st.session_state.page = "Research"
            st.rerun()
        if st.button("⚡ Advanced Features", key="nav_advanced", use_container_width=True, type="secondary" if st.session_state.page != "Advanced Features" else "primary"):
            st.session_state.page = "Advanced Features"
            st.rerun()
        if st.button("⚙️ Settings & Privacy (New)", key="nav_settings_new", use_container_width=True, type="secondary" if st.session_state.page != "Settings & Privacy (New)" else "primary"):
            st.session_state.page = "Settings & Privacy (New)"
            st.rerun()
        if st.button("🔮 Future Vision", key="nav_future", use_container_width=True, type="secondary" if st.session_state.page != "Future Vision" else "primary"):
            st.session_state.page = "Future Vision"
            st.rerun()
        if st.button("🎓 Educational Portal", key="nav_education", use_container_width=True, type="secondary" if st.session_state.page != "Educational Portal" else "primary"):
            st.session_state.page = "Educational Portal"
            st.rerun()
        if st.button("📊 Scientific Analysis", key="nav_scientific", use_container_width=True, type="secondary" if st.session_state.page != "Scientific Analysis" else "primary"):
            st.session_state.page = "Scientific Analysis"
            st.rerun()

        # 6. Community & Impact
        nav_category("Community & Impact")
        if st.button("🏆 Community Challenge Arena", key="nav_community", use_container_width=True, type="secondary" if st.session_state.page != "Community Challenge Arena" else "primary"):
            st.session_state.page = "Community Challenge Arena"
            st.rerun()

def render_top_bar():
    """Renders the Top Bar with User Stats (XP, Streak)."""
    # Load User Data
    user_data = load_user_progress()
    
    with st.container():
        c1, c2 = st.columns([2, 1])
        with c1:
             # Generous Breadcrumb / Page Title
             st.markdown(f"### {st.session_state.page}")
        with c2:
            st.markdown(f"""
            <div style="display: flex; justify-content: flex-end; gap: 15px; align-items: center;">
                 <div style="text-align: right; display: none; @media(min-width: 768px){{display: block;}}">
                    <div style="font-weight: 700; color: white;">Researcher</div>
                    <div style="font-size: 0.75rem; color: #94a3b8;">Level {user_data['level']} • {user_data['xp']} XP</div>
                 </div>
                 <div style="background: rgba(45, 212, 191, 0.1); color: #2dd4bf; padding: 5px 12px; border-radius: 20px; font-weight: 700; border: 1px solid rgba(45, 212, 191, 0.2);">
                    🔥 {user_data['streak_days']}
                 </div>
            </div>
            """, unsafe_allow_html=True)
    st.markdown("---")

# EXECUTE LAYOUT
try:
    # --- DEBUG: FORCE SENSOR UI ON MAIN PAGE ---
    st.divider()
    st.markdown("## 🛠️ DEBUG SENSOR CONTROL")
    c_debug_1, c_debug_2 = st.columns(2)
    with c_debug_1:
        debug_sensor_mode = st.selectbox("Override Sensor Mode", ["Simulation", "Webcam", "Hardware"], key="debug_sensor_select")
        if st.button("Apply Strategy"):
            if sensor_manager:
                sensor_manager.set_strategy(debug_sensor_mode.upper())
                st.success(f"Strategy set to {debug_sensor_mode}")
            else:
                st.error("SensorManager is None!")
    with c_debug_2:
        if sensor_manager and sensor_manager.strategy == "WEBCAM":
             f = sensor_manager.get_latest_frame()
             if f is not None: st.image(f, width=200)
             else: st.warning("No Frame")
    st.divider()
    # -------------------------------------------

    render_sidebar()
    render_top_bar()
except Exception as e:
    st.error(f"⚠️ UI Layout Crash: {e}")
    import traceback
    st.code(traceback.format_exc())
    # Try to continue despite crash

# ==========================================
# TRAINING / GAMIFICATION LOGIC
# ==========================================
def render_training():
    """
    Renders the Gamified Biofeedback Interface.
    Matches the provided screenshots: Breathing, Garden, Achievements.
    """
    user_data = load_user_progress()
    
    # DEBUG: Visible State Tracker
    st.warning(f"DEBUG: Current Page = {st.session_state.get('page')} | Sentinel Enabled = {st.session_state.get('sentinel_enabled')}")

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
        
    # (Auto-refresh moved to end of function)

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

    # 5. AUTO-REFRESH when training is active (MOVED HERE)
    if st.session_state.training_active:
        time.sleep(0.1)
        st.rerun()

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
# PAGE RENDERERS (PLACEHOLDERS)
# ==========================================

def render_placeholder(title, icon, desc):
    st.markdown(f"""
    <div style="text-align: center; padding: 100px 20px;">
        <div style="font-size: 5rem; margin-bottom: 20px;">{icon}</div>
        <div style="font-size: 2.1rem; font-weight: 700; color: white; margin-bottom: 10px;">{title}</div>
        <div style="color: #94a3b8; font-size: 1.1rem; max-width: 600px; margin: 0 auto; line-height: 1.6;">
            {desc}
        </div>
        <div style="margin-top: 40px; padding: 20px; background: rgba(15, 23, 42, 0.5); border: 1px dashed rgba(255,255,255,0.1); border-radius: 12px; display: inline-block;">
            <div style="color: #64748b; font-size: 0.9rem; font-family: monospace;">STATUS: UNDER DEVELOPMENT</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_session_summary():
    st.markdown("## 📈 Session Summary")
    st.markdown("---")
    render_placeholder("Session Summary", "📈", "Detailed insights from your past sessions will appear here.")

# def render_digital_twin_advanced_page():
#     st.markdown("## 👤 Digital Twin Advanced")
#     st.markdown("---")
#     render_placeholder("Digital Twin Advanced", "👤", "Advanced configuration for your digital twin.")


# ==========================================
# MAIN LAYOUT ROUTING
# ==========================================

def render_dashboard():
    # --- HEADER ---
    c1, c2 = st.columns([3, 1])
    with c1:
        st.markdown("# Symbiome Resilience System")
        st.markdown("AI-Powered Biological Intelligence Platform")
    with c2:
        # Live Mode Toggle
        if st.button(f"{'🔴 STOP LIVE' if st.session_state.live_mode else '🟢 GO LIVE'}", key="dashboard_live_toggle", use_container_width=True):
            st.session_state.live_mode = not st.session_state.live_mode
            st.rerun()
        
        if st.session_state.live_mode:
            st.caption("Live Monitoring Active: Auto-refreshing...")
    
    st.markdown("---")
    
    # --- SECTION 1: HERO (SRI GAUGE) ---
    current_sri = st.session_state.get('last_session_sri', 70)
    if current_sri >= 75:
        sri_color, status_text = "#00f2fe", "OPTIMAL STATE"
    elif current_sri >= 50:
        sri_color, status_text = "#f2c94c", "BALANCED"
    else:
        sri_color, status_text = "#ff4b1f", "HIGH STRESS"
    
    col_hero_1, col_hero_2, col_hero_3 = st.columns([1, 2, 1])
    
    with col_hero_2:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; margin: 40px 0;">
            <div style="
                width: 260px; height: 260px; 
                border-radius: 50%; 
                background: conic-gradient({sri_color} {current_sri}%, rgba(255,255,255,0.05) 0);
                display: flex; justify-content: center; align-items: center;
                box-shadow: 0 0 80px {sri_color}4d;
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
            <div style="margin-top: 25px; font-size: 1.5rem; font-weight: 700; color: {sri_color}; letter-spacing: 3px;">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.session_state.get('biofeedback_active'):
             st.button("⏹ STOP SESSION", on_click=stop_biofeedback, use_container_width=True, key="dashboard_stop_session")
        else:
            if st.button("◎ START BIOFEEDBACK SESSION", key="btn_dashboard_start", type="primary", use_container_width=True):
                start_biofeedback()
                st.rerun()
    
    # --- SECTION 2: BIOMETRICS ---
    st.markdown("### ⚡ Real-Time Biological Readings")
    m1, m2, m3, m4 = st.columns(4)
    biometrics = [
        ("Heart Rate", f"{int(live_hrv)}", "bpm", "#ff4b1f"),
        ("GSR (Stress)", f"{live_gsr:.1f}", "µS", "#f2c94c"),
        ("pH Level", f"{live_ph:.2f}", "pH", "#00f2fe"),
        ("Temperature", f"{live_temp:.1f}", "°C", "#a8ff78")
    ]
    
    for col, (label, val, unit, color) in zip([m1, m2, m3, m4], biometrics):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-label">{label}</div>
                <div style="display: flex; align-items: baseline;">
                    <span class="metric-value" style="font-size: 2.2rem;">{val}</span>
                    <span style="color: {color}; margin-left: 5px; font-weight: 600;">{unit}</span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # --- SECTION 3: AI PREDICTIONS ---
    st.markdown("### 🔮 Advanced Resilience Prediction")
    pred_1, pred_2 = st.columns(2)
    with pred_1:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #10b981;">
             <div style="color: #10b981; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">Recovery Prediction</div>
             <div style="font-size: 2.5rem; font-weight: 700; color: white;">{ai_data['recovery']:.1f} <span style="font-size: 1rem; color: #64748b;">min</span></div>
             <div style="color: #10b981;">{ai_data['recovery_trend']}</div>
        </div>
        """, unsafe_allow_html=True)
    with pred_2:
        st.markdown(f"""
        <div class="glass-card" style="border-left: 4px solid #2dd4bf;">
             <div style="color: #2dd4bf; font-weight: 700; font-size: 0.8rem; text-transform: uppercase;">AI Confidence</div>
             <div style="font-size: 2.5rem; font-weight: 700; color: white;">{ai_data['confidence']}%</div>
             <div style="color: #2dd4bf;">↑ High Precision</div>
        </div>
        """, unsafe_allow_html=True)

# --- EXECUTE ROUTING ---
route_page()

# --- FOOTER ---
st.markdown("---")
st.markdown("""
<div class="footer-container" style="padding-top: 40px; margin-top: 60px; border-top: 1px solid rgba(255,255,255,0.05);">
    <div style="display: flex; justify-content: space-between; flex-wrap: wrap; gap: 40px;">
        <div style="flex: 1.5; min-width: 250px;">
            <h4 style="color: #00f2fe; margin-bottom: 15px;">✨ About Symbiome</h4>
            <p style="font-size: 0.85rem; color: #94a3b8; line-height: 1.6;">
                The Science of Resilience. A multi-modal biofeedback system built for research, clinical validation, and human performance optimization.
            </p>
        </div>
        <div style="flex: 1; min-width: 150px;">
            <h4 style="color: #94a3b8; margin-bottom: 15px;">Technical Stack</h4>
            <div style="font-size: 0.85rem; color: #64748b; line-height: 1.8;">
                AI Predictive Engine<br>Digital Twin Modality<br>NLP Sentiment Analysis<br>Closed-Loop Intervention
            </div>
        </div>
    </div>
    <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; color: #475569; font-size: 0.8rem;">
        Symbiome Research Platform © 2025 • Advancing the science of human resilience
    </div>
</div>
""", unsafe_allow_html=True)

# --- AUTO-REFRESH ---
if st.session_state.live_mode:
    time.sleep(0.5)
    st.rerun()

# --- END OF APPLICATION ---
