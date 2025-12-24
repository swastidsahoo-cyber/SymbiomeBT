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
    
    # CSS Styles - ENHANCED to match screenshot exactly
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

/* Global Overrides */
.main { background: #0a0e27 !important; }
.stApp { background: #0a0e27 !important; font-family: 'Inter', sans-serif !important; }
[data-testid="stAppViewContainer"] { background: #0a0e27 !important; }

/* Header Styling */
.mapping-header {
    text-align: center;
    padding: 40px 20px 30px 20px;
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.05) 0%, rgba(139, 92, 246, 0.05) 100%);
    border-radius: 16px;
    margin-bottom: 30px;
    border: 1px solid rgba(6, 182, 212, 0.1);
}
.mapping-title {
    color: #06b6d4;
    font-size: 2.2rem;
    font-weight: 900;
    margin-bottom: 12px;
    letter-spacing: -0.5px;
    text-shadow: 0 0 20px rgba(6, 182, 212, 0.3);
}
.mapping-subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    line-height: 1.7;
    max-width: 900px;
    margin: 0 auto 25px auto;
    font-weight: 400;
}

/* Action Buttons */
.mapping-action-buttons {
    display: flex;
    gap: 12px;
    justify-content: center;
    margin: 25px 0 0 0;
    flex-wrap: wrap;
}
.mapping-action-btn {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(6, 182, 212, 0.05) 100%);
    border: 1.5px solid rgba(6, 182, 212, 0.4);
    color: #06b6d4;
    padding: 10px 20px;
    border-radius: 8px;
    font-size: 0.8rem;
    font-weight: 700;
    cursor: pointer;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.mapping-action-btn:hover {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.25) 0%, rgba(6, 182, 212, 0.15) 100%);
    border-color: rgba(6, 182, 212, 0.6);
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(6, 182, 212, 0.2);
}

/* Privacy Guard Panel */
.privacy-guard {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.08) 0%, rgba(16, 185, 129, 0.03) 100%);
    border: 1.5px solid rgba(16, 185, 129, 0.3);
    border-radius: 14px;
    padding: 24px 28px;
    margin: 25px 0;
    display: flex;
    align-items: center;
    gap: 24px;
    flex-wrap: wrap;
    box-shadow: 0 4px 16px rgba(16, 185, 129, 0.1);
}
.privacy-status {
    display: flex;
    align-items: center;
    gap: 10px;
}
.privacy-badge {
    background: linear-gradient(135deg, rgba(16, 185, 129, 0.25) 0%, rgba(16, 185, 129, 0.15) 100%);
    color: #10b981;
    padding: 6px 14px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    border: 1px solid rgba(16, 185, 129, 0.3);
}
.privacy-label {
    color: #64748b;
    font-size: 0.8rem;
    font-weight: 600;
    margin-right: 6px;
}
.privacy-value {
    color: #e2e8f0;
    font-size: 0.9rem;
    font-weight: 700;
}
.privacy-tooltip {
    margin-left: auto;
    color: #64748b;
    font-size: 0.75rem;
    font-style: italic;
    font-weight: 500;
}

/* Filter Panel */
.filter-panel {
    background: #1e293b;
    border: 1px solid rgba(148, 163, 184, 0.15);
    border-radius: 14px;
    padding: 24px;
    margin: 25px 0;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}

/* Heatmap Section */
.heatmap-section {
    margin: 30px 0;
}
.heatmap-header {
    color: #f1f5f9;
    font-size: 1.6rem;
    font-weight: 900;
    margin-bottom: 10px;
    letter-spacing: -0.3px;
}
.heatmap-subtitle {
    color: #94a3b8;
    font-size: 0.85rem;
    line-height: 1.6;
    margin-bottom: 25px;
    font-weight: 500;
}

/* Location Cards */
.location-card {
    background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
    border: 1.5px solid rgba(148, 163, 184, 0.15);
    border-radius: 14px;
    padding: 24px;
    margin: 18px 0;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3);
}
.location-card:hover {
    border-color: rgba(6, 182, 212, 0.4);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(6, 182, 212, 0.15);
}
.location-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}
.location-name {
    color: #f1f5f9;
    font-size: 1.2rem;
    font-weight: 800;
    letter-spacing: -0.2px;
}
.location-score {
    font-size: 3.5rem;
    font-weight: 900;
    line-height: 1;
    text-shadow: 0 0 20px currentColor;
}
.location-meta {
    color: #94a3b8;
    font-size: 0.8rem;
    margin-top: 6px;
    font-weight: 500;
}

