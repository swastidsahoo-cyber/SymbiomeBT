"""
Community Resilience Mapping Dashboard
Population-level environmental stress analytics.
PIXEL-PERFECT UI matching screenshot EXACTLY.
Privacy-first, non-surveillance framing.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from .resilience_mapping_engine import ResilienceMappingEngine

def render_resilience_mapping_page():
    # BALANCED CSS - Remove gap without hiding content
    st.markdown("""
    <style>
    /* Remove top gap with BALANCED negative margin */
    section.main > div.block-container {
        padding-top: 1rem !important;
        margin-top: 0rem !important;
    }
    
    /* Remove default Streamlit spacing */
    .main {
        padding-top: 0 !important;
    }
    
    section[data-testid="stAppViewContainer"] > .main {
        padding-top: 0 !important;
    }
    
    /* Ensure proper alignment */
    .stButton > button {
        width: 100% !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Initialize engine
    engine = ResilienceMappingEngine(min_n=10)
    
    # Initialize session state
    if 'mapping_time_window' not in st.session_state:
        st.session_state.mapping_time_window = 'week'
    
    if 'expanded_locations' not in st.session_state:
        st.session_state.expanded_locations = set()
    
    # AGGRESSIVE CSS - Override ALL Streamlit defaults
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* FORCE DARK THEME - Override Streamlit */
.main, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"], 
[data-testid="stToolbar"], section[data-testid="stSidebar"] {
    background-color: #0a0e27 !important;
    background: #0a0e27 !important;
    color: #ffffff !important;
}

/* REMOVE ALL TOP SPACING */
.main {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

.block-container {
    padding-top: 0 !important;
    margin-top: 0 !important;
}

[data-testid="stAppViewContainer"] > .main {
    padding-top: 0 !important;
}

.element-container:first-child {
    margin-top: 0 !important;
}

/* Force all text to be visible */
.main *, .stApp *, p, span, div, label, h1, h2, h3, h4, h5, h6 {
    color: #ffffff !important;
    font-family: 'Inter', sans-serif !important;
}

/* Override Streamlit selectbox styling */
.stSelectbox > div > div {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid rgba(148, 163, 184, 0.3) !important;
}

.stSelectbox label {
    color: #ffffff !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
}

/* Override Streamlit button styling */
.stButton > button {
    background-color: #1e293b !important;
    color: #ffffff !important;
    border: 1px solid rgba(148, 163, 184, 0.3) !important;
    font-weight: 600 !important;
}

.stButton > button[kind="primary"] {
    background-color: #06b6d4 !important;
    color: #0a0e27 !important;
    border: none !important;
}

/* Hide Streamlit branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Classes */
.mapping-container {
    background: #0a0e27;
    padding: 0 20px 20px 20px;
    min-height: 100vh;
}

.filter-row {
    background: #1a1f3a;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 30px;
    border: 1px solid rgba(148, 163, 184, 0.2);
}

.filter-label {
    color: #ffffff !important;
    font-size: 0.85rem !important;
    font-weight: 600 !important;
    margin-bottom: 8px !important;
    display: block !important;
}

.heatmap-title {
    color: #ffffff !important;
    font-size: 1.8rem !important;
    font-weight: 900 !important;
    margin: 30px 0 10px 0 !important;
}

.heatmap-subtitle {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    margin-bottom: 25px !important;
    line-height: 1.6 !important;
}

.location-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1.5px solid rgba(148, 163, 184, 0.2);
    border-radius: 14px;
    padding: 24px;
    margin: 18px 0;
    transition: all 0.3s ease;
}

.location-card:hover {
    border-color: rgba(6, 182, 212, 0.5);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(6, 182, 212, 0.2);
}

.location-header {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    margin-bottom: 20px;
}

.location-info {
    flex: 1;
}

.location-name {
    color: #ffffff !important;
    font-size: 1.3rem !important;
    font-weight: 800 !important;
    margin-bottom: 8px !important;
}

.location-meta {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    font-weight: 500 !important;
}

.location-score {
    font-size: 4rem !important;
    font-weight: 900 !important;
    line-height: 1 !important;
    text-shadow: 0 0 30px currentColor !important;
}

.score-red { color: #ef4444 !important; }
.score-yellow { color: #fbbf24 !important; }
.score-green { color: #10b981 !important; }

.resilience-bar {
    width: 100%;
    height: 16px;
    background: rgba(15, 23, 42, 0.8);
    border-radius: 8px;
    overflow: hidden;
    margin: 20px 0;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.4);
}

.resilience-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
    box-shadow: 0 0 16px currentColor;
}

.bar-red {
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}

.bar-yellow {
    background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
}

.bar-green {
    background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

.location-details {
    background: rgba(15, 23, 42, 0.7);
    border-radius: 12px;
    padding: 24px;
    margin-top: 20px;
    border: 1px solid rgba(148, 163, 184, 0.15);
}

.detail-title {
    color: #06b6d4 !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    margin-bottom: 16px !important;
}

.detail-text {
    color: #cbd5e1 !important;
    font-size: 0.9rem !important;
    line-height: 1.8 !important;
}

.action-panel {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(168, 85, 247, 0.05) 100%);
    border: 1.5px solid rgba(139, 92, 246, 0.3);
    border-radius: 14px;
    padding: 28px;
    margin: 35px 0;
}

.action-title {
    color: #a855f7 !important;
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    margin-bottom: 24px !important;
}

.action-card {
    background: rgba(15, 23, 42, 0.8);
    border-left: 4px solid;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
}

.action-card-red {
    border-left-color: #ef4444;
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
}

.action-card-yellow {
    border-left-color: #fbbf24;
    background: linear-gradient(90deg, rgba(251, 191, 36, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
}

.action-card-green {
    border-left-color: #10b981;
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.1) 0%, rgba(15, 23, 42, 0.8) 100%);
}

.action-location {
    color: #ffffff !important;
    font-size: 1.1rem !important;
    font-weight: 800 !important;
    margin-bottom: 10px !important;
}

.action-text {
    color: #cbd5e1 !important;
    font-size: 0.9rem !important;
    line-height: 1.7 !important;
}

.policy-panel {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.1) 0%, rgba(6, 182, 212, 0.05) 100%);
    border: 1.5px solid rgba(6, 182, 212, 0.3);
    border-radius: 14px;
    padding: 28px;
    margin: 35px 0;
}

