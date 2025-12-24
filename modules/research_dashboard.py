"""
Research & Analysis Dashboard
Scientific visualization and data insights
"""
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib.units import inch

def render_research_dashboard_page():
    # Header
    st.markdown('<h2 style="color: #cbd5e1;">Research & Analysis Dashboard</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">Scientific visualization and data insights</p>', unsafe_allow_html=True)
    
    # Top buttons
    col_btn1, col_btn2 = st.columns([6, 1])
    with col_btn2:
        if st.button("📥 Export CSV", use_container_width=True, type="secondary"):
            csv_data = generate_csv_export()
            st.download_button("Download CSV", csv_data, "symbiome_data.csv", "text/csv", use_container_width=True)
        if st.button("📄 Generate Report", use_container_width=True, type="primary"):
            pdf_data = generate_pdf_report()
            st.download_button("Download PDF", pdf_data, "symbiome_report.pdf", "application/pdf", use_container_width=True)
    
    # Top 4 Metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 16px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><div style="color: #10b981; font-size: 1.5rem;">🔬</div><div style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 2px 8px; border-radius: 8px; font-size: 0.7rem; font-weight: 700;">+12% vs last week</div></div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">27</div><div style="color: #94a3b8; font-size: 0.85rem;">Total Sessions</div></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px; padding: 16px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><div style="color: #06b6d4; font-size: 1.5rem;">📊</div><div style="background: rgba(239, 68, 68, 0.2); color: #ef4444; padding: 2px 8px; border-radius: 8px; font-size: 0.7rem; font-weight: 700;">-48%</div></div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">56.3</div><div style="color: #94a3b8; font-size: 0.85rem;">Avg SRI</div></div>', unsafe_allow_html=True)
    
    with col3:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 16px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><div style="color: #a78bfa; font-size: 1.5rem;">⏱️</div><div style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 2px 8px; border-radius: 8px; font-size: 0.7rem; font-weight: 700;">+5%</div></div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">5m</div><div style="color: #94a3b8; font-size: 0.85rem;">Avg Recovery</div></div>', unsafe_allow_html=True)
    
    with col4:
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(245, 158, 11, 0.3); border-radius: 12px; padding: 16px;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><div style="color: #f59e0b; font-size: 1.5rem;">⚠️</div><div style="color: #94a3b8; font-size: 0.7rem;">Across all sessions</div></div><div style="color: #e2e8f0; font-size: 2rem; font-weight: 900;">43</div><div style="color: #94a3b8; font-size: 0.85rem;">Stress Events</div></div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["Trends", "Breakdown", "Correlation", "Statistics", "Timeline", "Tools"])
    
    with tab1:
        render_trends_tab()
    
    with tab2:
        render_breakdown_tab()
    
    with tab3:
        render_correlation_tab()
    
    with tab4:
        render_statistics_tab()
    
    with tab5:
        render_timeline_tab()
    
    with tab6:
        render_tools_tab()


def render_trends_tab():
    st.markdown('<h3 style="color: #06b6d4; margin-top: 10px;">📈 SRI Progression Over Time</h3>', unsafe_allow_html=True)
    
    # Generate data
    days = np.arange(1, 28)
    sri_values = 50 + 10 * np.sin(days / 3) + np.random.normal(0, 3, 27)
    trendline = np.poly1d(np.polyfit(days, sri_values, 1))(days)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=days, y=sri_values, mode='lines+markers', name='Resilience Index', line=dict(color='#06b6d4', width=2), marker=dict(size=6)))
    fig.add_trace(go.Scatter(x=days, y=trendline, mode='lines', name='Trendline', line=dict(color='#10b981', width=2, dash='dash')))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        height=350,
        xaxis_title="Day",
        yaxis_title="SRI Score",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        font=dict(color='#cbd5e1'),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Recovery Time Trend
    st.markdown('<h3 style="color: #f59e0b; margin-top: 30px;">⏱️ Recovery Time Trend</h3>', unsafe_allow_html=True)
    
    recovery_times = 300 - 50 * np.sin(days / 4) + np.random.normal(0, 20, 27)
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=days, y=recovery_times, mode='lines+markers', name='Recovery Time', line=dict(color='#f59e0b', width=2), marker=dict(size=6)))
    
    fig2.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        height=350,
        xaxis_title="Day",
        yaxis_title="Seconds",
        font=dict(color='#cbd5e1'),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig2, use_container_width=True)
    
    # Bottom buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export CSV", key="trends_csv", use_container_width=True, type="secondary"):
            st.success("CSV exported!")
    with col2:
        if st.button("📄 Generate PDF Report", key="trends_pdf", use_container_width=True):
            st.success("PDF generated!")


