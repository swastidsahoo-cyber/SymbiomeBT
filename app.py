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
    # Fix for Streamlit Cloud: Ensure we look in the current directory
    css_path = os.path.join(os.path.dirname(__file__), "style.css")
    try:
        with open(css_path) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"Error: style.css not found at {css_path}")

load_css()

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    try:
        # Fix for Streamlit Cloud: Ensure we look in the current directory
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
# Logic
if not session_df.empty:
    latest_hrv = session_df['HRV_Score'].iloc[-1]
    latest_gsr = session_df['GSR_Score'].iloc[-1]
    latest_facial = session_df['Facial_Calm'].iloc[-1]
    current_sri = int(calculate_sri(latest_hrv, latest_gsr, latest_facial))
else:
    # Fallback if data fails
    latest_hrv = 60
    latest_gsr = 10
    latest_facial = 80
    current_sri = 75

if current_sri >= 75:
    sri_color = "#00f2fe" # Cyan
    status_text = "OPTIMAL STATE"
    glow_color = "rgba(0, 242, 254, 0.6)"
elif current_sri >= 50:
    sri_color = "#f2c94c" # Gold
    status_text = "BALANCED"
    glow_color = "rgba(242, 201, 76, 0.6)"
else:
    sri_color = "#ff4b1f" # Red
    status_text = "HIGH STRESS"
    glow_color = "rgba(255, 75, 31, 0.6)"

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
    
    # Biofeedback Button
    if st.button("⚡ Start Biofeedback Session", use_container_width=True):
        st.toast("Initializing Sensors...", icon="🧬")
        time.sleep(1)
        st.toast("Calibrating Baseline...", icon="📊")
        time.sleep(1)
        st.toast("Session Started!", icon="✅")

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
st.markdown("""
<div class="glass-card" style="display: flex; justify-content: space-between; align-items: center;">
    <div>
        <div style="font-weight: 600; font-size: 1.1rem; color: white; margin-bottom: 5px;">💧 Hydration Break</div>
        <div style="color: #94a3b8;">Your pH is slightly acidic. Drink 250ml of alkaline water.</div>
        <div style="font-size: 0.8rem; color: #00f2fe; margin-top: 10px;">⏱️ 2 min • ⚖️ Balances pH levels</div>
    </div>
    <button style="background: rgba(0, 242, 254, 0.1); color: #00f2fe; border: 1px solid #00f2fe; padding: 10px 20px; border-radius: 8px; cursor: pointer; font-weight: 600;">Start</button>
</div>
""", unsafe_allow_html=True)

# --- SECTION 4: SYSTEM ANALYSIS (RADAR & ZONES) ---
st.markdown("### 🧬 System Component Analysis")

col_radar, col_zones = st.columns([1, 1])

