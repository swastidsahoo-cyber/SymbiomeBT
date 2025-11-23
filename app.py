import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from modules.science_logic import calculate_sri, predict_recovery, get_digital_twin_insight
import time

# ==========================================
# SYMBIOME APP CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Symbiome | AI Resilience Platform",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CSS & THEME MANAGEMENT
# ==========================================
def load_css(theme="dark"):
    with open("style.css") as f:
        css = f.read()
        
    if theme == "light":
        # Inject Light Mode Overrides
        css += """
        .stApp {
            background: #f0f9ff !important;
            color: #1a1a2e !important;
        }
        h1, h2, h3, .metric-label {
            color: #1a1a2e !important;
        }
        .stMarkdown p {
            color: #4a5568 !important;
        }
        """
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)

# ==========================================
# DATA LOADING
# ==========================================
@st.cache_data
def load_data():
    try:
        history_df = pd.read_csv("data/user_history.csv")
        session_df = pd.read_csv("data/simulated_session.csv")
        return history_df, session_df
    except FileNotFoundError:
        st.error("Data files not found. Please check the data directory.")
        return pd.DataFrame(), pd.DataFrame()

history_df, session_df = load_data()

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/dna-helix.png", width=60)
    st.title("Symbiome")
    st.markdown("### Resilience Platform")
    
    menu = st.radio(
        "Navigation", 
        ["Dashboard", "Monitor", "System", "Framework", "Settings"],
        index=0
    )
    
    st.markdown("---")
    st.markdown("### 🧬 System Status")
    st.markdown("🟢 **Sensors**: Active (Simulated)")
    st.markdown("🟣 **AI Engine**: Online")
    st.markdown("🔵 **Cloud Sync**: Just now")

# ==========================================
# PAGE ROUTING
# ==========================================

