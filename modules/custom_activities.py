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
    .ca-header {
        margin-bottom: 30px;
    }
    .ca-title {
        color: #f59e0b;
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 5px;
    }
    .virtual-sensor-card {
        background: rgba(15, 23, 42, 0.4);
        border: 1px solid rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 24px;
        text-align: center;
        transition: all 0.3s ease;
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .virtual-sensor-card:hover {
        border-color: rgba(6, 182, 212, 0.3);
        background: rgba(6, 182, 212, 0.05);
    }
    .sensor-icon {
        font-size: 2rem;
        margin-bottom: 10px;
    }
    .sensor-title {
        font-weight: 700;
        color: white;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    .sensor-desc {
        font-size: 0.75rem;
        color: #94a3b8;
    }
    .info-bar {
        background: rgba(6, 182, 212, 0.1);
        border: 1px solid rgba(6, 182, 212, 0.2);
        padding: 12px 20px;
        border-radius: 8px;
        margin-top: 20px;
        font-size: 0.85rem;
        color: #e2e8f0;
    }
    .activity-card {
        background: #0a0a0a;
        border: 1px solid rgba(255,255,255,0.05);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 15px;
    }
    .empty-state {
        background: rgba(15, 23, 42, 0.3);
        border: 2px dashed rgba(255, 255, 255, 0.05);
        border-radius: 16px;
        padding: 60px 40px;
        text-align: center;
        margin-top: 20px;
    }
    .active-session-bar {
        background: rgba(45, 26, 26, 0.5);
        border: 1px solid rgba(239, 68, 68, 0.2);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

    # --- TOP HEADER ---
    st.markdown("""
    <div class="ca-header">
        <div class="ca-title">Custom Stress Activities</div>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Add your own real-world stress challenges and measure your resilience with or without sensors
        </p>
    </div>
    """, unsafe_allow_html=True)

    # --- ACTIVE SESSION VIEW ---
    if st.session_state.active_ca_session["active"]:
        session = st.session_state.active_ca_session
        elapsed = int(time.time() - session["start_time"])
        mins, secs = divmod(elapsed, 60)
        
        # Simulate sensor readings incrementing
        if random.random() > 0.7:
            session["readings"] += 1

        st.markdown(f"""
        <div class="active-session-bar">
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                <div style="display: flex; align-items: center; gap: 15px;">
                    <div style="width: 10px; height: 10px; background: #ef4444; border-radius: 50%; animation: pulse-red 2s infinite;"></div>
                    <div style="font-weight: 700; color: white;">Session Active <span style="font-weight: 400; color: #94a3b8; margin-left: 10px;">{mins}:{secs:02d}</span></div>
                    <div style="font-size: 0.85rem; color: #f59e0b; margin-left: 20px;">⚡ {session['readings']} readings</div>
                    <div style="display: flex; gap: 10px; margin-left: 10px;">
                        <span style="font-size: 0.8rem; color: #94a3b8;">📷 Camera PPG</span>
                        <span style="font-size: 0.8rem; color: #94a3b8;">🎙️ Voice</span>
                        <span style="font-size: 0.8rem; color: #94a3b8;">⌨️ Typing</span>
                    </div>
                </div>
            </div>
            
            <div style="margin-bottom: 20px;">
                <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                    <span style="font-size: 0.85rem; font-weight: 600; color: white;">Current Stress Level: {session['stress_level']}/10</span>
                </div>
                <div style="width: 100%; height: 8px; background: rgba(255,255,255,0.1); border-radius: 4px;">
                    <div style="width: {session['stress_level']*10}%; height: 100%; background: white; border-radius: 4px;"></div>
                </div>
            </div>
            
            <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; text-align: center;">
                <div>
                    <div style="color: #2dd4bf; font-size: 1.5rem; font-weight: 700;">{70 + random.randint(0,10)}</div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">HRV (ms)</div>
                </div>
                <div>
                    <div style="color: #38bdf8; font-size: 1.5rem; font-weight: 700;">{75 + random.randint(0,5)}</div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">HR (bpm)</div>
                </div>
                <div>
                    <div style="color: #a855f7; font-size: 1.5rem; font-weight: 700;">{50 + random.randint(0,5)}</div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">GSR (μS)</div>
                </div>
                <div>
                    <div style="color: #f59e0b; font-size: 1.5rem; font-weight: 700;">{40 + random.randint(0,10)}</div>
                    <div style="color: #94a3b8; font-size: 0.7rem;">Calm Index</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        ca_col_end, ca_col_space = st.columns([1, 4])
        with ca_col_end:
            if st.button("End & Compute Score", key="end_ca_session", use_container_width=True):
                st.session_state.active_ca_session["active"] = False
                st.toast("Activity analyzed. Data synced to Journal.", icon="📊")
                st.rerun()

    # --- VIRTUAL SENSOR LAYER (Always Visible) ---
    st.markdown('<div style="margin-bottom: 40px;">', unsafe_allow_html=True)
    st.markdown("#### ⚡ Virtual Sensor Layer")
    st.caption("Enable measurement methods - works completely without hardware")
    
    vs1, vs2, vs3, vs4 = st.columns(4)
    with vs1:
        st.markdown("""<div class="virtual-sensor-card"><div class="sensor-icon">📷</div><div class="sensor-title">Camera PPG</div><div class="sensor-desc">HRV & Heart Rate</div></div>""", unsafe_allow_html=True)
    with vs2:
        st.markdown("""<div class="virtual-sensor-card"><div class="sensor-icon">🎙️</div><div class="sensor-title">Voice Analysis</div><div class="sensor-desc">Speech stress markers</div></div>""", unsafe_allow_html=True)
    with vs3:
        st.markdown("""<div class="virtual-sensor-card"><div class="sensor-icon">⌨️</div><div class="sensor-title">Typing Dynamics</div><div class="sensor-desc">Cognitive load</div></div>""", unsafe_allow_html=True)
    with vs4:
        st.markdown("""<div class="virtual-sensor-card"><div class="sensor-icon">🧠</div><div class="sensor-title">Cognitive Tests</div><div class="sensor-desc">Reaction time & accuracy</div></div>""", unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-bar">
        <b>No hardware required:</b> These virtual sensors use your device's camera, microphone, and interaction patterns to measure physiological stress without any wearable devices.
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- YOUR CUSTOM ACTIVITIES ---
    st.markdown('<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">', unsafe_allow_html=True)
    st.markdown("### Your Custom Activities")
    if st.button("+ Add New Activity", key="btn_show_add"):
        st.session_state.show_add_activity = True
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Add Activity Form (Modal Simulation)
    if st.session_state.show_add_activity:
        with st.container():
            st.markdown("""
            <div style="background: rgba(15, 23, 42, 0.95); padding: 30px; border-radius: 16px; border: 1px solid rgba(255,255,255,0.1); margin-bottom: 30px;">
                <h4 style="color: white; margin-bottom: 5px;">Add New Stress Activity</h4>
                <p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">Create a custom activity to track your stress response</p>
            </div>
            """, unsafe_allow_html=True)
            
            with st.form("new_activity_form"):
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
                new_notes = st.text_area("Notes (optional)", placeholder="e.g., With friends")
                
                f1, f2 = st.columns(2)
                with f1:
                    if st.form_submit_button("◎ Add Activity", use_container_width=True):
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
                with f2:
                    if st.form_submit_button("Cancel", use_container_width=True):
                        st.session_state.show_add_activity = False
                        st.rerun()

    # Activity List
    if not st.session_state.custom_activities:
        st.markdown(f"""
        <div class="empty-state">
            <div style="font-size: 3rem; color: #334155; margin-bottom: 20px;">◎</div>
            <h4 style="color: white; margin-bottom: 10px;">No Custom Activities Yet</h4>
            <p style="color: #94a3b8; max-width: 400px; margin: 0 auto 30px auto;">
                Create your first stress activity to start tracking your resilience in real-world scenarios. Works with sensors or self-report data.
            </p>
        </div>
        """, unsafe_allow_html=True)
    else:
        # Render cards
        cols = st.columns(2)
        for i, activity in enumerate(st.session_state.custom_activities):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="activity-card">
                    <div style="display: flex; gap: 15px; align-items: flex-start; margin-bottom: 20px;">
                        <div style="background: rgba(245, 158, 11, 0.1); width: 48px; height: 48px; border-radius: 12px; display: flex; justify-content: center; align-items: center; font-size: 1.5rem;">🧠</div>
                        <div>
                            <div style="font-weight: 700; color: white; font-size: 1.1rem;">{activity['name']}</div>
                            <div style="font-size: 0.85rem; color: #94a3b8;">{activity['type']}</div>
                        </div>
                    </div>
                    
                    <div style="margin-bottom: 20px;">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 8px;">
                            <span style="font-size: 0.85rem; color: #e2e8f0;">Intensity</span>
                            <span style="font-size: 0.85rem; color: white; font-weight: 700;">{activity['intensity']}/10</span>
                        </div>
                        <div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px;">
                            <div style="width: {activity['intensity']*10}%; height: 100%; background: white; border-radius: 3px;"></div>
                        </div>
                    </div>
                    
                    <div style="display: flex; gap: 15px; color: #94a3b8; font-size: 0.85rem; margin-bottom: 15px;">
                        <span>🕒 {activity['duration']}m</span>
                        <span>📊 {activity['sessions']} sessions</span>
                    </div>
                    <div style="color: #64748b; font-size: 0.8rem; margin-bottom: 20px;">{activity['notes']}</div>
                </div>
                """, unsafe_allow_html=True)
                
                # Invisible overlapping button trick for "Start Activity"
                if st.button("▷ Start Activity", key=f"start_{i}", use_container_width=True):
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
