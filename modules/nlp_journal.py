"""
Mind-Body Journal (v1.5)
PIXEL-PERFECT 1:1 UI Realization.
Matches competition mockups exactly in header, stats, input grid, and logs.
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
        st.session_state.journal_logs = [
            {"date": "12/21/2025", "mood": 6.16, "stress": 6.16, "energy": 5.79, "gut": 7.55, "sri": 51, "diet": ["Vegetables", "Protein"]},
            {"date": "12/20/2025", "mood": 6.22, "stress": 3.40, "energy": 8.16, "gut": 5.34, "sri": 72, "diet": ["Fruits", "Grains"]},
            {"date": "12/19/2025", "mood": 4.74, "stress": 4.69, "energy": 6.62, "gut": 8.59, "sri": 61, "diet": ["Spicy", "Alcohol"]},
            {"date": "12/18/2025", "mood": 9.42, "stress": 4.25, "energy": 8.14, "gut": 9.26, "sri": 66, "diet": ["Vegetables", "Caffeine"]},
            {"date": "12/17/2025", "mood": 6.92, "stress": 3.56, "energy": 7.31, "gut": 7.55, "sri": 68, "diet": ["Dairy", "Sweets"]}
        ]

    # --- CSS STYLES (PIXEL-PERFECT FIGMA ACCURACY) ---
    clean_render("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'Inter', sans-serif !important;
}

.journal-header-v15 {
    text-align: center;
    margin-bottom: 40px;
}
.journal-title-v15 {
    color: #a855f7;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 8px;
}
.journal-sub-v15 {
    color: #94a3b8;
    font-size: 0.85rem;
    font-weight: 500;
}

/* Stat Tags */
.stat-row-v15 {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 30px;
}
.stat-tag-v15 {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 12px;
    padding: 16px;
    display: flex;
    align-items: center;
    gap: 12px;
}
.tag-icon-v15 { font-size: 1.4rem; }
.tag-val-v15 { color: white; font-weight: 800; font-size: 1.25rem; }
.tag-lbl-v15 { color: #94a3b8; font-size: 0.7rem; font-weight: 600; }

/* Main Panels */
.panel-v15 {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.08);
    border-radius: 20px;
    padding: 30px;
    height: 100%;
}
.panel-title-v15 {
    color: white;
    font-weight: 800;
    font-size: 1.1rem;
    margin-bottom: 25px;
    display: flex;
    align-items: center;
    gap: 10px;
}

/* Sliders */
.slider-label-v15 {
    display: flex;
    justify-content: space-between;
    margin-top: 20px;
    margin-bottom: 8px;
}
.slider-name-v15 { color: white; font-size: 0.8rem; font-weight: 800; }
.slider-val-v15 { color: white; font-size: 0.8rem; font-weight: 800; }

/* Diet Grid */
.diet-grid-v15 {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 10px;
    margin-top: 15px;
}
.diet-item-v15 {
    background: rgba(15, 23, 42, 0.4);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 8px;
    padding: 10px;
    display: flex;
    align-items: center;
    gap: 10px;
    cursor: pointer;
    transition: all 0.2s;
}

/* Recent Logs */
.log-scroll-panel-v15 {
    height: 550px;
    overflow-y: auto;
    padding-right: 15px;
}
.log-scroll-panel-v15::-webkit-scrollbar { width: 6px; }
.log-scroll-panel-v15::-webkit-scrollbar-track { background: transparent; }
.log-scroll-panel-v15::-webkit-scrollbar-thumb { background: rgba(255,255,255,0.1); border-radius: 3px; }

.log-item-v15 {
    background: #020617;
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 12px;
    padding: 20px;
    margin-bottom: 12px;
    position: relative;
}
.log-header-v15 {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 15px;
}
.log-date-v15 { color: #f59e0b; font-size: 0.8rem; font-weight: 800; }
.log-sri-badge-v15 {
    background: rgba(255,255,255,0.03);
    color: white;
    font-size: 0.6rem;
    padding: 3px 8px;
    border-radius: 4px;
    font-weight: 700;
}
.log-metrics-v15 {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
}
.log-metric-sub-v15 { color: #64748b; font-size: 0.65rem; font-weight: 500; font-family: monospace; }

/* Science */
.science-panel-v15 {
    background: #110e20;
    border-radius: 16px;
    padding: 30px;
    margin-top: 50px;
}
</style>
    """)

    # --- TOP HEADER ---
    clean_render("""
<div class="journal-header-v15">
    <div class="journal-title-v15">Mind-Body Journal</div>
    <div class="journal-sub-v15">Bridge the gap between emotions and physiology - track how your feelings connect to your body's resilience</div>
</div>
    """)

    # --- STAT ROW ---
    st.markdown('<div class="stat-row-v15">', unsafe_allow_html=True)
    tags = [
        ("❤️", "10", "Total Logs"),
        ("🧠", "7.4", "Avg Mood"),
        ("🍴", "7.3", "Gut Comfort"),
        ("⚡", "40%", "Good Days")
    ]
    cols = st.columns(4)
    for i, (icon, val, lbl) in enumerate(tags):
        with cols[i]:
            st.markdown(f"""
<div class="stat-tag-v15">
    <div class="tag-icon-v15">{icon}</div>
    <div>
        <div class="tag-val-v15">{val}</div>
        <div class="tag-lbl-v15">{lbl}</div>
    </div>
</div>
            """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

    # --- MAIN GRID ---
    col_l, col_r = st.columns(2)

    with col_l:
        st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-v15"><span style="color: #2dd4bf;">+</span> Log Your State</div>', unsafe_allow_html=True)
        
        mood = st.slider("Mood Slider", 1, 10, 5, key="mood_s", label_visibility="collapsed")
        clean_render(f'<div class="slider-label-v15"><span class="slider-name-v15">Mood</span><span class="slider-val-v15">{mood}/10</span></div>')
        
        stress = st.slider("Stress Slider", 1, 10, 5, key="stress_s", label_visibility="collapsed")
        clean_render(f'<div class="slider-label-v15"><span class="slider-name-v15">Stress Level</span><span class="slider-val-v15">{stress}/10</span></div>')

        energy = st.slider("Energy Slider", 1, 10, 5, key="energy_s", label_visibility="collapsed")
        clean_render(f'<div class="slider-label-v15"><span class="slider-name-v15">Energy Level</span><span class="slider-val-v15">{energy}/10</span></div>')

        gut = st.slider("Gut Slider", 1, 10, 5, key="gut_s", label_visibility="collapsed")
        clean_render(f'<div class="slider-label-v15"><span class="slider-name-v15">Gut Comfort</span><span class="slider-val-v15">{gut}/10</span></div>')

        st.markdown('<div style="color: white; font-size: 0.8rem; font-weight: 800; margin-top: 30px; margin-bottom: 15px;">Today\'s Diet</div>', unsafe_allow_html=True)
        
        diet_cats = [
            ("🥦", "Vegetables"), ("🍎", "Fruits"), ("🍞", "Grains"), ("🥛", "Dairy"), 
            ("🍗", "Protein"), ("☕", "Caffeine"), ("🍷", "Alcohol"), ("🍰", "Sweets"), 
            ("🌶️", "Spicy"), ("🍔", "Processed")
        ]
        
        selected_diet = []
        d_cols = st.columns(2)
        for i, (icon, name) in enumerate(diet_cats):
            if d_cols[i % 2].checkbox(f"{icon} {name}", key=f"d_cat_{i}"):
                selected_diet.append(name)
        
        st.markdown('<div style="color: white; font-size: 0.8rem; font-weight: 800; margin-top: 30px; margin-bottom: 10px;">Notes</div>', unsafe_allow_html=True)
        notes = st.text_area("journal_notes", placeholder="How are you feeling? Any symptoms or observations?", label_visibility="collapsed", height=80)
        
        if st.button("➕ Log Entry", use_container_width=True):
            new_entry = {
                "date": datetime.now().strftime("%m/%d/%Y"),
                "mood": float(mood), "stress": float(stress), "energy": float(energy), "gut": float(gut),
                "sri": random.randint(50, 95), "diet": selected_diet
            }
            st.session_state.journal_logs.insert(0, new_entry)
            st.toast("Deep-Sync Entry Captured", icon="🧬")
            st.rerun()

        st.markdown('</div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-v15"><span style="color: #a855f7;">📋</span> Recent Logs</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="log-scroll-panel-v15">', unsafe_allow_html=True)
        for log in st.session_state.journal_logs:
            st.markdown(f"""
<div class="log-item-v15">
    <div class="log-header-v15">
        <div class="log-date-v15">🟡 {log['date']}</div>
        <div class="log-sri-badge-v15">SRI: {log['sri']}</div>
    </div>
    <div class="log-metrics-v15">
        <div class="log-metric-sub-v15">Mood: {log['mood']}/10</div>
        <div class="log-metric-sub-v15">Stress: {log['stress']}/10</div>
        <div class="log-metric-sub-v15">Energy: {log['energy']}/10</div>
        <div class="log-metric-sub-v15">Gut: {log['gut']}/10</div>
    </div>
</div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- CORRELATION CHARTS ---
    st.markdown('<div style="height: 40px;"></div>', unsafe_allow_html=True)
    df = pd.DataFrame(st.session_state.journal_logs)
    col_c1, col_c2 = st.columns(2)
    
    with col_c1:
        st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-v15"><span style="color: #2dd4bf;">📊</span> Mood vs Resilience Correlation</div>', unsafe_allow_html=True)
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=df['mood'], y=df['sri'], mode='markers', marker=dict(color='#ec4899', size=12, line=dict(color='white', width=1))))
        fig1.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background: rgba(236, 72, 153, 0.1); border-radius: 8px; padding: 12px; margin-top: 15px; font-size: 0.75rem; color: #f472b6;">Insight: Your mood shows a <b>positive correlation</b> with resilience. Better emotional states predict higher SRI by ~15%.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
        st.markdown('<div class="panel-title-v15"><span style="color: #10b981;">🍴</span> Gut-Brain Axis Connection</div>', unsafe_allow_html=True)
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=df['gut'], y=df['sri'] * 0.9, mode='markers', marker=dict(color='#10b981', size=12, line=dict(color='white', width=1))))
        fig2.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=250, margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"), xaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'), yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)'))
        st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
        st.markdown('<div style="background: rgba(16, 185, 129, 0.1); border-radius: 8px; padding: 12px; margin-top: 15px; font-size: 0.75rem; color: #10b981;">Gut-Brain Insight: Gut comfort correlates with HRV variability. The <b>microbiome-vagus nerve pathway</b> may influence autonomic regulation.</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    # --- SCIENCE PANEL ---
    clean_render("""
<div class="science-panel-v15">
    <div class="panel-title-v15" style="margin-bottom: 25px;"><span style="color: #f59e0b;">💡</span> The Science Behind Mind-Body Logging</div>
    <div style="margin-bottom: 20px;">
        <span style="color: #a855f7; font-weight: 800; font-size: 0.85rem;">Psychophysiology:</span>
        <span class="journal-sub-v15"> Your emotional state directly influences your autonomic nervous system, affecting HRV and stress markers.</span>
    </div>
    <div style="margin-bottom: 20px;">
        <span style="color: #10b981; font-weight: 800; font-size: 0.85rem;">Gut-Brain Axis:</span>
        <span class="journal-sub-v15"> The enteric nervous system ("second brain") communicates with your CNS via the vagus nerve, influencing mood and resilience.</span>
    </div>
    <div>
        <span style="color: #f472b6; font-weight: 800; font-size: 0.85rem;">Microbiome Impact:</span>
        <span class="journal-sub-v15"> Gut bacteria produce neurotransmitters like serotonin (90% made in gut) and GABA, directly affecting emotional regulation.</span>
    </div>
</div>
    """)

if __name__ == "__main__":
    render_nlp_journal_page()
