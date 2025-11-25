import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.science_logic import calculate_sri, predict_recovery, get_digital_twin_insight
import time
import os

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
    st.session_state.show_coach = False
if 'biofeedback_active' not in st.session_state:
    st.session_state.biofeedback_active = False
if 'hydration_active' not in st.session_state:
    st.session_state.hydration_active = False

def toggle_coach():
    st.session_state.show_coach = not st.session_state.show_coach

def start_biofeedback():
    st.session_state.biofeedback_active = True

def start_hydration():
    st.session_state.hydration_active = True

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    try:
        base_dir = os.path.dirname(__file__)
        history_path = os.path.join(base_dir, "data", "user_history.csv")
        session_path = os.path.join(base_dir, "data", "simulated_session.csv")
        
        history_df = pd.read_csv(history_path)
        session_df = pd.read_csv(session_path)
        return history_df, session_df
    except FileNotFoundError:
        return pd.DataFrame(), pd.DataFrame()

history_df, session_df = load_data()

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
    st.markdown("""
    <div style="text-align: right;">
        <span style="background: rgba(0, 242, 254, 0.1); color: #00f2fe; padding: 5px 10px; border-radius: 8px; font-size: 0.8rem; border: 1px solid rgba(0, 242, 254, 0.3);">
            ● LIVE MONITORING
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# --- SECTION 1: HERO (SRI GAUGE) ---
if not session_df.empty:
    latest_hrv = session_df['HRV_Score'].iloc[-1]
    latest_gsr = session_df['GSR_Score'].iloc[-1]
    latest_facial = session_df['Facial_Calm'].iloc[-1]
    current_sri = int(calculate_sri(latest_hrv, latest_gsr, latest_facial))
else:
    latest_hrv, latest_gsr, latest_facial, current_sri = 60, 10, 80, 75

if current_sri >= 75:
    sri_color, status_text, glow_color = "#00f2fe", "OPTIMAL STATE", "rgba(0, 242, 254, 0.6)"
elif current_sri >= 50:
    sri_color, status_text, glow_color = "#f2c94c", "BALANCED", "rgba(242, 201, 76, 0.6)"
else:
    sri_color, status_text, glow_color = "#ff4b1f", "HIGH STRESS", "rgba(255, 75, 31, 0.6)"

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
        <div style="color: #64748b; margin-top: 5px;">Your resilience is stable. Small adjustments can optimize performance.</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Biofeedback Button Logic
    if st.session_state.biofeedback_active:
        st.success("✅ Biofeedback Session Active")
        st.progress(65, text="Calibrating Sensors...")
    else:
        st.button("⚡ Start Biofeedback Session", on_click=start_biofeedback, use_container_width=True)

# --- SECTION 2: REAL-TIME BIOMETRICS STRIP ---
st.markdown("### ⚡ Real-Time Biological Readings")
m1, m2, m3, m4 = st.columns(4)
metrics = [
    ("Heart Rate", f"{int(latest_hrv + 20)}", "bpm", "#ff4b1f"),
    ("GSR (Stress)", f"{latest_gsr}", "µS", "#f2c94c"),
    ("pH Level", f"{session_df['pH_Level'].iloc[-1]}", "pH", "#00f2fe"),
    ("Temperature", f"{session_df['Temperature_C'].iloc[-1]}", "°C", "#a8ff78")
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

# Hydration Card with Button Logic
c_hydro_1, c_hydro_2 = st.columns([3, 1])
with c_hydro_1:
    st.markdown("""
    <div class="glass-card" style="height: 100%; display: flex; flex-direction: column; justify-content: center;">
        <div style="font-weight: 600; font-size: 1.1rem; color: white; margin-bottom: 5px;">💧 Hydration Break</div>
        <div style="color: #94a3b8;">Your pH is slightly acidic. Drink 250ml of alkaline water.</div>
        <div style="font-size: 0.8rem; color: #00f2fe; margin-top: 10px;">⏱️ 2 min • ⚖️ Balances pH levels</div>
    </div>
    """, unsafe_allow_html=True)
with c_hydro_2:
    st.markdown('<div style="height: 25px;"></div>', unsafe_allow_html=True) # Spacer
    if st.session_state.hydration_active:
        st.button("✅ Active", disabled=True, use_container_width=True)
    else:
        st.button("Start", on_click=start_hydration, use_container_width=True)

# --- SECTION 4: DETAILED AI PREDICTION ENGINE ---
st.markdown("### 🔮 AI Prediction Engine")

# Main AI Insight Card
st.markdown(f"""
<div class="glass-card" style="background: linear-gradient(135deg, rgba(118, 75, 162, 0.2) 0%, rgba(24, 24, 27, 0.5) 100%); border: 1px solid rgba(118, 75, 162, 0.4);">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
        <div style="font-size: 1.1rem; font-weight: 700; color: white;">✨ AI Insight</div>
        <div style="background: #e11d48; color: white; padding: 2px 10px; border-radius: 12px; font-size: 0.7rem; font-weight: 700;">LIVE</div>
    </div>
    <div style="font-size: 1.2rem; color: #e2e8f0; margin-bottom: 10px;">Optimal resilience maintained. Continue current wellness practices.</div>
    <div style="color: #a855f7; font-size: 0.9rem; font-weight: 600;">Confidence: 92%</div>
</div>
""", unsafe_allow_html=True)

# Detailed Metrics Grid
c_grid1, c_grid2 = st.columns(2)
with c_grid1:
    st.markdown("""
    <div class="ai-grid-card">
        <div class="ai-grid-label">⏱️ Expected Recovery</div>
        <div class="ai-grid-value">4.2 min</div>
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
    st.markdown("""
    <div class="ai-grid-card">
        <div class="ai-grid-label">📉 Stress Risk</div>
        <div class="ai-grid-value" style="color: #10b981;">Low</div>
        <div style="font-size: 0.7rem; color: #10b981;">Stable trend</div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="ai-grid-card">
        <div class="ai-grid-label">🤖 AI Confidence</div>
        <div class="ai-grid-value">92%</div>
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
        history_df['Cardiovascular_Score'].iloc[-1],
        history_df['Neurological_Score'].iloc[-1],
        history_df['Metabolic_Score'].iloc[-1],
        history_df['Thermal_Score'].iloc[-1],
        100 - latest_gsr
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
    fig = px.area(history_df.tail(7), x='Date', y='Symbiome_Resilience_Score', template='plotly_dark')
    fig.update_traces(line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.1)')
    fig.update_layout(height=250, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', margin=dict(l=0, r=0, t=0, b=0), xaxis=dict(showgrid=False), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)'))
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

# --- AI COACH (INTERACTIVE) ---
# Floating Bubble CSS (Hidden button overlay)
st.markdown("""
<style>
div.stButton > button[kind="secondary"] {
    position: fixed;
    bottom: 30px;
    right: 30px;
    width: 60px;
    height: 60px;
    border-radius: 50%;
    background: linear-gradient(135deg, #00f2fe 0%, #4facfe 100%);
    color: white;
    font-size: 24px;
    border: none;
    box-shadow: 0 4px 20px rgba(0, 242, 254, 0.4);
    z-index: 9999;
    transition: transform 0.3s ease;
}
div.stButton > button[kind="secondary"]:hover {
    transform: scale(1.1);
    box-shadow: 0 8px 30px rgba(0, 242, 254, 0.6);
}
</style>
""", unsafe_allow_html=True)

# Toggle logic
st.button("🤖", key="coach_btn", on_click=toggle_coach, type="secondary")

# Tip Popup (Styled exactly like UI)
if st.session_state.show_coach:
    st.markdown("""
    <div style="
        position: fixed; bottom: 100px; right: 30px; width: 350px;
        background: #115e59; /* Dark Teal */
        border-radius: 12px;
        padding: 20px; 
        box-shadow: 0 10px 40px rgba(0,0,0,0.5); 
        z-index: 9998;
        font-family: 'Outfit', sans-serif;
    ">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 10px;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <div style="
                    width: 32px; height: 32px; 
                    background: rgba(255,255,255,0.1); 
                    border-radius: 50%; 
                    display: flex; justify-content: center; align-items: center;
                ">
                    <span style="font-size: 16px;">💡</span>
                </div>
                <div>
                    <div style="font-size: 0.8rem; color: #ccfbf1; font-weight: 600;">AI Coach</div>
                    <div style="font-size: 0.9rem; color: white; font-weight: 700;">Did You Know?</div>
                </div>
            </div>
            <div style="cursor: pointer; color: #ccfbf1;">✕</div>
        </div>
        
        <div style="font-size: 0.9rem; color: #f0fdfa; line-height: 1.5; margin-bottom: 20px;">
            Your gut microbiome produces 90% of serotonin. Poor gut health can reduce HRV by 18% on average.
        </div>
        
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <button style="
                background: #2dd4bf; 
                color: #0f172a; 
                border: none; 
                padding: 8px 16px; 
                border-radius: 6px; 
                font-size: 0.85rem; 
                font-weight: 600; 
                cursor: pointer;
            ">Learn More</button>
            
            <div style="display: flex; align-items: center; gap: 8px; cursor: pointer;">
                <span style="font-size: 0.85rem; color: #ccfbf1; font-weight: 600;">Next Tip</span>
                <div style="display: flex; gap: 4px;">
                    <div style="width: 6px; height: 6px; background: #2dd4bf; border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background: rgba(45, 212, 191, 0.3); border-radius: 50%;"></div>
                    <div style="width: 6px; height: 6px; background: rgba(45, 212, 191, 0.3); border-radius: 50%;"></div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

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
