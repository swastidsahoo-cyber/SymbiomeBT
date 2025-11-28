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
    fluctuation = (random.random() - 0.5) * 3
    
    # BIOFEEDBACK MODE: Boost HRV, Lower Stress
    if st.session_state.biofeedback_active:
        # Simulate "Calming Down" - HRV rises, GSR drops
        hrv_base = 85 + (15 * math.sin(now / 8)) # Higher, smoother HRV
        gsr_base = 4 + (1 * math.cos(now / 10))  # Lower, stable GSR
        facial_base = 95 # High calmness
        temp_base = 36.4 # Slightly cooler (parasympathetic)
    else:
        # NORMAL MODE: Random stress spikes
        hrv_base = 60 + (10 * math.sin(now / 10))
        gsr_base = 12 + (4 * math.cos(now / 15))
        facial_base = 75
        temp_base = 36.7
        
        # Occasional "Stress Spike" (10% chance)
        if random.random() < 0.1:
            hrv_base -= 15
            gsr_base += 5

    # Apply noise
    hrv = hrv_base + fluctuation
    gsr = gsr_base + (fluctuation / 2)
    facial = facial_base + fluctuation
    temp = temp_base + (random.random() - 0.5) * 0.1
    ph = 7.35 + (random.random() - 0.5) * 0.05
    
    return hrv, gsr, facial, temp, ph

# Get live data
live_hrv, live_gsr, live_facial, live_temp, live_ph = simulate_live_data()
current_sri = int(calculate_sri(live_hrv, live_gsr, live_facial))

# --- AI PREDICTION LOGIC ---
def get_ai_predictions(sri):
    """Returns deterministic AI insights based on the SRI score."""
    if sri >= 80:
        return {
            "recovery": random.uniform(2.0, 3.5), # Fast recovery
            "recovery_trend": "↑ 25% (Optimal)",
            "peak_perf": "NOW - 18:00",
            "stress_risk": "Low",
            "stress_color": "#10b981",
            "confidence": random.randint(94, 99),
            "insight": "Optimal resilience maintained. Continue current wellness practices."
        }
    elif sri >= 50:
        return {
            "recovery": random.uniform(4.0, 6.0), # Moderate recovery
            "recovery_trend": "↑ 10% (Stable)",
            "peak_perf": "10:00 - 12:00",
            "stress_risk": "Moderate",
            "stress_color": "#f59e0b",
            "confidence": random.randint(88, 93),
            "insight": "System stable. Minor adjustments to hydration could boost performance."
        }
    else:
        return {
            "recovery": random.uniform(8.0, 12.0), # Slow recovery
            "recovery_trend": "↓ 15% (Needs Rest)",
            "peak_perf": "Rest Required",
            "stress_risk": "High",
            "stress_color": "#ef4444",
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