with col_radar:
    # Radar Chart
    categories = ['Cardiovascular', 'Neurological', 'Metabolic', 'Thermal', 'Stress Resilience']
    r_values = [
        history_df['Cardiovascular_Score'].iloc[-1],
        history_df['Neurological_Score'].iloc[-1],
        history_df['Metabolic_Score'].iloc[-1],
        history_df['Thermal_Score'].iloc[-1],
        100 - latest_gsr
    ]
    
    fig = go.Figure()
    fig.add_trace(go.Scatterpolar(
        r=r_values,
        theta=categories,
        fill='toself',
        name='Current Status',
        line_color='#00f2fe',
        fillcolor='rgba(0, 242, 254, 0.2)'
    ))
    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, linecolor='rgba(255,255,255,0.1)'),
            angularaxis=dict(tickfont=dict(color='#94a3b8', size=10)),
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        showlegend=False,
        height=350,
        margin=dict(l=40, r=40, t=20, b=20)
    )
    
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_zones:
    st.markdown("""
    <div class="glass-card" style="height: 350px; display: flex; flex-direction: column; justify-content: center;">
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Peak Performance</span>
                <span style="color: #00f2fe;">90-100</span>
            </div>
            <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                <div style="width: 90%; height: 100%; background: #00f2fe; border-radius: 4px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Optimal</span>
                <span style="color: #a8ff78;">75-89</span>
            </div>
            <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                <div style="width: 75%; height: 100%; background: #a8ff78; border-radius: 4px;"></div>
            </div>
        </div>
        <div style="margin-bottom: 20px;">
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Balanced</span>
                <span style="color: #f2c94c;">60-74</span>
            </div>
            <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                <div style="width: 60%; height: 100%; background: #f2c94c; border-radius: 4px;"></div>
            </div>
        </div>
        <div>
            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                <span>Critical</span>
                <span style="color: #ff4b1f;">0-59</span>
            </div>
            <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                <div style="width: 30%; height: 100%; background: #ff4b1f; border-radius: 4px;"></div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- SECTION 5: AI PREDICTION & TRENDS ---
st.markdown("### 🔮 AI Prediction Engine")

c_ai, c_trend = st.columns([1, 2])

with c_ai:
    st.markdown(f"""
    <div class="glass-card" style="background: linear-gradient(135deg, rgba(118, 75, 162, 0.2) 0%, rgba(24, 24, 27, 0.5) 100%); border: 1px solid rgba(118, 75, 162, 0.4);">
        <div style="font-size: 0.9rem; color: #d4fc79; margin-bottom: 15px; display: flex; align-items: center;">
            <span style="margin-right: 8px;">✨</span> AI INSIGHT
        </div>
        <div style="font-size: 2.5rem; font-weight: 700; color: white;">{current_sri + 2}</div>
        <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">Predicted SRI (10 min)</div>
        <div style="background: rgba(255,255,255,0.05); padding: 15px; border-radius: 12px; font-size: 0.85rem; line-height: 1.5; border-left: 3px solid #d4fc79;">
            "Hydration boost detected. Vagal tone expected to improve by 4% within 10 minutes."
        </div>
        <div style="margin-top: 15px; font-size: 0.8rem; color: #a855f7;">Confidence: 92%</div>
    </div>
    """, unsafe_allow_html=True)

with c_trend:
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown('<div class="metric-label">7-DAY RESILIENCE TREND</div>', unsafe_allow_html=True)
    fig = px.area(history_df.tail(7), x='Date', y='Symbiome_Resilience_Score', template='plotly_dark')
    fig.update_traces(line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.1)')
    fig.update_layout(
        height=220, 
        paper_bgcolor='rgba(0,0,0,0)', 
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(showgrid=False),
        yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.1)')
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- SECTION 6: SIF FRAMEWORK (CARDS) ---
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
        <div class="glass-card" style="min-height: 180px; cursor: pointer;">
            <div style="font-size: 2rem; margin-bottom: 15px;">{icon}</div>
            <div style="font-weight: 700; color: white; margin-bottom: 8px; font-size: 1.1rem;">{title}</div>
            <div style="font-size: 0.9rem; color: #94a3b8; line-height: 1.4;">{desc}</div>
            <div style="margin-top: 15px; color: #00f2fe; font-size: 0.8rem; font-weight: 600;">EXPLORE →</div>
        </div>
        """, unsafe_allow_html=True)

# --- AI COACH (FLOATING) ---
st.markdown("""
<div class="ai-coach-container">
    <div class="ai-coach-bubble" title="AI Coach">
        <span class="ai-coach-icon">🤖</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --- SIDEBAR (SETTINGS & DOCS) ---
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=50)
    st.markdown("### Symbiome")
    st.markdown("---")
    
    with st.expander("⚙️ Settings & Data"):
        st.markdown("Edit underlying data sources:")
        if st.checkbox("Show Data Editor"):
            st.data_editor(history_df, num_rows="dynamic")
            
    with st.expander("📄 Scientific Documentation"):
        st.markdown("Read the whitepaper:")
        try:
            with open("science_whitepaper.md", "r") as f:
                st.download_button("Download Whitepaper", f, file_name="Symbiome_Whitepaper.md")
        except FileNotFoundError:
            st.error("Whitepaper file not found.")
