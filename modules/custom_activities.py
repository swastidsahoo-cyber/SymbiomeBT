"""
Custom Activities Interface.
Allows users to define and track real-world stress challenges using Virtual Sensors.
Version 8.8 - BULLETPROOF NATIVE MODAL & INTERACTION
"""
import streamlit as st
import numpy as np
import time
import random
import textwrap
from datetime import datetime

def clean_render(html_str):
    """Ensure HTML strings are perfectly dedented and clean for Streamlit."""
    # Strips all leading indentation from the multiline string and renders it.
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def render_custom_activities_page():
    # --- SESSION STATE INITIALIZATION ---
    if 'custom_activities' not in st.session_state:
        st.session_state.custom_activities = []
    
    if 'active_ca_session' not in st.session_state:
        st.session_state.active_ca_session = {
            "active": False,
            "activity_name": None,
            "start_time": None,
            "readings": 0,
            "stress_level": 5
        }
    if 'show_add_activity' not in st.session_state:
        st.session_state.show_add_activity = False

    # --- CSS STYLES (ENFORCED 0-INDENT) ---
    clean_render("""
<style>
@keyframes pulse-vibrant {
    0% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(249, 115, 22, 0.6); }
    70% { transform: scale(1); box-shadow: 0 0 0 15px rgba(249, 115, 22, 0); }
    100% { transform: scale(0.98); box-shadow: 0 0 0 0 rgba(249, 115, 22, 0); }
}
.ca-title {
    background: linear-gradient(135deg, #fb923c 0%, #f97316 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2.5rem;
    font-weight: 900;
    margin-bottom: 8px;
    letter-spacing: -0.5px;
}
.section-container {
    background: rgba(30, 41, 59, 0.4);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 30px;
    box-shadow: 0 15px 35px rgba(0,0,0,0.3);
}
.sensor-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 18px;
    margin-top: 25px;
}
.sensor-card {
    background: linear-gradient(145deg, rgba(15, 23, 42, 0.8), rgba(2, 6, 23, 0.9));
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 16px;
    padding: 24px;
    text-align: center;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}
.sensor-card:hover {
    border-color: #fb923c;
    transform: translateY(-5px);
    box-shadow: 0 10px 25px rgba(249, 115, 22, 0.2);
}
.sensor-icon { 
    font-size: 2.2rem; 
    margin-bottom: 18px; 
    filter: drop-shadow(0 0 10px rgba(249, 115, 22, 0.3));
}
.sensor-label { font-weight: 800; color: white; font-size: 1rem; margin-bottom: 6px; }
.sensor-sub { font-size: 0.75rem; color: #94a3b8; font-weight: 500; }

.activity-card-container {
    background: linear-gradient(165deg, #0f172a 0%, #020617 100%);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 28px;
    margin-bottom: 25px;
    position: relative;
    height: 100%;
    overflow: hidden;
}
.activity-card-container::before {
    content: '';
    position: absolute; top: 0; left: 0; width: 100%; height: 4px;
    background: linear-gradient(90deg, #f97316, #a855f7);
    opacity: 0.6;
}
.brain-box {
    background: linear-gradient(135deg, rgba(245, 158, 11, 0.2), rgba(245, 158, 11, 0.1));
    width: 48px; height: 48px; border-radius: 14px;
    display: flex; justify-content: center; align-items: center;
    font-size: 1.6rem; color: #fb923c;
    border: 1px solid rgba(245, 158, 11, 0.2);
}
.active-session-v2 {
    background: linear-gradient(135deg, #1e0b0b 0%, #2e1212 50%, #1e0b0b 100%);
    border: 1px solid rgba(239, 68, 68, 0.4);
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 35px;
    box-shadow: 0 20px 50px rgba(239, 68, 68, 0.15);
}
.intensity-bar-bg {
    width: 100%; height: 10px; background: rgba(255,255,255,0.1); border-radius: 5px; position: relative; margin: 20px 0;
    overflow: hidden;
}
.intensity-bar-fill { 
    height: 100%; 
    background: linear-gradient(90deg, #fb923c, #f97316); 
    border-radius: 5px; 
    box-shadow: 0 0 15px rgba(249, 115, 22, 0.5);
}
.intensity-bar-handle {
    width: 16px; height: 16px; background: white; border-radius: 50%;
    position: absolute; top: -3px; border: 3px solid #f97316;
    box-shadow: 0 0 10px rgba(255,255,255,0.8);
}

/* MODAL UNIT (V9.0 VIBRANT) */
div[data-testid="stForm"] {
    background: linear-gradient(165deg, #0f172a 0%, #020617 100%) !important;
    border: 1px solid rgba(255,255,255,0.15) !important;
    border-radius: 28px !important;
    padding: 40px !important;
    box-shadow: 0 30px 100px rgba(0,0,0,0.8) !important;
}

/* Custom button styling - Premium Glass Look */
div.stButton > button {
    background: linear-gradient(135deg, rgba(255,255,255,0.08), rgba(255,255,255,0.03)) !important;
    border: 1px solid rgba(255,255,255,0.12) !important;
    color: #e2e8f0 !important;
    font-weight: 700 !important;
    border-radius: 12px !important;
    padding: 12px 24px !important;
    transition: all 0.3s ease !important;
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.85rem !important;
}
div.stButton > button:hover {
    background: linear-gradient(135deg, #fb923c, #f97316) !important;
    color: white !important;
    border-color: transparent !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 10px 20px rgba(249, 115, 22, 0.3) !important;
}
</style>
    """)

    # --- TOP HEADER ---
    clean_render("""
<div style="margin-bottom: 30px;">
    <div class="ca-title">Custom Stress Activities</div>
    <p style="color: #94a3b8; font-size: 1.05rem;">
        Add your own real-world stress challenges and measure your resilience with or without sensors
    </p>
</div>
    """)

    # --- MODAL LAYER (V8.8 - NATIVE CENTERED) ---
    if st.session_state.show_add_activity:
        # We use columns to center a "whole popup box" that is 100% interactive
        m_col1, m_col2, m_col3 = st.columns([0.2, 1, 0.2])
        with m_col2:
            with st.form("new_activity_form_v88"):
                clean_render("""
<div style="text-align: left; margin-bottom: 25px;">
    <h3 style="color: white; margin-bottom: 5px; font-weight: 800;">Add New Stress Activity</h3>
    <p style="color: #94a3b8; font-size: 0.9rem;">Create a custom activity to track your stress response</p>
</div>
                """)
                
                new_name = st.text_input("Activity Name", placeholder="e.g., Chemistry Exam, Job Interview, Public Speaking")
                new_type = st.selectbox("Activity Type", [
                    "Cognitive (studying, exams)", 
                    "Social (presentations, interviews)", 
                    "Physical (sports, exercise)", 
                    "Emotional (difficult conversations)", 
                    "High Pressure (competitions, deadlines)"
                ])
                
                clean_render('<div style="margin-top: 15px; color: white; font-size: 0.9rem; font-weight: 600;">Estimated Intensity: 5/10</div>')
                new_intensity = st.slider("Intensity Slider", 1, 10, 5, label_visibility="collapsed")
                
                new_duration = st.number_input("Expected Duration (minutes)", min_value=1, value=10)
                new_notes = st.text_area("Notes (optional)", placeholder="What triggers stress? Where are you? Who are you with?")
                
                st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)
                f_btns_col1, f_btns_col2 = st.columns([2, 1])
                with f_btns_col1:
                    if st.form_submit_button("✅ Add Activity", use_container_width=True):
                        st.session_state.custom_activities.append({
                            "name": new_name if new_name else "Untitled Activity",
                            "type": new_type.split(" (")[0],
                            "intensity": new_intensity,
                            "duration": new_duration,
                            "notes": new_notes,
                            "sessions": 0
                        })
                        st.session_state.show_add_activity = False
                        st.toast("Activity synchronized to Registry", icon="✨")
                        st.rerun()
                with f_btns_col2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_add_activity = False
                        st.rerun()
        # Ensure nothing else renders below the modal if we want the "modal focus"
        return # Exit the function early while modal is up

    # --- ACTIVE SESSION VIEW ---
    if st.session_state.active_ca_session["active"]:
        session = st.session_state.active_ca_session
        elapsed = int(time.time() - session["start_time"])
        mins, secs = divmod(elapsed, 60)
        if random.random() > 0.7: session["readings"] += 1
        
        # v8.9: Realistic Stress Level & Metric Fluctuations
        # Random walk for stress level (0.1 steps)
        session["stress_level"] = round(max(1.0, min(10.0, session["stress_level"] + random.uniform(-0.15, 0.15))), 1)
        
        # Generate varied metrics for the grid
        hrv = 70 + random.randint(0, 15)
        hr = 72 + random.randint(0, 10)
        gsr = 50 + random.randint(0, 8)
        calm = 40 + random.randint(0, 12)

        clean_render(f"""
<div class="active-session-v2">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="width: 10px; height: 10px; background: #ef4444; border-radius: 50%; box-shadow: 0 0 10px #ef4444;"></div>
            <div style="font-weight: 700; color: white; font-size: 0.95rem;">Session Active <span style="font-weight: 400; color: #94a3b8; margin-left: 10px;">{mins}:{secs:02d}</span></div>
            <div style="font-size: 0.8rem; color: #f59e0b; margin-left: 20px; display: flex; align-items: center; gap: 5px;">⚡ {session['readings']} readings</div>
            <div style="display: flex; gap: 12px; margin-left: 15px;">
                <span style="font-size: 0.8rem; color: #94a3b8;">📷 Camera PPG</span>
                <span style="font-size: 0.8rem; color: #94a3b8;">🎙️ Voice</span>
                <span style="font-size: 0.8rem; color: #94a3b8;">⌨️ Typing</span>
            </div>
        </div>
    </div>
    <div style="margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 12px;">
            <span style="font-size: 0.95rem; font-weight: 700; color: white;">Current Stress Level: {session['stress_level']}/10</span>
        </div>
        <div class="intensity-bar-bg">
            <div class="intensity-bar-fill" style="width: {session['stress_level']*10}%;"></div>
            <div class="intensity-bar-handle" style="left: calc({session['stress_level']*10}% - 6px);"></div>
        </div>
    </div>
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; text-align: center;">
        <div><div style="color: #2dd4bf; font-size: 1.8rem; font-weight: 800;">{hrv}</div><div style="color: #94a3b8; font-size: 0.75rem;">HRV (ms)</div></div>
        <div><div style="color: #38bdf8; font-size: 1.8rem; font-weight: 800;">{hr}</div><div style="color: #94a3b8; font-size: 0.75rem;">HR (bpm)</div></div>
        <div><div style="color: #a855f7; font-size: 1.8rem; font-weight: 800;">{gsr}</div><div style="color: #94a3b8; font-size: 0.75rem;">GSR (μS)</div></div>
        <div><div style="color: #10b981; font-size: 1.8rem; font-weight: 800;">{calm}</div><div style="color: #94a3b8; font-size: 0.75rem;">Calm Index</div></div>
    </div>
</div>
        """)
        
        if st.button("⏹️ End & Compute Score", key="end_session_btn", type="primary", use_container_width=True):
            st.session_state.active_ca_session["active"] = False
            st.toast("Activity analyzed. Data synced to Journal.", icon="📊")
            st.rerun()

    # --- VIRTUAL SENSOR LAYER (SCREENSHOT 0) ---
    if not st.session_state.active_ca_session["active"]:
        clean_render("""
<div class="section-container">
    <div style="display: flex; align-items: center; gap: 12px; margin-bottom: 5px;">
        <span style="font-size: 1.3rem; color: #94a3b8;">♒</span>
        <span style="font-weight: 700; color: white; font-size: 1.1rem;">Virtual Sensor Layer</span>
    </div>
    <div style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">
        Enable measurement methods - works completely without hardware
    </div>
    <div class="sensor-grid">
        <div class="sensor-card">
            <div class="sensor-icon">📷</div>
            <div class="sensor-label">Camera PPG</div>
            <div class="sensor-sub">HRV & Heart Rate</div>
        </div>
        <div class="sensor-card">
            <div class="sensor-icon">🎙️</div>
            <div class="sensor-label">Voice Analysis</div>
            <div class="sensor-sub">Speech stress markers</div>
        </div>
        <div class="sensor-card">
            <div class="sensor-icon">⌨️</div>
            <div class="sensor-label">Typing Dynamics</div>
            <div class="sensor-sub">Cognitive load</div>
        </div>
        <div class="sensor-card">
            <div class="sensor-icon">🧠</div>
            <div class="sensor-label">Cognitive Tests</div>
            <div class="sensor-sub">Reaction time & accuracy</div>
        </div>
    </div>
</div>
        """)

    # --- YOUR CUSTOM ACTIVITIES HEADER ---
    ca_header_col1, ca_header_col2 = st.columns([3, 1])
    with ca_header_col1:
        st.markdown('<h3 style="margin-top: 10px; font-weight: 800;">Your Custom Activities</h3>', unsafe_allow_html=True)
    with ca_header_col2:
        if st.button("+ Add New Activity", key="btn_show_add_main", use_container_width=True):
            st.session_state.show_add_activity = True
            st.rerun()

    # --- REGISTRY VIEW ---
    if not st.session_state.custom_activities:
        clean_render("""
<div style="background: rgba(15, 23, 42, 0.4); border: 2px dashed rgba(255,255,255,0.05); border-radius: 20px; padding: 100px 40px; text-align: center; margin-top: 20px;">
    <div style="font-size: 4rem; color: #334155; margin-bottom: 25px;">🎯</div>
    <h3 style="color: white; margin-bottom: 15px; font-weight: 800;">No Custom Activities Yet</h3>
    <p style="color: #94a3b8; max-width: 450px; margin: 0 auto 35px auto; font-size: 1rem; line-height: 1.6;">
        Create your first stress activity to start tracking your resilience in real-world scenarios.
    </p>
</div>
        """)
    else:
        # Use columns for card grid
        cols = st.columns(2)
        for i, activity in enumerate(st.session_state.custom_activities):
            with cols[i % 2]:
                with st.container():
                    clean_render(f"""
<div class="activity-card-container">
    <div style="display: flex; gap: 18px; align-items: flex-start; margin-bottom: 25px;">
        <div class="brain-box">🧠</div>
        <div>
            <div style="font-weight: 800; color: white; font-size: 1.25rem;">{activity['name']}</div>
            <div style="font-size: 0.9rem; color: #94a3b8; font-weight: 500;">{activity['type']}</div>
        </div>
    </div>
    <div style="margin-bottom: 25px;">
        <div style="display: flex; justify-content: space-between; margin-bottom: 10px;">
            <span style="font-size: 0.9rem; color: #e2e8f0; font-weight: 500;">Intensity</span>
            <span style="font-size: 0.95rem; color: white; font-weight: 800;">{activity['intensity']}/10</span>
        </div>
        <div class="intensity-bar-bg" style="margin: 0;">
            <div class="intensity-bar-fill" style="width: {activity['intensity']*10}%;"></div>
        </div>
    </div>
    <div style="display: flex; gap: 20px; color: #94a3b8; font-size: 0.9rem; margin-bottom: 15px; font-weight: 500;">
        <span>🕒 {activity['duration']}m</span>
        <span>📊 {activity['sessions']} sessions</span>
    </div>
    <div style="color: #64748b; font-size: 0.85rem; margin-bottom: 25px;">{activity['notes']}</div>
</div>
                    """)
                    if st.button(f"▷ Start Activity", key=f"real_start_{i}", use_container_width=True):
                        st.session_state.active_ca_session = {
                            "active": True,
                            "activity_name": activity['name'],
                            "start_time": time.time(),
                            "readings": 0,
                            "stress_level": 5
                        }
                        activity['sessions'] += 1
                        st.rerun()

    # --- AUTO-REFRESH FOR ACTIVE SESSION ---
    if st.session_state.active_ca_session["active"]:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    render_custom_activities_page()