/* Resilience Bar */
.resilience-bar {
    width: 100%;
    height: 14px;
    background: rgba(15, 23, 42, 0.8);
    border-radius: 8px;
    overflow: hidden;
    margin: 18px 0;
    box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.3);
}
.resilience-bar-fill {
    height: 100%;
    border-radius: 8px;
    transition: width 0.5s ease;
    box-shadow: 0 0 12px currentColor;
}
.resilience-bar-fill.red {
    background: linear-gradient(90deg, #ef4444 0%, #dc2626 100%);
}
.resilience-bar-fill.yellow {
    background: linear-gradient(90deg, #fbbf24 0%, #f59e0b 100%);
}
.resilience-bar-fill.green {
    background: linear-gradient(90deg, #10b981 0%, #059669 100%);
}

/* Location Details */
.location-details {
    background: rgba(15, 23, 42, 0.7);
    border-radius: 12px;
    padding: 24px;
    margin-top: 20px;
    border: 1px solid rgba(148, 163, 184, 0.1);
}
.detail-section {
    margin-bottom: 24px;
}
.detail-title {
    color: #06b6d4;
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 14px;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.detail-content {
    color: #cbd5e1;
    font-size: 0.85rem;
    line-height: 1.8;
    font-weight: 500;
}

/* Action Panel */
.action-panel {
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.08) 0%, rgba(168, 85, 247, 0.03) 100%);
    border: 1.5px solid rgba(139, 92, 246, 0.25);
    border-radius: 14px;
    padding: 28px;
    margin: 35px 0;
    box-shadow: 0 4px 16px rgba(139, 92, 246, 0.1);
}
.action-title {
    color: #a855f7;
    font-size: 1.4rem;
    font-weight: 900;
    margin-bottom: 24px;
    letter-spacing: -0.3px;
}
.action-card {
    background: rgba(15, 23, 42, 0.7);
    border-left: 4px solid;
    border-radius: 10px;
    padding: 20px;
    margin-bottom: 16px;
    transition: all 0.3s ease;
}
.action-card:hover {
    transform: translateX(4px);
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
}
.action-card.red {
    border-left-color: #ef4444;
    background: linear-gradient(90deg, rgba(239, 68, 68, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);
}
.action-card.yellow {
    border-left-color: #fbbf24;
    background: linear-gradient(90deg, rgba(251, 191, 36, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);
}
.action-card.green {
    border-left-color: #10b981;
    background: linear-gradient(90deg, rgba(16, 185, 129, 0.08) 0%, rgba(15, 23, 42, 0.7) 100%);
}
.action-card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 12px;
}
.action-location {
    color: #f1f5f9;
    font-size: 1rem;
    font-weight: 800;
}
.action-confidence {
    background: rgba(148, 163, 184, 0.15);
    color: #94a3b8;
    padding: 5px 12px;
    border-radius: 8px;
    font-size: 0.7rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}
.action-trigger {
    color: #94a3b8;
    font-size: 0.8rem;
    margin-bottom: 10px;
    font-weight: 500;
}
.action-rationale {
    color: #cbd5e1;
    font-size: 0.85rem;
    line-height: 1.7;
    margin-bottom: 12px;
    font-weight: 500;
}
.action-response {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.15) 0%, rgba(6, 182, 212, 0.05) 100%);
    color: #06b6d4;
    padding: 8px 14px;
    border-radius: 8px;
    font-size: 0.75rem;
    font-weight: 700;
    display: inline-block;
    border: 1px solid rgba(6, 182, 212, 0.3);
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

/* Policy Panel */
.policy-panel {
    background: linear-gradient(135deg, rgba(6, 182, 212, 0.08) 0%, rgba(6, 182, 212, 0.03) 100%);
    border: 1.5px solid rgba(6, 182, 212, 0.25);
    border-radius: 14px;
    padding: 28px;
    margin: 35px 0;
    box-shadow: 0 4px 16px rgba(6, 182, 212, 0.1);
}
.policy-title {
    color: #06b6d4;
    font-size: 1.4rem;
    font-weight: 900;
    margin-bottom: 14px;
    letter-spacing: -0.3px;
}
.policy-subtitle {
    color: #94a3b8;
    font-size: 0.8rem;
    line-height: 1.7;
    margin-bottom: 24px;
    font-weight: 500;
}
.policy-insight {
    color: #e2e8f0;
    font-size: 0.9rem;
    line-height: 1.8;
    margin-bottom: 18px;
    padding: 18px;
    background: rgba(15, 23, 42, 0.5);
    border-radius: 10px;
    border-left: 3px solid rgba(6, 182, 212, 0.5);
    font-weight: 500;
}
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Header
    header_html = """<div class="mapping-header">
<div class="mapping-title">🗺️ Community Resilience Mapping</div>
<div class="mapping-subtitle">Environment-driven insights for institutional wellbeing. Aggregated, anonymised resilience signals across physical environments aid decision-making, risk mitigation, and preventive wellbeing strategies.</div>
<div class="mapping-action-buttons">
<div class="mapping-action-btn">View Dashboard</div>
<div class="mapping-action-btn">Administrative Actions</div>
<div class="mapping-action-btn">Policy Insights</div>
</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    
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
<div class="privacy-tooltip">
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
    st.markdown('<div class="heatmap-section">', unsafe_allow_html=True)
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
        
        # Color for score
        score_color = '#ef4444' if color_band == 'red' else '#fbbf24' if color_band == 'yellow' else '#10b981'
        
        # Location card
        is_expanded = location_name in st.session_state.expanded_locations
        
        card_html = f"""<div class="location-card">
<div class="location-header">
<div>
<div class="location-name">{location_name} {trend_arrow}</div>
<div class="location-meta">{participant_count} students - Avg RQ: {score}</div>
</div>
<div class="location-score" style="color: {score_color};">{score}</div>
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
                height=220,
                margin=dict(l=0, r=0, t=10, b=0),
                xaxis=dict(showgrid=False, color='#64748b', title='Hour', titlefont=dict(size=11)),
                yaxis=dict(showgrid=True, gridcolor='rgba(148,163,184,0.1)', color='#64748b', title='Stress Intensity', titlefont=dict(size=11)),
                font=dict(family='Inter', color='#cbd5e1', size=10)
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
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Administrative Action Items Panel
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
    insights = engine.generate_policy_insights(locations_data)
    
    st.markdown('<div class="policy-panel">', unsafe_allow_html=True)
    st.markdown('<div class="policy-title">📈 Stress Temporal Trends for Public Health Policy</div>', unsafe_allow_html=True)
    st.markdown('<div class="policy-subtitle">Resilience trends across campus locations contribute to evidence-based institutional wellbeing strategies. Population-level signals, not individual traits.</div>', unsafe_allow_html=True)
    
    for insight in insights:
        st.markdown(f'<div class="policy-insight">{insight}</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # PDF Export Button
    st.markdown('<br>', unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 📄 Export Community Resilience Report")
    
    export_col1, export_col2 = st.columns(2)
    
    with export_col1:
        st.markdown("""
        **Generate Comprehensive Institutional Report**
        
        Export your complete Community Resilience Mapping analysis including:
        - Executive Summary with key findings
        - Spatial analysis and location heatmaps
        - Temporal analysis and peak stress patterns
        - Environmental correlations
        - Non-prescriptive recommendations
        - Ethics & limitations
        """)
    
    with export_col2:
        if st.button("📥 Download Community Resilience Report", key="download_mapping_pdf", use_container_width=True, type="primary"):
            try:
                from .resilience_mapping_pdf import generate_community_resilience_pdf
                
                # Generate PDF
                pdf_buffer = generate_community_resilience_pdf(
                    locations_data=locations_data,
                    action_items=action_items,
                    policy_insights=insights
                )
                
                # Offer download
                st.download_button(
                    label="💾 Save PDF Report",
                    data=pdf_buffer,
                    file_name=f"Community_Resilience_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                    mime="application/pdf",
                    key="save_mapping_pdf",
                    use_container_width=True
                )
                
                st.success("✅ Community Resilience Report generated successfully!")
                
            except Exception as e:
                st.error(f"❌ Error generating PDF: {str(e)}")
                st.info("Please ensure all required dependencies are installed.")

if __name__ == "__main__":
    render_resilience_mapping_page()
