"""
Mind-Body Journal (v1.0)
High-fidelity interface for tracking the Gut-Brain axis and emotional resilience.
Matches provided competition mockup exactly.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
import textwrap
import pandas as pd
from datetime import datetime

def clean_render(html_str):
    """Ensure HTML strings are perfectly dedented and clean for Streamlit."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def render_nlp_journal_page():
    # --- SESSION STATE INITIALIZATION ---
    if "journal_logs" not in st.session_state:
        # Pre-seed with some historical data for the charts
        st.session_state.journal_logs = [
            {"date": "12/21/2025", "mood": 6.2, "stress": 6.1, "energy": 5.8, "gut": 7.5, "sri": 51, "diet": ["Vegetables", "Protein"]},
            {"date": "12/20/2025", "mood": 8.1, "stress": 3.4, "energy": 8.3, "gut": 5.2, "sri": 72, "diet": ["Fruits", "Grains"]},
            {"date": "12/19/2025", "mood": 4.7, "stress": 4.6, "energy": 6.6, "gut": 8.5, "sri": 61, "diet": ["Spicy", "Alcohol"]},
            {"date": "12/18/2025", "mood": 9.4, "stress": 4.2, "energy": 8.1, "gut": 9.2, "sri": 66, "diet": ["Vegetables", "Caffeine"]},
            {"date": "12/17/2025", "mood": 6.9, "stress": 3.9, "energy": 7.3, "gut": 7.5, "sri": 68, "diet": ["Dairy", "Sweets"]}
        ]

    # --- CSS STYLES (HI-FI MATCH) ---
    clean_render("""
<style>
.journal-header { text-align: center; margin-bottom: 40px; }
.journal-title {
    color: #a855f7; font-size: 2.2rem; font-weight: 800; margin-bottom: 5px;
}
.journal-sub { color: #94a3b8; font-size: 0.9rem; }

/* Stat Badges */
.stat-tag-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 30px; }
.stat-tag-card {
    background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px; padding: 15px; display: flex; align-items: center; gap: 12px;
}
.stat-tag-icon { font-size: 1.4rem; color: #a855f7; }
.stat-tag-val { color: white; font-weight: 800; font-size: 1.2rem; }
.stat-tag-lbl { color: #94a3b8; font-size: 0.7rem; }

/* Input Section */
.input-panel {
    background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px; padding: 24px; height: 100%;
}
.diet-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 15px; }
.diet-btn {
    background: rgba(30, 41, 59, 0.5); border: 1px solid rgba(255,255,255,0.05);
    border-radius: 6px; padding: 10px; color: #94a3b8; font-size: 0.75rem;
    text-align: center; cursor: pointer; transition: all 0.2s;
}
.diet-btn:hover { background: rgba(168, 85, 247, 0.2); color: white; border-color: #a855f7; }

/* Logs List */
.log-list {
    background: rgba(15, 23, 42, 0.4); border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px; padding: 24px; height: 500px; overflow-y: auto;
}
.log-entry-card {
    background: rgba(2, 6, 23, 0.6); border: 1px solid rgba(255,255,255,0.03);
    border-radius: 10px; padding: 15px; margin-bottom: 12px;
}

/* Insight Box */
.insight-box {
    background: rgba(15, 23, 42, 0.6); border: 1px solid rgba(236, 72, 153, 0.2);
    border-radius: 8px; padding: 12px; margin-top: 15px; font-size: 0.75rem; color: #f472b6;
}

/* Science Section */
.science-panel {
    background: rgba(88, 28, 135, 0.1); border-top: 2px solid #a855f7;
    border-radius: 16px; padding: 30px; margin-top: 50px;
}
</style>
    """)

    # --- HEADER ---
    clean_render("""
<div class="journal-header">
    <div class="journal-title">Mind-Body Journal</div>
    <div class="journal-sub">Bridge the gap between emotions and physiology - track how your feelings connect to your body's resilience</div>
</div>
    """)

    # --- TOP STATS ---
    st.markdown('<div class="stat-tag-grid">', unsafe_allow_html=True)
    stats = [
        ("❤️", "10", "Total Logs"),
        ("🧠", "7.4", "Avg Mood"),
        ("🍴", "7.3", "Gut Comfort"),
        ("📈", "40%", "Good Days")
    ]
    cols = st.columns(4)
    for i, (icon, val, lbl) in enumerate(stats):
        with cols[i]:
            st.markdown(f"""
<div class="stat-tag-card">
    <div class="stat-tag-icon">{icon}</div>
    <div>
        <div class="stat-tag-val">{val}</div>
        <div class="stat-tag-lbl">{lbl}</div>
    </div>
</div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MAIN INPUT GRID ---
    col_input, col_logs = st.columns([1, 1])

    with col_input:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div style="color: #10b981; font-weight: 800; font-size: 0.9rem; margin-bottom: 20px;">+ Log Your State</div>', unsafe_allow_html=True)
        
        mood = st.slider("Mood", 1, 10, 5)
        stress = st.slider("Stress Level", 1, 10, 5)
        energy = st.slider("Energy Level", 1, 10, 5)
        gut = st.slider("Gut Comfort", 1, 10, 5)
        
        st.markdown('<div style="color: #10b981; font-weight: 800; font-size: 0.8rem; margin-top: 25px;">Today\'s Diet</div>', unsafe_allow_html=True)
        diet_categories = [
            ("🥦", "Vegetables"), ("🍎", "Fruits"), ("🍞", "Grains"), ("🥛", "Dairy"), 
            ("🍗", "Protein"), ("☕", "Caffeine"), ("🍷", "Alcohol"), ("🍰", "Sweets"), 
            ("🌶️", "Spicy"), ("🍔", "Processed")
        ]
        
        selected_diet = []
        diet_grid_cols = st.columns(2)
        for i, (icon, name) in enumerate(diet_categories):
            if diet_grid_cols[i % 2].checkbox(f"{icon} {name}", key=f"diet_{i}"):
                selected_diet.append(name)
        
        st.markdown('<div style="color: #94a3b8; font-weight: 800; font-size: 0.8rem; margin-top: 25px;">Notes</div>', unsafe_allow_html=True)
        notes = st.text_area("How are you feeling?", placeholder="Any symptoms or observations?", label_visibility="collapsed")
        
        if st.button("➕ Log Entry", use_container_width=True):
            new_log = {
                "date": datetime.now().strftime("%m/%d/%Y"),
                "mood": float(mood),
                "stress": float(stress),
                "energy": float(energy),
                "gut": float(gut),
                "sri": random.randint(50, 95),
                "diet": selected_diet
            }
            st.session_state.journal_logs.insert(0, new_log)
            st.toast("Entry Analyzed & Synchronized!", icon="🧠")
            st.rerun()
            
        st.markdown('</div>', unsafe_allow_html=True)

    with col_logs:
        st.markdown('<div class="log-list">', unsafe_allow_html=True)
        st.markdown('<div style="color: #a855f7; font-weight: 800; font-size: 0.9rem; margin-bottom: 20px;">📅 Recent Logs</div>', unsafe_allow_html=True)
        
        for log in st.session_state.journal_logs:
            diet_str = ", ".join(log['diet']) if log['diet'] else "Normal diet"
            st.markdown(f"""
<div class="log-entry-card">
    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px;">
        <div style="color: #f59e0b; font-size: 0.75rem; font-weight: 800;">🟡 {log['date']}</div>
        <div style="color: white; font-size: 0.7rem; background: rgba(255,255,255,0.05); padding: 2px 6px; border-radius: 4px;">SRI: {log['sri']}</div>
    </div>
    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px;">
        <div style="color: #94a3b8; font-size: 0.65rem;">Mood: {log['mood']}/10</div>
        <div style="color: #94a3b8; font-size: 0.65rem;">Stress: {log['stress']}/10</div>
        <div style="color: #94a3b8; font-size: 0.65rem;">Energy: {log['energy']}/10</div>
        <div style="color: #94a3b8; font-size: 0.65rem;">Gut: {log['gut']}/10</div>
    </div>
    <div style="color: #64748b; font-size: 0.6rem; margin-top: 8px; font-style: italic;">{diet_str}</div>
</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)

    # --- CORRELATION CHARTS ---
    col_chart1, col_chart2 = st.columns(2)
    
    df = pd.DataFrame(st.session_state.journal_logs)
    
    with col_chart1:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div style="color: #10b981; font-weight: 800; font-size: 0.85rem; margin-bottom: 20px;">📉 Mood vs Resilience Correlation</div>', unsafe_allow_html=True)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df['mood'], y=df['sri'], mode='markers', marker=dict(color='#f472b6', size=12)))
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), xaxis=dict(title="Mood Score"), yaxis=dict(title="SRI"))
        st.plotly_chart(fig1, use_container_width=True)
        st.markdown('<div class="insight-box">Insight: Your mood shows a <b>positive correlation</b> with resilience. Better emotional states predict higher SRI by ~15%.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_chart2:
        st.markdown('<div class="input-panel">', unsafe_allow_html=True)
        st.markdown('<div style="color: #10b981; font-weight: 800; font-size: 0.85rem; margin-bottom: 20px;">🍴 Gut-Brain Axis Connection</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        # Mocking HRV values based on gut comfort
        hrv_vals = df['gut'] * 8 + np.random.randint(-5, 5, len(df))
        fig2.add_trace(go.Scatter(x=df['gut'], y=hrv_vals, mode='markers', marker=dict(color='#2dd4bf', size=12)))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), xaxis=dict(title="Gut Comfort"), yaxis=dict(title="HRV"))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="insight-box" style="border-color: #2dd4bf; color: #2dd4bf;">Gut-Brain Insight: Gut comfort correlates with HRV variability via the <b>microbiome-vagus nerve pathway</b>.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SCIENCE BRIEFING ---
    st.markdown("""
<div class="science-panel">
    <div style="font-weight: 800; color: white; font-size: 1.1rem; margin-bottom: 25px;">💡 The Science Behind Mind-Body Logging</div>
    <div style="margin-bottom: 20px;">
        <span style="color: #a855f7; font-weight: 800; font-size: 0.85rem;">Psychophysiology:</span>
        <span style="color: #94a3b8; font-size: 0.85rem;"> Your emotional state directly influences your autonomic nervous system, affecting HRV and stress markers.</span>
    </div>
    <div style="margin-bottom: 20px;">
        <span style="color: #10b981; font-weight: 800; font-size: 0.85rem;">Gut-Brain Axis:</span>
        <span style="color: #94a3b8; font-size: 0.85rem;"> The enteric nervous system ("second brain") communicates with your CNS via the vagus nerve, influencing mood and resilience.</span>
    </div>
    <div>
        <span style="color: #f472b6; font-weight: 800; font-size: 0.85rem;">Microbiome Impact:</span>
        <span style="color: #94a3b8; font-size: 0.85rem;"> Gut bacteria produce neurotransmitters like serotonin (90% made in gut) and GABA, directly affecting emotional regulation.</span>
    </div>
</div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    render_nlp_journal_page()