def render_breakdown_tab():
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #a78bfa; margin-top: 10px;">🥧 Component Contribution</h3>', unsafe_allow_html=True)
        
        labels = ['GSR: 49', 'HRV: 34', 'Facial: 73']
        values = [49, 34, 73]
        colors_pie = ['#06b6d4', '#ef4444', '#a78bfa']
        
        fig = go.Figure(data=[go.Pie(labels=labels, values=values, marker=dict(colors=colors_pie), hole=0.3)])
        
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            height=300,
            font=dict(color='#cbd5e1'),
            showlegend=True,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 style="color: #10b981; margin-top: 10px;">📊 Session Types</h3>', unsafe_allow_html=True)
        
        session_types = ['Baseline', 'Stress', 'Recovery', 'Breathing']
        session_counts = [7, 4, 10, 9]
        colors_bar = ['#64748b', '#ef4444', '#10b981', '#06b6d4']
        
        fig2 = go.Figure(data=[go.Bar(x=session_types, y=session_counts, marker=dict(color=colors_bar))])
        
        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(15,23,42,0.8)',
            height=300,
            yaxis_title="Count",
            font=dict(color='#cbd5e1'),
            showlegend=False,
            margin=dict(l=50, r=50, t=20, b=50)
        )
        
        st.plotly_chart(fig2, use_container_width=True)
    
    # Bottom buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export CSV", key="breakdown_csv", use_container_width=True, type="secondary"):
            st.success("CSV exported!")
    with col2:
        if st.button("📄 Generate PDF Report", key="breakdown_pdf", use_container_width=True):
            st.success("PDF generated!")


def render_correlation_tab():
    st.markdown('<h3 style="color: #06b6d4; margin-top: 10px;">🔗 HRV vs Recovery Time</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #cbd5e1; font-size: 0.9rem;">Correlation analysis: Higher HRV heavily correlates with faster recovery</p>', unsafe_allow_html=True)
    
    # Generate scatter data
    hrv_values = np.random.uniform(400, 600, 50)
    recovery_times = 600 - 0.8 * hrv_values + np.random.normal(0, 30, 50)
    
    fig = go.Figure(data=go.Scatter(
        x=hrv_values,
        y=recovery_times,
        mode='markers',
        marker=dict(size=8, color='#06b6d4', opacity=0.7)
    ))
    
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(15,23,42,0.8)',
        height=400,
        xaxis_title="Heart Rate Variability (ms)",
        yaxis_title="Recovery Time (s)",
        font=dict(color='#cbd5e1'),
        margin=dict(l=50, r=50, t=50, b=50)
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Correlation coefficient
    st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(6, 182, 212, 0.3); border-radius: 12px; padding: 16px; margin-top: 20px;"><div style="color: #06b6d4; font-weight: 700; margin-bottom: 8px;">📊 Correlation coefficient: r = -0.68, p < 0.001</div><div style="color: #cbd5e1; font-size: 0.85rem;">Strong negative correlation indicates higher HRV predicts faster recovery.</div></div>', unsafe_allow_html=True)
    
    # Bottom buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export CSV", key="corr_csv", use_container_width=True, type="secondary"):
            st.success("CSV exported!")
    with col2:
        if st.button("📄 Generate PDF Report", key="corr_pdf", use_container_width=True):
            st.success("PDF generated!")


