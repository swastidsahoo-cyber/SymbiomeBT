"""
Community Resilience Mapping Dashboard
Population-level environmental stress analytics.
PIXEL-PERFECT UI matching specification.
Privacy-first, non-surveillance framing.
"""
import streamlit as st
import plotly.graph_objects as go
import numpy as np
from datetime import datetime
from .resilience_mapping_engine import ResilienceMappingEngine

def render_resilience_mapping_page():
    # Initialize engine
    engine = ResilienceMappingEngine(min_n=10)
    
    # Initialize session state
    if 'mapping_time_window' not in st.session_state:
        st.session_state.mapping_time_window = 'week'
    
    if 'expanded_locations' not in st.session_state:
        st.session_state.expanded_locations = set()
    
    # CSS Styles - Pixel-perfect match to screenshot
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; background: #0a0e27; }
.mapping-header { text-align: center; padding: 30px 0 20px 0; }
.mapping-title { color: #06b6d4; font-size: 1.8rem; font-weight: 800; margin-bottom: 8px; }
.mapping-subtitle { color: #94a3b8; font-size: 0.85rem; line-height: 1.6; max-width: 900px; margin: 0 auto 20px auto; }
.mapping-action-buttons { display: flex; gap: 10px; justify-content: center; margin: 20px 0; }
.mapping-action-btn { background: rgba(6, 182, 212, 0.1); border: 1px solid rgba(6, 182, 212, 0.3); color: #06b6d4; padding: 8px 16px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.privacy-guard { background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; margin: 20px 0; display: flex; align-items: center; gap: 20px; }
.privacy-status { display: flex; align-items: center; gap: 8px; }
.privacy-badge { background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 4px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; }
.privacy-label { color: #94a3b8; font-size: 0.75rem; margin-right: 8px; }
.privacy-value { color: white; font-size: 0.85rem; font-weight: 700; }
.filter-panel { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 20px 0; }
.heatmap-header { color: white; font-size: 1.3rem; font-weight: 800; margin-bottom: 8px; }
.heatmap-subtitle { color: #94a3b8; font-size: 0.75rem; line-height: 1.5; margin-bottom: 20px; }
.location-card { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 20px; margin: 15px 0; cursor: pointer; transition: all 0.3s; }
.location-card:hover { border-color: rgba(6, 182, 212, 0.3); }
.location-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px; }
.location-name { color: white; font-size: 1.1rem; font-weight: 700; }
.location-score { color: white; font-size: 3rem; font-weight: 900; line-height: 1; }
.location-meta { color: #94a3b8; font-size: 0.75rem; margin-top: 5px; }
.resilience-bar { width: 100%; height: 12px; background: rgba(255, 255, 255, 0.05); border-radius: 6px; overflow: hidden; margin: 15px 0; }
.resilience-bar-fill { height: 100%; border-radius: 6px; }
.resilience-bar-fill.red { background: #ef4444; }
.resilience-bar-fill.yellow { background: #fbbf24; }
.resilience-bar-fill.green { background: #10b981; }
.location-details { background: rgba(15, 23, 42, 0.6); border-radius: 8px; padding: 20px; margin-top: 15px; }
.detail-section { margin-bottom: 20px; }
.detail-title { color: #06b6d4; font-size: 0.9rem; font-weight: 700; margin-bottom: 10px; }
.detail-content { color: #94a3b8; font-size: 0.8rem; line-height: 1.6; }
.action-panel { background: linear-gradient(135deg, rgba(139, 92, 246, 0.05) 0%, rgba(168, 85, 247, 0.05) 100%); border: 1px solid rgba(139, 92, 246, 0.2); border-radius: 12px; padding: 24px; margin: 30px 0; }
.action-title { color: #a855f7; font-size: 1.2rem; font-weight: 800; margin-bottom: 20px; }
.action-card { background: rgba(15, 23, 42, 0.6); border-left: 4px solid; border-radius: 8px; padding: 16px; margin-bottom: 15px; }
.action-card.red { border-left-color: #ef4444; }
.action-card.yellow { border-left-color: #fbbf24; }
.action-card.green { border-left-color: #10b981; }
.action-card-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 10px; }
.action-location { color: white; font-size: 0.95rem; font-weight: 700; }
.action-confidence { background: rgba(255, 255, 255, 0.1); color: #94a3b8; padding: 4px 10px; border-radius: 6px; font-size: 0.7rem; font-weight: 700; }
.action-trigger { color: #94a3b8; font-size: 0.75rem; margin-bottom: 8px; }
.action-rationale { color: #cbd5e1; font-size: 0.8rem; line-height: 1.5; margin-bottom: 8px; }
.action-response { background: rgba(6, 182, 212, 0.1); color: #06b6d4; padding: 6px 12px; border-radius: 6px; font-size: 0.75rem; font-weight: 700; display: inline-block; }
.policy-panel { background: rgba(6, 182, 212, 0.05); border: 1px solid rgba(6, 182, 212, 0.2); border-radius: 12px; padding: 24px; margin: 30px 0; }
.policy-title { color: #06b6d4; font-size: 1.2rem; font-weight: 800; margin-bottom: 12px; }
.policy-subtitle { color: #94a3b8; font-size: 0.75rem; line-height: 1.6; margin-bottom: 20px; }
.policy-insight { color: #cbd5e1; font-size: 0.85rem; line-height: 1.7; margin-bottom: 15px; padding: 15px; background: rgba(15, 23, 42, 0.4); border-radius: 8px; }
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Header
    header_html = """<div class="mapping-header">
<div class="mapping-title">🗺️ Community Resilience Mapping</div>
<div class="mapping-subtitle">Environment-driven insights for institutional wellbeing. Aggregated, anonymised resilience signals across physical environments aid decision-making, risk mitigation, and preventive wellbeing strategies.</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Action Buttons
    action_html = """<div class="mapping-action-buttons">
<div class="mapping-action-btn">View Dashboard</div>
<div class="mapping-action-btn">Administrative Actions</div>
<div class="mapping-action-btn">Policy Insights</div>
</div>"""
    st.markdown(action_html, unsafe_allow_html=True)
    
    # Privacy Guard Status Panel
    privacy_html = """<div class="privacy-guard">
<div class="privacy-status">
<span class="privacy-label">Privacy Status:</span>
<span class="privacy-badge">Protected</span>
</div>
<div class="privacy-status">
<span class="privacy-label">Aggregation:</span>
<span class="privacy-value">K-anonymised</span>
</div>
<div class="privacy-status">
<span class="privacy-label">Granularity:</span>
<span class="privacy-value">Zone-level only</span>
</div>
<div style="margin-left: auto; color: #64748b; font-size: 0.7rem; font-style: italic;">
ⓘ No individual-level data is displayed or stored on this screen
</div>
</div>"""
    st.markdown(privacy_html, unsafe_allow_html=True)
    
    # Global Filter Controls
    st.markdown('<div class="filter-panel">', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([2, 2, 2, 3, 1])
    
    with col1:
        institution = st.selectbox("Institution", ["Trinity College Dublin"], key="institution_filter")
    
    with col2:
        city_zone = st.selectbox("City/Zone", ["Dublin City Centre"], key="zone_filter")
    
    with col3:
        resilience_filter = st.selectbox("Resilience Score", ["All Scores", "High Strain (0-49)", "Moderate (50-74)", "Adaptive (75-100)"], key="resilience_filter")
    
    with col4:
        col_day, col_week, col_month = st.columns(3)
        with col_day:
            if st.button("Day", key="filter_day", use_container_width=True, type="primary" if st.session_state.mapping_time_window == 'day' else "secondary"):
                st.session_state.mapping_time_window = 'day'
                st.rerun()
        with col_week:
            if st.button("Week", key="filter_week", use_container_width=True, type="primary" if st.session_state.mapping_time_window == 'week' else "secondary"):
                st.session_state.mapping_time_window = 'week'
                st.rerun()
        with col_month:
            if st.button("Month", key="filter_month", use_container_width=True, type="primary" if st.session_state.mapping_time_window == 'month' else "secondary"):
                st.session_state.mapping_time_window = 'month'
                st.rerun()
    
    with col5:
        if st.button("🔄", key="refresh_data", use_container_width=True):
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Get location data
    locations_data = engine.get_all_locations_data(st.session_state.mapping_time_window)
    
    # School Stress Heatmap
    st.markdown('<br>', unsafe_allow_html=True)
    heatmap_header_html = """<div class="heatmap-header">School Stress Heatmap (This week)</div>
<div class="heatmap-subtitle">Aggregated resilience signals across locations (Only locations based on student data shown on campus environment)</div>"""
    st.markdown(heatmap_header_html, unsafe_allow_html=True)
    
    # Location Cards
    for loc_data in locations_data:
        location_name = loc_data['location']
        score = loc_data['composite_resilience']
        color_band = loc_data['color_band']
        participant_count = loc_data['participant_count']
        trend = loc_data['trend']
        
        # Trend arrow
        trend_arrow = "↗" if trend == "improving" else "↘" if trend == "declining" else "→"
        
        # Location card
        is_expanded = location_name in st.session_state.expanded_locations
        
        card_html = f"""<div class="location-card">
<div class="location-header">
<div>
<div class="location-name">{location_name} {trend_arrow}</div>
<div class="location-meta">{participant_count} students - Avg RQ: {score}</div>
</div>
<div class="location-score" style="color: {'#ef4444' if color_band == 'red' else '#fbbf24' if color_band == 'yellow' else '#10b981'};">{score}</div>
</div>
<div class="resilience-bar">
<div class="resilience-bar-fill {color_band}" style="width: {score}%;"></div>
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
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
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
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                height=200,
                margin=dict(l=0, r=0, t=0, b=0),
                xaxis=dict(showgrid=False, color='#64748b', title='Hour'),
                yaxis=dict(showgrid=True, gridcolor='rgba(255,255,255,0.05)', color='#64748b', title='Stress Intensity'),
                font=dict(family='Inter', color='white', size=9)
            )
            
            st.plotly_chart(fig_peak, use_container_width=True, key=f"peak_{location_name}")
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Recovery Patterns
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="detail-title">🔄 Recovery Patterns</div>', unsafe_allow_html=True)
            
            recovery = engine.calculate_recovery_patterns(loc_data)
            recovery_html = f"""<div class="detail-content">
<strong>Average Recovery Speed:</strong> {recovery['avg_recovery_speed']} (baseline: {recovery['baseline_recovery']})<br/>
<strong>Unresolved Stress:</strong> {recovery['unresolved_stress_pct']}% (baseline: {recovery['baseline_unresolved']}%)<br/>
<strong>Comparison:</strong> Recovery is {recovery['recovery_comparison']} than institutional baseline
</div>"""
            st.markdown(recovery_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            # Environmental Correlates
            st.markdown('<div class="detail-section">', unsafe_allow_html=True)
            st.markdown('<div class="detail-title">🏢 Environmental Correlates</div>', unsafe_allow_html=True)
            
            env_factors = engine.get_environmental_factors(location_name)
            env_html = f"""<div class="detail-content">
<strong>Noise Level:</strong> {env_factors['noise_level'].capitalize()}<br/>
<strong>Occupancy Density:</strong> {env_factors['occupancy_density'].capitalize()}<br/>
<strong>Primary Activity:</strong> {env_factors['primary_activity'].capitalize()}
</div>"""
            st.markdown(env_html, unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Administrative Action Items Panel
    st.markdown('<br><br>', unsafe_allow_html=True)
    st.markdown('<div class="action-panel">', unsafe_allow_html=True)
    st.markdown('<div class="action-title">🎯 Administrative Action Items</div>', unsafe_allow_html=True)
    
    action_items = engine.generate_action_items(locations_data)
    
    for action in action_items[:5]:  # Show top 5
        action_card_html = f"""<div class="action-card {action['color']}">
<div class="action-card-header">
<div class="action-location">{action['location']}</div>
<div class="action-confidence">Confidence: {action['confidence']}</div>
</div>
<div class="action-trigger">Trigger: {action['trigger']}</div>
<div class="action-rationale">{action['rationale']}</div>
<div class="action-response">{action['suggested_response']}</div>
</div>"""
        st.markdown(action_card_html, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Policy & Public Health Insights Panel
    st.markdown('<div class="policy-panel">', unsafe_allow_html=True)
    st.markdown('<div class="policy-title">📈 Stress Temporal Trends for Public Health Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="policy-subtitle">Resilience trends across campus locations contribute to evidence-based institutional wellbeing strategies. Population-level signals, not individual traits.</div>', unsafe_allow_html=True)
    
    insights = engine.generate_policy_insights(locations_data)
    
    for insight in insights:
        st.markdown(f'<div class="policy-insight">{insight}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF Export Button
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📄 Export Community Resilience Report")
    
    if st.button("📥 Download Community Resilience Report", key="download_mapping_pdf", use_container_width=True, type="primary"):
        st.info("📋 PDF export functionality will generate a comprehensive institutional report with all sections: Executive Summary, Spatial Analysis, Temporal Analysis, Environmental Correlations, Recommendations, and Ethics & Limitations.")

if __name__ == "__main__":
    render_resilience_mapping_page()