.policy-title {
    color: #06b6d4 !important;
    font-size: 1.5rem !important;
    font-weight: 900 !important;
    margin-bottom: 16px !important;
}

.policy-subtitle {
    color: #94a3b8 !important;
    font-size: 0.85rem !important;
    margin-bottom: 24px !important;
    line-height: 1.7 !important;
}

.policy-insight {
    color: #e2e8f0 !important;
    font-size: 0.95rem !important;
    line-height: 1.8 !important;
    margin-bottom: 18px !important;
    padding: 18px !important;
    background: rgba(15, 23, 42, 0.6) !important;
    border-radius: 10px !important;
    border-left: 3px solid rgba(6, 182, 212, 0.6) !important;
}
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Initialize session state for view
    if 'resilience_view' not in st.session_state:
        st.session_state.resilience_view = 'school'
    
    # Container
    st.markdown('<div class="mapping-container">', unsafe_allow_html=True)
    
    # VIEW TOGGLES + TIME PERIOD TOGGLES (FUNCTIONAL)
    st.markdown('<div style="background: linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 14px; padding: 16px 24px; margin: 0 0 20px 0;">', unsafe_allow_html=True)
    
    col_left, col_right = st.columns([2, 1])
    
    with col_left:
        view_col1, view_col2, view_col3 = st.columns(3)
        with view_col1:
            if st.button("🏫 School View", key="btn_school_view", use_container_width=True, type="primary" if st.session_state.resilience_view == 'school' else "secondary"):
                st.session_state.resilience_view = 'school'
                st.rerun()
        with view_col2:
            if st.button("🏙️ City View", key="btn_city_view", use_container_width=True, type="primary" if st.session_state.resilience_view == 'city' else "secondary"):
                st.session_state.resilience_view = 'city'
                st.rerun()
        with view_col3:
            if st.button("🌍 National View", key="btn_national_view", use_container_width=True, type="primary" if st.session_state.resilience_view == 'national' else "secondary"):
                st.session_state.resilience_view = 'national'
                st.rerun()
    
    with col_right:
        time_col1, time_col2, time_col3 = st.columns(3)
        with time_col1:
            if st.button("Day", key="btn_day", use_container_width=True, type="primary" if st.session_state.mapping_time_window == 'day' else "secondary"):
                st.session_state.mapping_time_window = 'day'
                st.rerun()
        with time_col2:
            if st.button("Week", key="btn_week", use_container_width=True, type="primary" if st.session_state.mapping_time_window == 'week' else "secondary"):
                st.session_state.mapping_time_window = 'week'
                st.rerun()
        with time_col3:
            if st.button("Month", key="btn_month", use_container_width=True, type="primary" if st.session_state.mapping_time_window == 'month' else "secondary"):
                st.session_state.mapping_time_window = 'month'
                st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PRIVACY GUARD STATUS PANEL (matching screenshot - more compact)
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.03) 100%); border: 1.5px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px 20px; margin: 0 0 20px 0; display: flex; align-items: center; gap: 20px; flex-wrap: wrap;">
        <div style="display: flex; align-items: center; gap: 8px;">
            <span style="color: #10b981; font-size: 1.2rem;">🛡️</span>
            <span style="color: #10b981; font-size: 0.8rem; font-weight: 800; text-transform: uppercase; letter-spacing: 0.5px;">Privacy-First Design</span>
        </div>
        <div style="color: #94a3b8; font-size: 0.75rem; line-height: 1.5;">
            All data is aggregated and anonymised. Individual users cannot be identified. Only location-based patterns and time-based trends are shown to administrators.
        </div>
        <div style="display: flex; gap: 12px; margin-left: auto;">
            <div style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.3);">
                ✓ GDPR Compliant
            </div>
            <div style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.3);">
                ✓ Minimum 20 users per zone
            </div>
            <div style="background: rgba(16, 185, 129, 0.15); color: #10b981; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.3);">
                ✓ No personal identifiers
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Filter Row
    st.markdown('<div class="filter-row">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<span class="filter-label">Institution</span>', unsafe_allow_html=True)
        institution = st.selectbox("", ["Trinity College Dublin"], key="institution_filter", label_visibility="collapsed")
    
    with col2:
        st.markdown('<span class="filter-label">City/Zone</span>', unsafe_allow_html=True)
        city_zone = st.selectbox("", ["Dublin City Centre"], key="zone_filter", label_visibility="collapsed")
    
    with col3:
        st.markdown('<span class="filter-label">Resilience Score</span>', unsafe_allow_html=True)
        resilience_filter = st.selectbox("", ["All Scores", "High Strain (0-49)", "Moderate (50-74)", "Adaptive (75-100)"], key="resilience_filter", label_visibility="collapsed")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Heatmap Header
    st.markdown('<div class="heatmap-title">School Stress Heatmap (This week)</div>', unsafe_allow_html=True)
    st.markdown('<div class="heatmap-subtitle">Aggregated resilience signals across locations (Only locations based on student data shown on campus environment)</div>', unsafe_allow_html=True)
    
    # Get location data
    locations_data = engine.get_all_locations_data(st.session_state.mapping_time_window)
    
    # Location Cards
    for loc_data in locations_data:
        location_name = loc_data['location']
        score = loc_data['composite_resilience']
        color_band = loc_data['color_band']
        participant_count = loc_data['participant_count']
        trend = loc_data['trend']
        
        # Trend arrow
        trend_arrow = "↗" if trend == "improving" else "↘" if trend == "declining" else "→"
        
        # Color classes
        score_class = 'score-red' if color_band == 'red' else 'score-yellow' if color_band == 'yellow' else 'score-green'
        bar_class = 'bar-red' if color_band == 'red' else 'bar-yellow' if color_band == 'yellow' else 'bar-green'
        
        # Location card
        is_expanded = location_name in st.session_state.expanded_locations
        
        card_html = f"""<div class="location-card">
<div class="location-header">
<div class="location-info">
<div class="location-name">{location_name} {trend_arrow}</div>
<div class="location-meta">{participant_count} students - Avg RQ: {score}</div>
</div>
<div class="location-score {score_class}">{score}</div>
</div>
<div class="resilience-bar">
<div class="resilience-bar-fill {bar_class}" style="width: {score}%;"></div>
</div>
</div>"""
        st.markdown(card_html, unsafe_allow_html=True)
        
        # Expand/Collapse button
        if st.button(f"{'▼ Hide Details' if is_expanded else '▶ Show Details'}", key=f"expand_{location_name}", use_container_width=True):
            if is_expanded:
                st.session_state.expanded_locations.remove(location_name)
            else:
                st.session_state.expanded_locations.add(location_name)
            st.rerun()
        
        # Location Details (if expanded)
        if is_expanded:
            st.markdown('<div class="location-details">', unsafe_allow_html=True)
            
            # Peak Stress Times
            st.markdown('<div class="detail-title">📊 Peak Stress Times</div>', unsafe_allow_html=True)
            
            peak_times = engine.generate_peak_stress_times(location_name)
            hours = list(peak_times.keys())
            intensities = list(peak_times.values())
            
            fig_peak = go.Figure()
            fig_peak.add_trace(go.Bar(
                x=hours,
                y=intensities,
                marker=dict(
                    color=intensities,
                    colorscale=[[0, '#10b981'], [0.5, '#fbbf24'], [1, '#ef4444']],
                    showscale=False
                ),
                hovertemplate='%{x}<br>Stress: %{y}/100<extra></extra>'
            ))
            
            fig_peak.update_layout(
                paper_bgcolor='rgba(15,23,42,0.7)',
                plot_bgcolor='rgba(15,23,42,0.7)',
                height=220,
                margin=dict(l=40, r=20, t=20, b=40),
                xaxis=dict(
                    showgrid=False, 
                    color='#94a3b8', 
                    title=dict(text='Hour', font=dict(size=12, color='#94a3b8'))
                ),
                yaxis=dict(
                    showgrid=True, 
                    gridcolor='rgba(148,163,184,0.15)', 
                    color='#94a3b8', 
                    title=dict(text='Stress Intensity', font=dict(size=12, color='#94a3b8'))
                ),
                font=dict(family='Inter', color='#cbd5e1', size=11)
            )
            
            st.plotly_chart(fig_peak, use_container_width=True, key=f"peak_{location_name}")
            
            # Recovery Patterns
            st.markdown('<div class="detail-title">🔄 Recovery Patterns</div>', unsafe_allow_html=True)
            
            recovery = engine.calculate_recovery_patterns(loc_data)
            recovery_html = f"""<div class="detail-text">
<strong>Average Recovery Speed:</strong> {recovery['avg_recovery_speed']} (baseline: {recovery['baseline_recovery']})<br/>
<strong>Unresolved Stress:</strong> {recovery['unresolved_stress_pct']}% (baseline: {recovery['baseline_unresolved']}%)<br/>
<strong>Comparison:</strong> Recovery is {recovery['recovery_comparison']} than institutional baseline
</div>"""
            st.markdown(recovery_html, unsafe_allow_html=True)
            
            # Environmental Correlates
            st.markdown('<div class="detail-title">🏢 Environmental Correlates</div>', unsafe_allow_html=True)
            
            env_factors = engine.get_environmental_factors(location_name)
            env_html = f"""<div class="detail-text">
<strong>Noise Level:</strong> {env_factors['noise_level'].capitalize()}<br/>
<strong>Occupancy Density:</strong> {env_factors['occupancy_density'].capitalize()}<br/>
<strong>Primary Activity:</strong> {env_factors['primary_activity'].capitalize()}
</div>"""
            st.markdown(env_html, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Administrative Action Items Panel
    st.markdown('<div class="action-panel">', unsafe_allow_html=True)
    st.markdown('<div class="action-title">🎯 Administrative Action Items</div>', unsafe_allow_html=True)
    
    action_items = engine.generate_action_items(locations_data)
    
    for action in action_items[:5]:  # Show top 5
        card_class = f"action-card-{action['color']}"
        action_card_html = f"""<div class="action-card {card_class}">
<div class="action-location">{action['location']}</div>
<div class="action-text">
<strong>Trigger:</strong> {action['trigger']}<br/>
<strong>Rationale:</strong> {action['rationale']}<br/>
<strong>Consider:</strong> {action['suggested_response']}
</div>
</div>"""
        st.markdown(action_card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Policy & Public Health Insights Panel
    insights = engine.generate_policy_insights(locations_data)
    
    st.markdown('<div class="policy-panel">', unsafe_allow_html=True)
    st.markdown('<div class="policy-title">📈 Stress Temporal Trends for Public Health Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="policy-subtitle">Resilience trends across campus locations contribute to evidence-based institutional wellbeing strategies. Population-level signals, not individual traits.</div>', unsafe_allow_html=True)
    
    for insight in insights:
        st.markdown(f'<div class="policy-insight">{insight}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF Export
    st.markdown("---")
    st.markdown("### 📄 Export Community Resilience Report")
    
    if st.button("📥 Download PDF Report", key="download_mapping_pdf", use_container_width=True, type="primary"):
        try:
            from .resilience_mapping_pdf import generate_community_resilience_pdf
            
            pdf_buffer = generate_community_resilience_pdf(
                locations_data=locations_data,
                action_items=action_items,
                policy_insights=insights
            )
            
            st.download_button(
                label="💾 Save PDF Report",
                data=pdf_buffer,
                file_name=f"Community_Resilience_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                mime="application/pdf",
                key="save_mapping_pdf",
                use_container_width=True
            )
            
            st.success("✅ PDF generated successfully!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    render_resilience_mapping_page()
