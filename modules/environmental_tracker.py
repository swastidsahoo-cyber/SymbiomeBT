"""
Environmental Symbiome Feedback (v2.0)
COMPLETE REWRITE - BULLETPROOF HTML RENDERING
Zero indentation, direct variable injection for guaranteed visual rendering.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
import random
import time
import pandas as pd
from datetime import datetime

def render_environmental_tracker_page():
    # CSS - stored in variable with ZERO indentation
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; }
.env-header-v15 { text-align: center; margin-bottom: 40px; }
.env-title-v15 { color: #f59e0b; font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.env-sub-v15 { color: #94a3b8; font-size: 0.85rem; font-weight: 500; }
.env-stat-row-v15 { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; margin-bottom: 30px; }
.env-stat-card-v15 { background: #020617; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 20px; position: relative; display: flex; flex-direction: column; }
.env-stat-tag-v15 { position: absolute; top: 10px; right: 10px; background: #111827; color: #10b981; font-size: 0.55rem; font-weight: 800; padding: 3px 6px; border-radius: 4px; }
.env-stat-icon-v15 { font-size: 1.2rem; margin-bottom: 8px; }
.env-stat-val-v15 { color: white; font-weight: 800; font-size: 1.5rem; line-height: 1; }
.env-stat-lbl-v15 { color: #94a3b8; font-size: 0.7rem; font-weight: 600; margin-top: 4px; }
.panel-v15 { background: #020617; border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 20px; padding: 30px; margin-bottom: 25px; }
.panel-title-v15 { color: white; font-weight: 800; font-size: 1rem; margin-bottom: 25px; display: flex; align-items: center; gap: 10px; }
.env-sl-lbl-v15 { display: flex; justify-content: space-between; margin-top: 15px; margin-bottom: 4px; }
.env-sl-name-v15 { color: white; font-size: 0.75rem; font-weight: 800; }
.env-sl-val-v15 { color: white; font-size: 0.75rem; font-weight: 800; }
.tip-item-v15 { background: #020617; border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 10px; padding: 16px; margin-bottom: 12px; display: flex; justify-content: space-between; align-items: center; }
.impact-tag-v15 { border: 1px solid #10b981; color: #10b981; font-size: 0.65rem; font-weight: 800; padding: 2px 6px; border-radius: 4px; }
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Header
    header_html = """<div class="env-header-v15">