# --- DASHBOARD (DARK MODE) ---
if menu == "Dashboard":
    load_css("dark")
    
    # Header
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("# Your Symbiome Resilience")
        st.markdown("Your resilience is **balanced**. Small adjustments can optimize your response.")
    with col2:
        st.markdown(f"**User**: Researcher | **Level**: 5")
        st.markdown("🔥 **7 Day Streak**")

    st.markdown("---")

    # Main Gauge Logic
    latest_hrv = session_df['HRV_Score'].iloc[-1]
    latest_gsr = session_df['GSR_Score'].iloc[-1]
    latest_facial = session_df['Facial_Calm'].iloc[-1]
    current_sri = int(calculate_sri(latest_hrv, latest_gsr, latest_facial))
    
    if current_sri >= 75:
        sri_color = "#00f2fe"
        status_text = "OPTIMAL"
    elif current_sri >= 50:
        sri_color = "#f2c94c"
        status_text = "MODERATE"
    else:
        sri_color = "#ff4b1f"
        status_text = "STRESSED"

    # Layout
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        st.markdown(f"""
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; margin-bottom: 30px;">
            <div style="
                width: 200px; height: 200px; 
                border-radius: 50%; 
                background: conic-gradient({sri_color} {current_sri}%, rgba(255,255,255,0.1) 0);
                display: flex; justify-content: center; align-items: center;
                box-shadow: 0 0 50px {sri_color}40;
                animation: pulse-glow 3s infinite;
            ">
                <div style="
                    width: 180px; height: 180px; 
                    background: #1a1a2e; 
                    border-radius: 50%;
                    display: flex; flex-direction: column;
                    justify-content: center; align-items: center;
                ">
                    <span style="font-size: 4rem; font-weight: 700; color: white;">{current_sri}</span>
                    <span style="font-size: 1rem; color: rgba(255,255,255,0.6);">SRI SCORE</span>
                </div>
            </div>
            <div style="margin-top: 15px; font-size: 1.2rem; font-weight: 600; color: {sri_color}; letter-spacing: 2px;">
                {status_text}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("⚡ Start Biofeedback Session", use_container_width=True):
            st.toast("Initializing Sensors...", icon="🧬")

    # Cards
    st.markdown("### System Component Analysis")
    mc1, mc2, mc3, mc4 = st.columns(4)
    metrics = [
        ("HRV Index", int(latest_hrv), "#4facfe", "Balanced"),
        ("GSR Response", int(latest_gsr), "#f2c94c", "Balanced"),
        ("Cognitive Calm", int(latest_facial), "#00f2fe", "Optimal"),
        ("Environmental", 72, "#a8ff78", "Optimal")
    ]
    
    for col, (label, val, color, status) in zip([mc1, mc2, mc3, mc4], metrics):
        with col:
            st.markdown(f"""
            <div class="glass-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{val}</div>
                <div style="font-size: 0.8rem; color: {color};">{status}</div>
            </div>
            """, unsafe_allow_html=True)

    # Trend & AI
    c_trend, c_ai = st.columns([2, 1])
    with c_trend:
        st.markdown("### 📈 7-Day Resilience Trend")
        fig = px.area(history_df.tail(7), x='Date', y='Symbiome_Resilience_Score', template='plotly_dark')
        fig.update_traces(line_color='#00f2fe', fillcolor='rgba(0, 242, 254, 0.1)')
        fig.update_layout(height=300, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)
        
    with c_ai:
        st.markdown("### 🔮 AI Prediction")
        st.markdown(f"""
        <div class="glass-card" style="background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%); border: 1px solid #764ba2;">
            <div style="font-size: 0.9rem; color: #d4fc79; margin-bottom: 10px;">✨ Predicted SRI</div>
            <div style="font-size: 1.8rem; font-weight: 700;">{current_sri + 2} <span style="font-size: 0.8rem; color: #aaa;">(Confidence 80%)</span></div>
            <hr style="border-color: rgba(255,255,255,0.1);">
            <div style="font-size: 0.85rem; font-style: italic;">"Hydration boost may raise HRV within 10 mins."</div>
        </div>
        """, unsafe_allow_html=True)

    # AI Coach
    st.markdown("""
    <div class="ai-coach-container">
        <div class="ai-coach-bubble" title="AI Coach">
            <span class="ai-coach-icon">🤖</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# --- MONITOR (LIGHT MODE) ---
elif menu == "Monitor":
    load_css("light")
    
    st.markdown("# Symbiome Resilience System")
    st.markdown("AI-Powered Biological Intelligence Platform")
    
    st.markdown("### ⚡ Real-Time Biological Readings")
    
    # Light Mode Cards
    m1, m2, m3, m4 = st.columns(4)
    
    readings = [
        ("Heart Rate", f"{int(session_df['HRV_Score'].iloc[-1] + 20)} bpm", "Optimal: 72bpm"),
        ("GSR (Stress)", f"{session_df['GSR_Score'].iloc[-1]} µS", "Optimal: 50µS"),
        ("pH Level", f"{session_df['pH_Level'].iloc[-1]}", "Optimal: 7.35"),
        ("Temperature", f"{session_df['Temperature_C'].iloc[-1]}°C", "Optimal: 36.8°C")
    ]
    
    for col, (label, val, sub) in zip([m1, m2, m3, m4], readings):
        with col:
            st.markdown(f"""
            <div class="light-card">
                <div class="light-metric-label" style="color: #666;">{label}</div>
                <div style="font-size: 2rem; font-weight: 700; color: #1a1a2e;">{val}</div>
                <div style="font-size: 0.8rem; color: #10b981;">{sub}</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("### 🔄 Behavioral Feedback Loop")
    st.markdown("""
    <div class="light-card" style="display: flex; justify-content: space-between; align-items: center;">
        <div>
            <div style="font-weight: 600; font-size: 1.1rem; color: #1a1a2e;">💧 Hydration Break</div>
            <div style="color: #666;">Your pH is acidic. Drink 250ml of alkaline water.</div>
            <div style="font-size: 0.8rem; color: #666; margin-top: 5px;">⏱️ 2 min • ⚖️ Balances pH levels</div>
        </div>
        <button style="background: #1a1a2e; color: white; border: none; padding: 10px 20px; border-radius: 8px; cursor: pointer;">Start</button>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("### ✨ AI Prediction Engine")
    st.markdown("""
    <div class="light-card">
        <div style="display: flex; justify-content: space-between;">
            <div style="font-weight: 600; color: #764ba2;">🟣 AI Insight</div>
            <div style="background: #e11d48; color: white; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem;">Live</div>
        </div>
        <div style="margin-top: 10px; color: #1a1a2e;">Optimal resilience maintained. Continue current wellness practices.</div>
        <div style="margin-top: 10px; font-size: 0.8rem; color: #764ba2; background: #f3e8ff; padding: 5px 10px; border-radius: 5px; display: inline-block;">Confidence: 92%</div>
    </div>
    """, unsafe_allow_html=True)

# --- SYSTEM (LIGHT MODE) ---
elif menu == "System":
    load_css("light")
    
    col_score, col_radar = st.columns([1, 1])
    
    with col_score:
        st.markdown("### Symbiome Index Score")
        st.markdown("""
        <div class="light-card" style="text-align: center; padding: 40px;">
            <div style="font-size: 5rem; font-weight: 800; color: #10b981;">89<span style="font-size: 1.5rem; color: #aaa;">/100</span></div>
            <div style="color: #666;">Index Points</div>
            <div style="margin-top: 20px; height: 10px; background: #e5e7eb; border-radius: 5px; overflow: hidden;">
                <div style="width: 89%; height: 100%; background: #10b981;"></div>
            </div>
            <div style="display: flex; justify-content: space-between; font-size: 0.7rem; color: #aaa; margin-top: 5px;">
                <span>Critical</span><span>Fair</span><span>Good</span><span>Optimal</span><span>Peak</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("#### Health Performance Zones")
        zones = [("Peak Performance", "90-100", "#10b981"), ("Optimal", "75-89", "#34d399"), ("Good", "60-74", "#fbbf24")]
        for z_name, z_range, z_color in zones:
            st.markdown(f"""
            <div style="display: flex; justify-content: space-between; padding: 10px; border-bottom: 1px solid #eee;">
                <span style="display: flex; align-items: center;"><span style="width: 10px; height: 10px; background: {z_color}; border-radius: 50%; margin-right: 10px;"></span>{z_name}</span>
                <span style="color: #666;">{z_range}</span>
            </div>
            """, unsafe_allow_html=True)
            
    with col_radar:
        st.markdown("### System Component Analysis")
        
        # Radar Chart
        categories = ['Cardiovascular', 'Neurological', 'Metabolic', 'Thermal', 'Stress']
        r_values = [
            history_df['Cardiovascular_Score'].iloc[-1],
            history_df['Neurological_Score'].iloc[-1],
            history_df['Metabolic_Score'].iloc[-1],
            history_df['Thermal_Score'].iloc[-1],
            100 - history_df['GSR_Score'].iloc[-1] # Inverse stress for positive chart
        ]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=r_values,
            theta=categories,
            fill='toself',
            name='Current Status',
            line_color='#10b981'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            showlegend=False,
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # Component Cards
        c1, c2 = st.columns(2)
        with c1:
            st.metric("Cardiovascular", f"{r_values[0]}/100", "+2%")
            st.metric("Metabolic", f"{r_values[2]}/100", "-1%")
        with c2:
            st.metric("Neurological", f"{r_values[1]}/100", "+5%")
            st.metric("Thermal", f"{r_values[3]}/100", "0%")

# --- FRAMEWORK (LIGHT MODE) ---
elif menu == "Framework":
    load_css("light")
    
    st.markdown("# Symbiome Intelligence Framework (SIF)")
    st.markdown("7 Unique Features That Set This System Apart")
    
    features = [
        ("Resilience Mirror", "Transform your stress patterns into beautiful, evolving art", "✨"),
        ("Digital Twin", "AI model that learns and predicts your unique physiology", "🤖"),
        ("Environment × Body", "Discover how surroundings shape your resilience", "☁️"),
        ("Resilience Game", "Level up by mastering your stress response", "🎮"),
        ("Emotion Journal", "Map feelings to physiological signatures", "❤️"),
        ("Stress Forecast", "Predict tomorrow's resilience like weather", "🌧️"),
        ("Ethical AI", "Responsible design & data privacy commitment", "🛡️")
    ]
    
    cols = st.columns(3)
    for i, (title, desc, icon) in enumerate(features):
        with cols[i % 3]:
            st.markdown(f"""
            <div class="light-card" style="height: 200px;">
                <div style="font-size: 2rem; margin-bottom: 10px;">{icon}</div>
                <div style="font-weight: 600; color: #1a1a2e; margin-bottom: 5px;">{title}</div>
                <div style="font-size: 0.9rem; color: #666;">{desc}</div>
                <div style="margin-top: 15px; color: #764ba2; font-size: 0.8rem; font-weight: 600; cursor: pointer;">Explore →</div>
            </div>
            """, unsafe_allow_html=True)
            
    st.markdown("""
    <div style="background: linear-gradient(90deg, #764ba2, #667eea); padding: 30px; border-radius: 16px; color: white; margin-top: 30px;">
        <h3>🏆 Why These Innovations Matter for BTYSTE</h3>
        <ul style="list-style: none; padding: 0;">
            <li style="margin-bottom: 10px;">✅ <b>Interdisciplinary Excellence</b>: Bridging neuroscience, AI, psychology, and ethics.</li>
            <li style="margin-bottom: 10px;">✅ <b>Original Research</b>: 7 completely novel approaches.</li>
            <li>✅ <b>Real-World Impact</b>: Practical applications in education and healthcare.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)

# --- SETTINGS / DATA EDITOR ---
elif menu == "Settings":
    load_css("light") # Use light mode for editing for better readability
    
    st.title("⚙️ System Settings & Data Management")
    st.markdown("Directly edit the underlying data sources. Changes will be saved immediately.")
    
    tab1, tab2 = st.tabs(["User History (CSV)", "Simulated Session (CSV)"])
    
    with tab1:
        st.markdown("### User History Data")
        edited_history = st.data_editor(history_df, num_rows="dynamic", use_container_width=True)
        if st.button("Save History Changes"):
            edited_history.to_csv("data/user_history.csv", index=False)
            st.success("History data saved successfully!")
            st.cache_data.clear()
            
    with tab2:
        st.markdown("### Simulated Session Data")
        edited_session = st.data_editor(session_df, num_rows="dynamic", use_container_width=True)
        if st.button("Save Session Changes"):
            edited_session.to_csv("data/simulated_session.csv", index=False)
            st.success("Session data saved successfully!")
            st.cache_data.clear()

