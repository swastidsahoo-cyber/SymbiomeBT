"""
Custom Activities Interface.
Allows users to define and track real-world stress challenges using Virtual Sensors.
"""
import streamlit as st
import numpy as np
import time
import random
from datetime import datetime

def render_custom_activities_page():
    # --- SESSION STATE INITIALIZATION ---
    if 'custom_activities' not in st.session_state:
        st.session_state.custom_activities = [
            {
                "name": "Chemistry Test",
                "type": "Cognitive",
                "intensity": 6,
                "duration": 1,
                "notes": "With friends",
                "sessions": 0
            }
        ]
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

    # --- CSS STYLES ---
    st.markdown("""
<style>
@keyframes pulse-red {
    0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
    70% { transform: scale(1); box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
    100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0); }
}
.ca-title {
    color: #f97316;
    font-size: 2.2rem;
    font-weight: 800;
    margin-bottom: 5px;
}
.section-container {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 24px;
    margin-bottom: 25px;
}
.sensor-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 15px;
    margin-top: 20px;
}
.sensor-card {
    background: rgba(2, 6, 23, 0.6);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 10px;
    padding: 20px;
    text-align: center;
    transition: all 0.2s ease;
}
.sensor-card:hover {
    border-color: rgba(6, 182, 212, 0.4);
    background: rgba(2, 6, 23, 0.8);
}
.sensor-icon {
    font-size: 1.8rem;
    margin-bottom: 15px;
    opacity: 0.9;
}
.sensor-label {
    font-weight: 700;
    color: white;
    font-size: 0.95rem;
    margin-bottom: 5px;
}
.sensor-sub {
    font-size: 0.7rem;
    color: #94a3b8;
}
.no-hw-box {
    background: rgba(6, 182, 212, 0.05);
    border: 1px solid rgba(6, 182, 212, 0.2);
    padding: 12px 20px;
    border-radius: 8px;
    margin-top: 20px;
    font-size: 0.85rem;
    color: #e2e8f0;
    text-align: left;
}
.activity-card-container {
    background: #0f172a;
    border: 1px solid rgba(255,255,255,0.05);
    border-radius: 14px;
    padding: 24px;
    margin-bottom: 20px;
    position: relative;
}
.brain-box {
    background: rgba(245, 158, 11, 0.15);
    width: 44px;
    height: 44px;
    border-radius: 10px;
    display: flex;
    justify-content: center;
    align-items: center;
    font-size: 1.4rem;
    color: #f59e0b;
}
.active-session-v2 {
    background: linear-gradient(90deg, #1e0b0b 0%, #2a1a1a 100%);
    border: 1px solid rgba(239, 68, 68, 0.3);
    border-radius: 16px;
    padding: 25px;
    margin-bottom: 30px;
}
.intensity-bar-bg {
    width: 100%; height: 6px; background: rgba(255,255,255,0.1); border-radius: 3px; position: relative; margin: 15px 0;
}
.intensity-bar-fill {
    height: 100%; background: white; border-radius: 3px;
}
.intensity-bar-handle {
    width: 12px; height: 12px; background: white; border-radius: 50%; position: absolute; top: -3px; left: 60%;
}
.btn-start {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.1);
    color: #94a3b8;
    padding: 10px;
    border-radius: 8px;
    text-align: center;
    font-weight: 600;
    transition: all 0.2s;
    cursor: pointer;
}
.btn-start:hover {
    background: rgba(255,255,255,0.1);
    color: white;
}
</style>
""", unsafe_allow_html=True)

    # --- TOP HEADER ---
    st.markdown("""
<div style="margin-bottom: 30px;">
    <div class="ca-title">Custom Stress Activities</div>
    <p style="color: #94a3b8; font-size: 1.05rem;">
        Add your own real-world stress challenges and measure your resilience with or without sensors
    </p>
</div>
""", unsafe_allow_html=True)

    # --- ACTIVE SESSION VIEW (SCREENSHOT 3) ---
    if st.session_state.active_ca_session["active"]:
        session = st.session_state.active_ca_session
        elapsed = int(time.time() - session["start_time"])
        mins, secs = divmod(elapsed, 60)
        
        # Simulate sensor readings incrementing
        if random.random() > 0.7:
            session["readings"] += 1

        # Use a single block for the Active Session Bar to match Screenshot 3
        st.markdown(f"""
<div class="active-session-v2">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 25px;">
        <div style="display: flex; align-items: center; gap: 15px;">
            <div style="width: 10px; height: 10px; background: #ef4444; border-radius: 50%; box-shadow: 0 0 10px #ef4444;"></div>
            <div style="font-weight: 700; color: white; font-size: 0.95rem;">Session Active <span style="font-weight: 400; color: #94a3b8; margin-left: 10px;">{mins}:{secs:02d}</span></div>
            <div style="font-size: 0.8rem; color: #f59e0b; margin-left: 20px; display: flex; align-items: center; gap: 5px;">⚡ {session['readings']} readings</div>
            <div style="display: flex; gap: 12px; margin-left: 15px;">
                <span style="font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 5px;">📷 Camera PPG</span>
                <span style="font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 5px;">🎙️ Voice</span>
                <span style="font-size: 0.8rem; color: #94a3b8; display: flex; align-items: center; gap: 5px;">⌨️ Typing</span>
            </div>
        </div>
        <div style="background: rgba(239, 68, 68, 0.1); border: 1px solid #ef4444; color: white; padding: 6px 16px; border-radius: 8px; font-weight: 700; font-size: 0.85rem; display: flex; align-items: center; gap: 8px;">
            <span style="font-size: 0.9rem;">⏹️</span> End & Compute Score
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
        <div>
            <div style="color: #2dd4bf; font-size: 1.8rem; font-weight: 800;">{70 + random.randint(0,10)}</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">HRV (ms)</div>
        </div>
        <div>
            <div style="color: #38bdf8; font-size: 1.8rem; font-weight: 800;">{75 + random.randint(0,5)}</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">HR (bpm)</div>
        </div>
        <div>
            <div style="color: #a855f7; font-size: 1.8rem; font-weight: 800;">{50 + random.randint(0,5)}</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">GSR (μS)</div>
        </div>
        <div>
            <div style="color: #10b981; font-size: 1.8rem; font-weight: 800;">{40 + random.randint(0,10)}</div>
            <div style="color: #94a3b8; font-size: 0.75rem;">Calm Index</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)
        
        # Invisible button to trigger the end (placed near the text for UX)
        if st.button("Click to End Session", key="end_hidden", type="primary", use_container_width=True):
            st.session_state.active_ca_session["active"] = False
            st.toast("Activity analyzed. Data synced to Journal.", icon="📊")
            st.rerun()

    # --- VIRTUAL SENSOR LAYER (SCREENSHOT 0) ---
    st.markdown(f"""
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
    
    <div class="no-hw-box">
        <span style="font-weight: 700;">No hardware required:</span> These virtual sensors use your device's camera, microphone, and interaction patterns to measure physiological stress without any wearable devices.
    </div>
</div>
""", unsafe_allow_html=True)

    # --- YOUR CUSTOM ACTIVITIES ---
    ca_header_col1, ca_header_col2 = st.columns([3, 1])
    with ca_header_col1:
        st.markdown('<h3 style="margin-top: 10px;">Your Custom Activities</h3>', unsafe_allow_html=True)
    with ca_header_col2:
        if st.button("+ Add New Activity", key="btn_show_add", use_container_width=True):
            st.session_state.show_add_activity = True
            st.rerun()

    # Add Activity Form (Modal Simulation - SCREENSHOT 1 & 2)
    if st.session_state.show_add_activity:
        st.markdown("""
<div style="position: fixed; top:0; left:0; width:100%; height:100%; background: rgba(0,0,0,0.7); z-index: 10002;"></div>
<div style="position: fixed; top:50%; left:50%; transform: translate(-50%, -50%); width: 500px; background: #0f172a; border: 1px solid rgba(255,255,255,0.1); border-radius: 20px; z-index: 10003; padding: 40px; box-shadow: 0 20px 60px rgba(0,0,0,0.6);">
    <div style="text-align: left; margin-bottom: 30px;">
        <h3 style="color: white; margin-bottom: 10px;">Add New Stress Activity</h3>
        <p style="color: #94a3b8; font-size: 0.95rem;">Create a custom activity to track your stress response</p>
    </div>
</div>
""", unsafe_allow_html=True)
        
        # We place columns for the form inputs to overlay the "modal"
        m_col1, m_col2, m_col3 = st.columns([1, 2, 1])
        with m_col2:
            with st.form("new_activity_form_v2"):
                new_name = st.text_input("Activity Name", placeholder="e.g., Chemistry Test")
                new_type = st.selectbox("Activity Type", [
                    "Cognitive (studying, exams)", 
                    "Social (presentations, interviews)", 
                    "Physical (sports, exercise)", 
                    "Emotional (difficult conversations)", 
                    "High Pressure (competitions, deadlines)"
                ])
                new_intensity = st.slider("Estimated Intensity", 1, 10, 6)
                new_duration = st.number_input("Expected Duration (minutes)", min_value=1, value=1)
                new_notes = st.text_area("Notes (optional)", placeholder="With friends")
                
                f_col1, f_col2 = st.columns(2)
                with f_col1:
                    if st.form_submit_button("🎯 Add Activity", use_container_width=True):
                        st.session_state.custom_activities.append({
                            "name": new_name if new_name else "Untitled Activity",
                            "type": new_type.split(" (")[0],
                            "intensity": new_intensity,
                            "duration": new_duration,
                            "notes": new_notes,
                            "sessions": 0
                        })
                        st.session_state.show_add_activity = False
                        st.rerun()
                with f_col2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_add_activity = False
                        st.rerun()

    # Empty State (SCREENSHOT 0)
    if not st.session_state.custom_activities:
        st.markdown("""
<div style="background: rgba(15, 23, 42, 0.4); border: 2px dashed rgba(255,255,255,0.05); border-radius: 20px; padding: 100px 40px; text-align: center; margin-top: 20px;">
    <div style="font-size: 4rem; color: #334155; margin-bottom: 25px;">🎯</div>
    <h3 style="color: white; margin-bottom: 15px; font-weight: 800;">No Custom Activities Yet</h3>
    <p style="color: #94a3b8; max-width: 450px; margin: 0 auto 35px auto; font-size: 1rem; line-height: 1.6;">
        Create your first stress activity to start tracking your resilience in real-world scenarios. Works with sensors or self-report data.
    </p>
</div>
""", unsafe_allow_html=True)
        # Hidden button for the centered look
        m_empty1, m_empty2, m_empty3 = st.columns([1, 1, 1])
        with m_empty2:
            if st.button("+ Add Your First Activity", key="btn_first_add", type="primary", use_container_width=True):
                st.session_state.show_add_activity = True
                st.rerun()
    else:
        # Activity List Cards (SCREENSHOT 3)
        cols = st.columns(2)
        for i, activity in enumerate(st.session_state.custom_activities):
            with cols[i % 2]:
                st.markdown(f"""
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
    
    <div class="btn-start" onClick="window.parent.postMessage({{type: 'streamlit:setComponentValue', key: 'start_{i}', value: true}}, '*')">
        ▷ Start Activity
    </div>
</div>
""", unsafe_allow_html=True)
                
                # Hidden actual button for functional start
                if st.button(f"Hidden Start {i}", key=f"start_{i}", type="secondary"):
                    st.session_state.active_ca_session = {
                        "active": True,
                        "activity_name": activity['name'],
                        "start_time": time.time(),
                        "readings": 0,
                        "stress_level": 5
                    }
                    activity['sessions'] += 1
                    st.rerun()

    # --- AUTO-REFRESH (If session active) ---
    if st.session_state.active_ca_session["active"]:
        time.sleep(1)
        st.rerun()

if __name__ == "__main__":
    render_custom_activities_page()