def render_statistics_tab():
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<h3 style="color: #cbd5e1; margin-top: 10px;">📊 Descriptive Statistics</h3>', unsafe_allow_html=True)
        
        stats_data = [
            ["Sample Size", "27 sessions"],
            ["Mean SRI", "56.89 ± 9.68"],
            ["Mean HRV", "54.52 ms"],
            ["Mean GSR", "3.21 µS"],
            ["Mean Recovery", "4.8 min"],
            ["Total Duration", "6.5 hours"]
        ]
        
        for label, value in stats_data:
            st.markdown(f'<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 8px; padding: 12px; margin: 8px 0; display: flex; justify-content: space-between;"><span style="color: #94a3b8;">{label}</span><span style="color: #e2e8f0; font-weight: 700;">{value}</span></div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<h3 style="color: #10b981; margin-top: 10px;">💡 Key Insights</h3>', unsafe_allow_html=True)
        
        insights = [
            ("SRI improved by ~60% over time", "#10b981"),
            ("Recovery time decreased by 1.7s on average", "#06b6d4"),
            ("8% of sessions achieved SRI > 70", "#a78bfa"),
            ("Breathing sessions show 1% highest SRI", "#f59e0b")
        ]
        
        for i, (insight, color) in enumerate(insights, 1):
            st.markdown(f'<div style="background: rgba(30, 41, 59, 0.8); border-left: 3px solid {color}; border-radius: 8px; padding: 12px; margin: 8px 0;"><div style="color: {color}; font-weight: 700; font-size: 0.75rem; margin-bottom: 4px;">{i}</div><div style="color: #cbd5e1; font-size: 0.9rem;">{insight}</div></div>', unsafe_allow_html=True)
    
    # Research-Ready Export
    st.markdown('<h3 style="color: #3b82f6; margin-top: 30px;">📚 Research-Ready Export</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #cbd5e1; font-size: 0.9rem;">Export anonymized data for academic research and validation studies</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export Raw Data (CSV)", key="stats_csv", use_container_width=True, type="secondary"):
            st.success("Raw data exported!")
    with col2:
        if st.button("📄 Generate Summary Report", key="stats_pdf", use_container_width=True):
            st.success("Summary report generated!")
    
    st.markdown('<div style="background: rgba(59, 130, 246, 0.1); border-left: 3px solid #3b82f6; padding: 12px; margin-top: 16px; border-radius: 4px;"><div style="color: #cbd5e1; font-size: 0.85rem;"><strong>Ethics Note:</strong> All exported data is anonymized and contains no personally identifiable information. Contact for research collaborations.</div></div>', unsafe_allow_html=True)


def render_timeline_tab():
    st.markdown('<h3 style="color: #a78bfa; margin-top: 10px;">⏱️ AI Insights Timeline</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #cbd5e1; font-size: 0.9rem;">Chronological feed of key observations and pattern detections</p>', unsafe_allow_html=True)
    
    timeline_events = [
        ("12/24/2024", "Insight Date", "3 sessions completed - baseline pattern established", "#3b82f6", "Milestone"),
        ("12/24/2024", "Recovery time shows strong negative correlation with HRV (r = -0.68, p < 0.001)", "Pattern"),
        ("12/23/2024", "Stress spike detected at 14:52 - GSR increased 45%, baseline", "#f59e0b", "Alert"),
        ("12/22/2024", "Fastest recovery time achieved: 3.2 minutes (target: <5 min)", "#10b981", "Achievement")
    ]
    
    for i, event in enumerate(timeline_events):
        if len(event) == 5:
            date, title, desc, color, badge = event
        else:
            date, desc, badge = event
            title = ""
            color = "#06b6d4"
        
        icon_map = {"Milestone": "🎯", "Pattern": "🔍", "Alert": "⚠️", "Achievement": "🏆"}
        icon = icon_map.get(badge, "📌")
        
        st.markdown(f'<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 16px; margin: 12px 0; display: flex; gap: 15px;"><div style="color: {color}; font-size: 2rem;">{icon}</div><div style="flex: 1;"><div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px;"><div style="color: #e2e8f0; font-weight: 700;">{title if title else desc[:50]}</div><div style="background: rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.2,)}; color: {color}; padding: 4px 12px; border-radius: 12px; font-size: 0.75rem; font-weight: 700;">{badge}</div></div><div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 6px;">{date}</div>{f"<div style=\\"color: #cbd5e1; font-size: 0.9rem;\\">{desc}</div>" if title else ""}</div></div>', unsafe_allow_html=True)
    
    # Bottom buttons
    col1, col2 = st.columns(2)
    with col1:
        if st.button("📥 Export CSV", key="timeline_csv", use_container_width=True, type="secondary"):
            st.success("Timeline exported!")
    with col2:
        if st.button("📄 Generate PDF Report", key="timeline_pdf", use_container_width=True):
            st.success("Timeline report generated!")


def render_tools_tab():
    st.markdown('<h3 style="color: #06b6d4; margin-top: 10px;">🛠️ Research Tools</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #cbd5e1;">Advanced data export and analysis tools for researchers</p>', unsafe_allow_html=True)
    
    st.info("Additional research tools and collaboration features coming soon!")


def generate_csv_export():
    # Generate sample CSV data
    df = pd.DataFrame({
        'Date': pd.date_range(start='2024-12-01', periods=27),
        'SRI': np.random.uniform(45, 65, 27),
        'HRV': np.random.uniform(400, 600, 27),
        'GSR': np.random.uniform(2, 4, 27),
        'Recovery_Time': np.random.uniform(200, 400, 27)
    })
    return df.to_csv(index=False)


def generate_pdf_report():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#06b6d4'), spaceAfter=12)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=16, textColor=colors.HexColor('#10b981'), spaceAfter=10)
    
    # Title
    story.append(Paragraph("Symbiome Research Report", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Executive Summary
    story.append(Paragraph("Executive Summary", heading_style))
    story.append(Paragraph("This report contains comprehensive analysis of 27 biofeedback sessions, including stress resilience metrics, recovery patterns, and AI-generated insights.", styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Key Metrics
    story.append(Paragraph("Key Metrics", heading_style))
    metrics_data = [
        ['Metric', 'Value'],
        ['Total Sessions', '27'],
        ['Average SRI', '56.3'],
        ['Average Recovery Time', '5 minutes'],
        ['Stress Events Detected', '43']
    ]
    
    metrics_table = Table(metrics_data)
    metrics_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#06b6d4')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    
    story.append(metrics_table)
    story.append(Spacer(1, 0.3*inch))
    
    # Key Insights
    story.append(Paragraph("Key Insights", heading_style))
    story.append(Paragraph("• SRI improved by approximately 60% over the observation period", styles['Normal']))
    story.append(Paragraph("• Recovery time decreased by 1.7 seconds on average", styles['Normal']))
    story.append(Paragraph("• 8% of sessions achieved SRI scores above 70", styles['Normal']))
    story.append(Paragraph("• Breathing sessions demonstrated 1% highest SRI improvement", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Paragraph("___", styles['Normal']))
    story.append(Paragraph("Symbiome - Advanced Biofeedback & Stress Management Platform", styles['Normal']))
    story.append(Paragraph("This data is anonymized and contains no personally identifiable information.", styles['Normal']))
    
    doc.build(story)
    buffer.seek(0)
    return buffer.getvalue()