<div class="env-title-v15">Environmental Symbiome Feedback</div>
<div class="env-sub-v15">How your surrounding environment shapes your physiological resilience</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Sensor Row
    st.markdown('<div class="env-stat-row-v15">', unsafe_allow_html=True)
    sensors = [
        ("☀️", "65 %", "Light Intensity"),
        ("🔊", "39 dB", "Ambient Noise"),
        ("🌡️", "21 °C", "Temperature"),
        ("💧", "69 %", "Humidity")
    ]
    cols = st.columns(4)
    for i, (icon, val, lbl) in enumerate(sensors):
        with cols[i]:
            sensor_html = f"""<div class="env-stat-card-v15">
<div class="env-stat-tag-v15">Optimal</div>
<div class="env-stat-icon-v15">{icon}</div>
<div class="env-stat-val-v15">{val}</div>
<div class="env-stat-lbl-v15">{lbl}</div>
</div>"""
            st.markdown(sensor_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Live Impact Model
    st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title-v15"><span style="color: #a855f7;">⚡</span> Live Environmental Impact Model</div>', unsafe_allow_html=True)
    
    col_sl, col_res = st.columns([1.8, 1])
    with col_sl:
        l_s = st.slider("L", 0, 100, 65, key="l_s", label_visibility="collapsed")
        st.markdown(f'<div class="env-sl-lbl-v15"><span class="env-sl-name-v15">💡 Light Exposure</span><span class="env-sl-val-v15">{l_s}%</span></div>', unsafe_allow_html=True)
        
        n_s = st.slider("N", 20, 100, 39, key="n_s", label_visibility="collapsed")
        st.markdown(f'<div class="env-sl-lbl-v15"><span class="env-sl-name-v15">🔊 Noise Level</span><span class="env-sl-val-v15">{n_s} dB</span></div>', unsafe_allow_html=True)

        t_s = st.slider("T", 10, 40, 21, key="t_s", label_visibility="collapsed")
        st.markdown(f'<div class="env-sl-lbl-v15"><span class="env-sl-name-v15">🌡️ Temperature</span><span class="env-sl-val-v15">{t_s}°C</span></div>', unsafe_allow_html=True)

    with col_res:
        # Calculate Mock Impact
        optimality = 100 - abs(l_s - 65) - abs(n_s - 39) - abs(t_s - 21)
        optimality = max(0, min(100, optimality))
        impact = (optimality - 50) / 2
        
        impact_html = f"""<div style="padding-top: 15px; text-align: right;">
<div style="color: #94a3b8; font-size: 0.75rem; font-weight: 700; margin-bottom: 5px;">Predicted SRI Impact</div>
<div style="color: #10b981; font-size: 2.2rem; font-weight: 900;">{'+' if impact >=0 else ''}{impact:.1f}%</div>
<div style="margin-top: 40px;">
<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;">
<span style="color: #94a3b8; font-size: 0.75rem; font-weight: 700;">Optimality Score</span>
<span style="color: white; font-size: 0.8rem; font-weight: 800;">{int(optimality)}/100</span>
</div>
<div style="width: 100%; height: 6px; background: rgba(255,255,255,0.05); border-radius: 3px;">
<div style="width: {optimality}%; height: 100%; background: white; border-radius: 3px;"></div>
</div>
</div>
</div>"""
        st.markdown(impact_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Curve Charts
    col_c1, col_c2 = st.columns(2)
    with col_c1:
        st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
        st.markdown('<div style="color: white; font-weight: 800; font-size: 0.85rem; margin-bottom: 15px;">Light vs Resilience</div>', unsafe_allow_html=True)
        x = np.linspace(20, 100, 50)
        y = 50 + 25 * np.exp(-((x - 70)**2) / 350)
        fig_l = go.Figure()
        fig_l.add_trace(go.Scatter(x=x, y=y, fill='tozeroy', line=dict(color='#f59e0b'), fillcolor='rgba(245, 158, 11, 0.1)'))
        fig_l.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False, title_text="Light (%)", title_font=dict(size=10, color="#64748b")), yaxis=dict(showgrid=True, gridcolor='#1e293b', range=[40, 90]))
        st.plotly_chart(fig_l, use_container_width=True, key="l_v_r")
        st.markdown('<div style="color: #94a3b8; font-size: 0.65rem; margin-top: 10px;">Moderate light (60-80%) correlates with optimal resilience</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_c2:
        st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
        st.markdown('<div style="color: white; font-weight: 800; font-size: 0.85rem; margin-bottom: 15px;">Noise vs Resilience</div>', unsafe_allow_html=True)
        x_n = np.linspace(20, 100, 50)
        y_n = 75 - 0.4 * x_n + np.random.normal(0, 1, 50)
        fig_n = go.Figure()
        fig_n.add_trace(go.Scatter(x=x_n, y=y_n, line=dict(color='#3b82f6', width=2)))
        fig_n.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=220, margin=dict(l=0,r=0,t=0,b=0), xaxis=dict(showgrid=False, title_text="Noise (dB)", title_font=dict(size=10, color="#64748b")), yaxis=dict(showgrid=True, gridcolor='#1e293b', range=[40, 90]))
        st.plotly_chart(fig_n, use_container_width=True, key="n_v_r")
        st.markdown('<div style="color: #94a3b8; font-size: 0.65rem; margin-top: 10px;">Higher ambient noise (>70dB) reduces resilience by average 14%</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # 24-Hour Pattern
    st.markdown('<div class="panel-v15">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title-v15"><span style="color: #2dd4bf;">🕒</span> 24-Hour Resilience & Light Pattern</div>', unsafe_allow_html=True)
    
    hours = [f"{i}:00" for i in range(24)]
    sri_24 = [30, 28, 32, 40, 45, 60, 65, 72, 75, 72, 70, 78, 80, 78, 75, 72, 70, 65, 58, 50, 45, 40, 35, 30]
    l_24 = [10, 10, 10, 20, 45, 90, 85, 80, 88, 92, 90, 85, 88, 80, 90, 85, 80, 50, 15, 10, 10, 10, 10, 10]
    
    fig_24 = go.Figure()
    fig_24.add_trace(go.Scatter(x=hours, y=l_24, name="Light", fill='tozeroy', line=dict(color='#f59e0b', dash='dot'), fillcolor='rgba(245, 158, 11, 0.05)', yaxis='y2'))
    fig_24.add_trace(go.Scatter(x=hours, y=sri_24, name="SRI", line=dict(color='#2dd4bf', width=3)))
    
    fig_24.update_layout(
        paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', height=320, 
        margin=dict(l=0,r=0,t=10,b=0), font=dict(color="#94a3b8"),
        xaxis=dict(showgrid=False, tickvals=hours[::4]),
        yaxis=dict(showgrid=True, gridcolor='#1e293b', title="SRI", range=[0, 110]),
        yaxis2=dict(overlaying='y', side='right', title="Light", range=[0, 110], showgrid=False),
        legend=dict(orientation="h", y=-0.2)
    )
    st.plotly_chart(fig_24, use_container_width=True, key="p24h")
    
    # Day/Night Insight Badges
    b_c1, b_c2 = st.columns(2)
    with b_c1:
        badge1_html = """<div style="background: #020617; border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 15px; display: flex; gap: 12px; border-left: 3px solid #f59e0b;">
<div style="font-size: 1.2rem;">☀️</div>
<div>
<div style="color: white; font-weight: 800; font-size: 0.75rem;">Day Pattern</div>
<div style="color: #64748b; font-size: 0.65rem; margin-top: 3px;">Morning sunlight exposure improves HRV by 12% and accelerates recovery</div>
</div>
</div>"""
        st.markdown(badge1_html, unsafe_allow_html=True)
    with b_c2:
        badge2_html = """<div style="background: #020617; border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 15px; display: flex; gap: 12px; border-left: 3px solid #3b82f6;">
<div style="font-size: 1.2rem;">🌙</div>
<div>
<div style="color: white; font-weight: 800; font-size: 0.75rem;">Night Pattern</div>
<div style="color: #64748b; font-size: 0.65rem; margin-top: 3px;">Low light after 10 PM supports natural cortisol reduction and sleep quality</div>
</div>
</div>"""
        st.markdown(badge2_html, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Tips
    st.markdown('<div style="font-weight: 800; color: white; font-size: 1.1rem; margin-bottom: 25px;">Environmental Optimization Tips</div>', unsafe_allow_html=True)
    tips = [
        ("💡", "Optimize your workspace lighting", "Try 60-70% brightness with natural light exposure for peak resilience", "+8% SRI"),
        ("🔇", "Create quiet zones during peak stress", "Reduce ambient noise below 50dB during focused work or recovery sessions", "+12% recovery speed"),
        ("🌡️", "Maintain thermal comfort", "Keep temperature between 20-22°C for optimal autonomic balance", "+6% HRV"),
        ("🌅", "Morning light ritual", "15 minutes of bright light exposure within 1 hour of waking", "+18% morning resilience")
    ]
    for i, t, d, tg in tips:
        tip_html = f"""<div class="tip-item-v15">
<div style="display: flex; gap: 15px; align-items: flex-start;">
<div style="font-size: 1.2rem;">{i}</div>
<div>
<div style="color: white; font-weight: 800; font-size: 0.85rem;">{t}</div>
<div style="color: #94a3b8; font-size: 0.75rem; margin-top: 4px;">{d}</div>
</div>
</div>
<div class="impact-tag-v15">{tg}</div>
</div>"""
        st.markdown(tip_html, unsafe_allow_html=True)

if __name__ == "__main__":
    render_environmental_tracker_page()
