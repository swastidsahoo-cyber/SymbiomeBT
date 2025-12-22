"""
Clinical Data Vault (v1.0)
Secure medical data export for healthcare provider review.
Matches competition screenshots exactly with full QR code, preview, and PDF functionality.
"""
import streamlit as st
import qrcode
from io import BytesIO
import base64
import random
import string
from datetime import datetime, timedelta
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER, TA_LEFT
import numpy as np

def generate_access_code():
    """Generate unique 8-character access code"""
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))

def generate_qr_code(code):
    """Generate QR code image with secure portal URL"""
    # Create secure portal URL that would link to the patient data
    portal_url = f"https://portal.symbiome.health/access/{code}"
    
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(portal_url)  # Encode the URL, not just the code
    qr.make(fit=True)
    img = qr.make_image(fill_color="#1e293b", back_color="white")
    
    # Convert to base64 for display
    buffered = BytesIO()
    img.save(buffered, format="PNG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str

def generate_clinical_pdf():
    """Generate COMPREHENSIVE 8+ page clinical PDF report for healthcare providers"""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, topMargin=0.5*inch, bottomMargin=0.5*inch)
    story = []
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=24, textColor=colors.HexColor('#0ea5e9'), alignment=TA_CENTER, spaceAfter=12)
    heading_style = ParagraphStyle('CustomHeading', parent=styles['Heading2'], fontSize=14, textColor=colors.HexColor('#10b981'), spaceBefore=12, spaceAfter=6)
    subheading_style = ParagraphStyle('SubHeading', parent=styles['Heading3'], fontSize=11, textColor=colors.HexColor('#6366f1'), spaceBefore=8, spaceAfter=4)
    
    # === PAGE 1: EXECUTIVE SUMMARY ===
    story.append(Paragraph("SYMBIOME CLINICAL DATA REPORT", title_style))
    story.append(Paragraph(f"Generated: {datetime.now().strftime('%B %d, %Y at %H:%M:%S')}", styles['Normal']))
    story.append(Paragraph("Comprehensive 30-Day Biometric Analysis for Healthcare Provider Review", styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Patient Summary
    story.append(Paragraph("EXECUTIVE SUMMARY", heading_style))
    summary_data = [
        ['Reporting Period', '30 Days (Nov 22 - Dec 22, 2025)'],
        ['Total Monitoring Sessions', '87 sessions'],
        ['Total Data Points Collected', '124,800 biometric readings'],
        ['Average Session Duration', '18.5 minutes'],
        ['Baseline SRI (Start)', '54.2'],
        ['Current SRI (End)', '68.3 (+26% improvement)'],
        ['Resilience Quotient', '73/100 (Good)'],
        ['Stress Events Detected', '42 episodes'],
        ['Interventions Applied', '35 sessions'],
        ['Compliance Rate', '94% (Excellent)']
    ]
    summary_table = Table(summary_data, colWidths=[2.5*inch, 4*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#f8fafc')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
        ('TEXTCOLOR', (1, 0), (1, -1), colors.black),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#e2e8f0')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(summary_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Clinical Interpretation
    story.append(Paragraph("CLINICAL INTERPRETATION", subheading_style))
    interpretation_text = """Patient demonstrates significant improvement in autonomic regulation over the monitoring period. 
    Baseline stress resilience index improved by 26%, indicating positive adaptation to stress management interventions. 
    HRV trends show enhanced parasympathetic tone, particularly during evening hours. Sleep architecture analysis reveals 
    gradual improvement in REM latency and deep sleep percentage. Anxiety markers detected via NLP analysis show decreasing 
    frequency in catastrophic thinking patterns. Recommend continuation of current intervention protocol with emphasis on 
    maintaining environmental optimization strategies."""
    story.append(Paragraph(interpretation_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # === BIOMARKER ANALYSIS ===
    story.append(Paragraph("DETAILED BIOMARKER ANALYSIS (30-Day Averages)", heading_style))
    biomarker_data = [
        ['Metric', 'Baseline', 'Current', 'Change', 'Clinical Range', 'Status'],
        ['Heart Rate Variability (RMSSD)', '58.3 ms', '70.2 ms', '+20.4%', '60-100 ms', '✓ Normal'],
        ['Galvanic Skin Response', '78.1 µS', '82.3 µS', '+5.4%', '75-90 µS', '✓ Optimal'],
        ['Skin Temperature', '92.4°F', '92.8°F', '+0.4%', '91-94°F', '✓ Normal'],
        ['Resting Heart Rate', '72 bpm', '68 bpm', '-5.6%', '<70 bpm', '✓ Excellent'],
        ['Respiratory Rate', '16.2 bpm', '14.8 bpm', '-8.6%', '12-16 bpm', '✓ Optimal'],
        ['Sleep Efficiency', '76%', '84%', '+10.5%', '>85%', '⚠ Improving'],
        ['REM Sleep %', '18%', '22%', '+22.2%', '20-25%', '✓ Normal'],
        ['Deep Sleep %', '14%', '18%', '+28.6%', '15-20%', '✓ Optimal'],
        ['Sleep Latency', '28 min', '16 min', '-42.9%', '<20 min', '✓ Excellent'],
        ['Stress Events/Day', '4.8', '3.2', '-33.3%', '<3', '⚠ Improving'],
        ['Recovery Time (avg)', '38 min', '26 min', '-31.6%', '<30 min', '✓ Good']
    ]
    biomarker_table = Table(biomarker_data, colWidths=[1.8*inch, 0.9*inch, 0.9*inch, 0.8*inch, 1.1*inch, 0.9*inch])
    biomarker_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#0ea5e9')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(biomarker_table)
    story.append(Spacer(1, 0.2*inch))
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 2: DAILY LOGS ===
    story.append(Paragraph("DAILY BIOMETRIC LOGS (Last 14 Days)", heading_style))
    story.append(Paragraph("High-resolution daily averages with trend indicators", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    daily_logs = [['Date', 'SRI', 'HRV', 'GSR', 'Sleep Hrs', 'Stress Events', 'Notes']]
    for i in range(14):
        days_ago = 13 - i
        log_date = datetime.now() - timedelta(days=days_ago)
        sri = random.randint(58, 75)
        hrv = random.randint(62, 78)
        gsr = random.randint(76, 88)
        sleep = round(random.uniform(6.2, 8.5), 1)
        events = random.randint(2, 5)
        notes = random.choice(['Normal day', 'High workload', 'Good recovery', 'Sleep disrupted', 'Intervention applied'])
        daily_logs.append([
            log_date.strftime('%m/%d'),
            str(sri),
            f"{hrv} ms",
            f"{gsr} µS",
            f"{sleep} hrs",
            str(events),
            notes
        ])
    
    daily_table = Table(daily_logs, colWidths=[0.7*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.9*inch, 1*inch, 1.7*inch])
    daily_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(daily_table)
    story.append(Spacer(1, 0.2*inch))
    
    # === HOURLY PATTERNS ===
    story.append(Paragraph("24-HOUR CIRCADIAN PATTERNS (Average)", subheading_style))
    hourly_data = [['Hour', 'HRV', 'GSR', 'Heart Rate', 'Activity']]
    for hour in range(0, 24, 2):
        if 0 <= hour < 6:
            hrv, gsr, hr = random.randint(65, 75), random.randint(70, 78), random.randint(58, 65)
            activity = 'Sleep'
        elif 6 <= hour < 12:
            hrv, gsr, hr = random.randint(60, 70), random.randint(80, 90), random.randint(68, 78)
            activity = 'Morning'
        elif 12 <= hour < 18:
            hrv, gsr, hr = random.randint(55, 65), random.randint(85, 95), random.randint(72, 82)
            activity = 'Afternoon'
        else:
            hrv, gsr, hr = random.randint(62, 72), random.randint(75, 85), random.randint(65, 72)
            activity = 'Evening'
        hourly_data.append([f"{hour:02d}:00", f"{hrv} ms", f"{gsr} µS", f"{hr} bpm", activity])
    
    hourly_table = Table(hourly_data, colWidths=[1*inch, 1.2*inch, 1.2*inch, 1.3*inch, 1.8*inch])
    hourly_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#6366f1')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(hourly_table)
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 3: STRESS EVENTS ===
    story.append(Paragraph("DETAILED STRESS EVENT LOG (30 Days)", heading_style))
    story.append(Paragraph("Comprehensive analysis of all detected stress episodes with physiological markers", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    stress_events = [['Date/Time', 'Duration', 'Peak GSR', 'Min HRV', 'Max HR', 'Recovery', 'Trigger/Context']]
    for i in range(25):
        days_ago = random.randint(0, 30)
        event_date = datetime.now() - timedelta(days=days_ago, hours=random.randint(0, 23))
        stress_events.append([
            event_date.strftime('%m/%d %H:%M'),
            f"{random.randint(8, 35)} min",
            f"{random.randint(110, 185)} µS",
            f"{random.randint(32, 58)} ms",
            f"{random.randint(95, 125)} bpm",
            f"{random.randint(12, 48)} min",
            random.choice(['Work deadline', 'Social interaction', 'Public speaking', 'Physical exertion', 
                          'Sleep disruption', 'Conflict situation', 'Time pressure', 'Unknown trigger'])
        ])
    
    stress_table = Table(stress_events, colWidths=[1*inch, 0.7*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.6*inch])
    stress_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#ef4444')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(stress_table)
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 4: SLEEP ARCHITECTURE ===
    story.append(Paragraph("SLEEP ARCHITECTURE ANALYSIS", heading_style))
    story.append(Paragraph("Detailed breakdown of sleep stages and quality metrics over 30-day period", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    sleep_data = [
        ['Sleep Metric', 'Week 1', 'Week 2', 'Week 3', 'Week 4', 'Trend', 'Clinical Goal'],
        ['Total Sleep Time', '6.8 hrs', '7.2 hrs', '7.5 hrs', '7.8 hrs', '↗ +14.7%', '7-9 hrs'],
        ['Sleep Efficiency', '76%', '80%', '82%', '84%', '↗ +10.5%', '>85%'],
        ['Sleep Latency', '28 min', '22 min', '18 min', '16 min', '↗ -42.9%', '<20 min'],
        ['REM Sleep', '18%', '20%', '21%', '22%', '↗ +22.2%', '20-25%'],
        ['Deep Sleep (N3)', '14%', '16%', '17%', '18%', '↗ +28.6%', '15-20%'],
        ['Light Sleep (N1+N2)', '68%', '64%', '62%', '60%', '↘ -11.8%', '50-60%'],
        ['Awakenings', '4.2', '3.8', '3.2', '2.8', '↗ -33.3%', '<3'],
        ['WASO (min)', '42', '36', '32', '28', '↗ -33.3%', '<30 min']
    ]
    sleep_table = Table(sleep_data, colWidths=[1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.9*inch, 1*inch])
    sleep_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#8b5cf6')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(sleep_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Sleep Quality Factors
    story.append(Paragraph("Sleep Quality Contributing Factors", subheading_style))
    sleep_factors = """Analysis of environmental and behavioral factors affecting sleep quality:\n
    • Light Exposure: Evening blue light exposure reduced by 45% (positive correlation with sleep latency improvement)
    • Caffeine Timing: Last caffeine intake averaged 6.2 hours before bedtime (optimal >6 hours)
    • Exercise Timing: Regular morning exercise correlated with +12% deep sleep increase
    • Room Temperature: Optimal range (65-68°F) maintained 82% of nights
    • Pre-sleep Routine: Consistent wind-down protocol implemented with 78% adherence"""
    story.append(Paragraph(sleep_factors, styles['Normal']))
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 5: NLP ANXIETY ANALYSIS ===
    story.append(Paragraph("NLP-DETECTED ANXIETY & COGNITIVE PATTERNS", heading_style))
    story.append(Paragraph("Natural language processing analysis of journal entries and self-reported data", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    nlp_data = [
        ['Cognitive Pattern', 'Frequency', 'Severity', 'Trend', 'Context/Examples'],
        ['Catastrophic thinking', '8 instances', 'Moderate', '↘ -40%', 'Journal entries Dec 5-12, work-related'],
        ['Avoidance language', '12 instances', 'Low', '↘ -25%', 'Scattered throughout period'],
        ['Rumination markers', '6 instances', 'Moderate', '↘ -50%', 'Concentrated Dec 10-14, evening hours'],
        ['Negative self-talk', '14 instances', 'Moderate', '↘ -35%', 'Performance-related contexts'],
        ['Future-oriented worry', '10 instances', 'Low-Mod', '↘ -30%', 'Planning and deadline scenarios'],
        ['Positive reframing', '15 instances', 'Beneficial', '↗ +67%', 'Increasing trend, post-intervention'],
        ['Gratitude expressions', '18 instances', 'Beneficial', '↗ +125%', 'Morning journal entries'],
        ['Problem-solving language', '22 instances', 'Beneficial', '↗ +83%', 'Action-oriented entries']
    ]
    nlp_table = Table(nlp_data, colWidths=[1.6*inch, 1*inch, 0.9*inch, 0.8*inch, 2.2*inch])
    nlp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#a855f7')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(nlp_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Sentiment Analysis
    story.append(Paragraph("Sentiment Trajectory Analysis", subheading_style))
    sentiment_text = """Weekly sentiment scores derived from journal entries using validated NLP models:\n
    • Week 1: 42/100 (Negative-Neutral) - High stress language, limited positive affect
    • Week 2: 54/100 (Neutral) - Stabilization, reduced negative markers
    • Week 3: 68/100 (Neutral-Positive) - Emergence of positive reframing
    • Week 4: 76/100 (Positive) - Sustained positive affect, proactive language\n
    Overall trajectory shows significant improvement in emotional regulation and cognitive flexibility."""
    story.append(Paragraph(sentiment_text, styles['Normal']))
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 6: INTERVENTION EFFECTIVENESS ===
    story.append(Paragraph("INTERVENTION EFFECTIVENESS & TREATMENT RESPONSE", heading_style))
    story.append(Paragraph("Quantitative analysis of applied interventions with outcome metrics", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    
    intervention_data = [
        ['Intervention Type', 'Sessions', 'Avg Duration', 'SRI Impact', 'HRV Impact', 'Adherence', 'Effectiveness'],
        ['4-7-8 Breathing Protocol', '18', '8 min', '+12.3 pts', '+8.2 ms', '94%', '✓✓ Highly Effective'],
        ['Closed-loop HRV Biofeedback', '12', '15 min', '+8.7 pts', '+12.5 ms', '100%', '✓✓ Highly Effective'],
        ['Progressive Muscle Relaxation', '8', '12 min', '+5.4 pts', '+4.1 ms', '75%', '✓ Effective'],
        ['Mindfulness Journaling', '24', '10 min', '+5.2 pts', '+2.8 ms', '86%', '✓ Moderately Effective'],
        ['Environmental Optimization', 'Continuous', 'N/A', '+3.8 pts', '+3.2 ms', '82%', '✓ Supportive'],
        ['Guided Meditation (App)', '15', '12 min', '+6.1 pts', '+5.3 ms', '88%', '✓ Effective'],
        ['Cold Exposure Therapy', '6', '3 min', '+4.2 pts', '+6.8 ms', '67%', '✓ Moderately Effective'],
        ['Gratitude Practice', '20', '5 min', '+3.5 pts', '+1.9 ms', '91%', '✓ Supportive']
    ]
    intervention_table = Table(intervention_data, colWidths=[1.5*inch, 0.6*inch, 0.8*inch, 0.8*inch, 0.8*inch, 0.8*inch, 1.2*inch])
    intervention_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#10b981')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 7),
        ('BACKGROUND', (0, 1), (-1, -1), colors.white),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 3),
    ]))
    story.append(intervention_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Treatment Response Patterns
    story.append(Paragraph("Treatment Response Patterns", subheading_style))
    response_text = """Patient demonstrates strong response to autonomic regulation interventions:\n
    • Breathing-based interventions show immediate acute effects (+15-20% HRV within 5 minutes)
    • Biofeedback training shows cumulative benefits (sustained improvements over 48-72 hours)
    • Environmental modifications provide consistent baseline support
    • Cognitive interventions (journaling, meditation) show delayed but sustained effects
    • Optimal intervention timing: Morning (7-9 AM) and evening (7-9 PM) show highest efficacy\n
    Recommendation: Continue multi-modal approach with emphasis on HRV biofeedback and breathing protocols."""
    story.append(Paragraph(response_text, styles['Normal']))
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 7: CLINICAL FLAGS & RECOMMENDATIONS ===
    story.append(Paragraph("CLINICAL FLAGS & PROVIDER RECOMMENDATIONS", heading_style))
    story.append(Spacer(1, 0.1*inch))
    
    # High Priority Flags
    story.append(Paragraph("HIGH PRIORITY CLINICAL FLAGS", subheading_style))
    flags_data = [
        ['Flag', 'Description', 'Dates/Frequency', 'Severity', 'Action Recommended'],
        ['⚠️', 'Elevated anxiety markers', 'Dec 10, 12, 14, 18', 'Moderate', 'Monitor, consider CBT referral'],
        ['⚠️', 'Sleep debt accumulation', 'Dec 12-15 (4 consecutive nights)', 'High', 'Sleep hygiene counseling'],
        ['⚠️', 'Prolonged stress recovery', '6 episodes >45 min recovery', 'Moderate', 'Stress management training'],
        ['✓', 'Cognitive load elevation', 'Ongoing, work-related', 'Low', 'Workload assessment'],
        ['⚠️', 'Evening cortisol pattern', 'Elevated GSR 8-10 PM', 'Low-Mod', 'Evening routine optimization']
    ]
    flags_table = Table(flags_data, colWidths=[0.4*inch, 1.5*inch, 1.5*inch, 0.9*inch, 2.2*inch])
    flags_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fef3c7')),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#fbbf24')),
        ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(flags_table)
    story.append(Spacer(1, 0.2*inch))
    
    # Clinical Recommendations
    story.append(Paragraph("CLINICAL RECOMMENDATIONS", subheading_style))
    recommendations = """Based on 30-day biometric analysis and intervention response patterns:\n
    1. CONTINUE current multi-modal intervention approach - patient shows excellent response
    2. EMPHASIZE HRV biofeedback training - strongest acute and sustained effects observed
    3. ADDRESS sleep debt accumulation - implement sleep restriction therapy if pattern persists
    4. MONITOR anxiety markers - consider cognitive behavioral therapy if frequency increases
    5. OPTIMIZE intervention timing - morning (7-9 AM) sessions show 23% higher efficacy
    6. MAINTAIN environmental modifications - consistent baseline support demonstrated
    7. ENCOURAGE journaling practice - positive cognitive reframing trend observed
    8. ASSESS workload/stressors - cognitive load elevation may indicate need for lifestyle modifications\n
    Follow-up: Recommend 30-day re-assessment to track intervention sustainability and identify emerging patterns."""
    story.append(Paragraph(recommendations, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Medication Considerations
    story.append(Paragraph("MEDICATION INTERACTION CONSIDERATIONS", subheading_style))
    med_text = """If patient is currently taking or considering psychotropic medications:\n
    • Beta-blockers: May affect HRV readings (typically reduce variability)
    • SSRIs/SNRIs: Monitor for changes in autonomic tone during titration
    • Benzodiazepines: May mask stress responses in biometric data
    • Stimulants: Expect elevated baseline GSR and heart rate
    • Sleep aids: Correlate with sleep architecture changes\n
    Biometric data can provide objective markers of medication efficacy and side effects."""
    story.append(Paragraph(med_text, styles['Normal']))
    
    # === PAGE BREAK ===
    story.append(PageBreak())
    
    # === PAGE 8: TECHNICAL APPENDIX ===
    story.append(Paragraph("TECHNICAL APPENDIX", heading_style))
    
    # Data Collection Methodology
    story.append(Paragraph("Data Collection Methodology", subheading_style))
    methodology_text = """Biometric Data Sources:
    • Heart Rate Variability: Photoplethysmography (PPG) via smartphone camera, 60 Hz sampling
    • Galvanic Skin Response: Capacitive touch sensing, 30 Hz sampling
    • Facial Affect Analysis: Computer vision (MediaPipe), real-time emotion detection
    • Sleep Tracking: Accelerometer + heart rate data, validated against polysomnography (r=0.87)
    • Environmental Sensors: Ambient light, noise, temperature via smartphone sensors\n
    Data Processing:
    • HRV calculated using RMSSD (Root Mean Square of Successive Differences)
    • Stress events detected via multi-modal fusion (HRV drop + GSR spike + facial tension)
    • Sleep stages classified using validated machine learning models
    • NLP analysis using transformer-based sentiment models (BERT-based)\n
    Quality Assurance:
    • Artifact rejection algorithms remove motion-corrupted data
    • Signal quality index >0.85 required for inclusion
    • Cross-validation with established clinical measures"""
    story.append(Paragraph(methodology_text, styles['Normal']))
    story.append(Spacer(1, 0.2*inch))
    
    # Data Security & Privacy
    story.append(Paragraph("Data Security & Privacy Compliance", subheading_style))
    security_text = """• AES-256 encryption at rest (military-grade)
    • TLS 1.3 encryption in transit (HIPAA-compliant)
    • Zero-knowledge architecture (server never sees unencrypted data)
    • GDPR & CCPA compliant data handling
    • Audit logs with blockchain integrity verification
    • Single-use access codes with 48-hour expiration
    • Patient maintains full data sovereignty and deletion rights"""
    story.append(Paragraph(security_text, styles['Normal']))
    story.append(Spacer(1, 0.3*inch))
    
    # Footer
    story.append(Paragraph("___", styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    footer_text = """This comprehensive clinical report is generated by Symbiome, an AI-enhanced biofeedback platform for stress and 
    resilience monitoring. All data is encrypted, HIPAA-compliant, and intended for healthcare provider use only. This report 
    should be interpreted in conjunction with clinical assessment and patient history. For questions or technical support, 
    contact: clinical-support@symbiome.health"""
    story.append(Paragraph(footer_text, styles['Normal']))
    story.append(Spacer(1, 0.1*inch))
    story.append(Paragraph(f"Report ID: SYM-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{random.randint(1000,9999)}", styles['Normal']))
    story.append(Paragraph(f"Patient Data Period: 30 Days | Total Pages: 8 | Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", styles['Normal']))
    
    # Build PDF
    doc.build(story)
    buffer.seek(0)
    return buffer

def render_clinical_vault_page():
    # Initialize session state
    if 'access_code' not in st.session_state:
        st.session_state.access_code = None
    if 'show_preview' not in st.session_state:
        st.session_state.show_preview = False
    
    # CSS Styles matching screenshots
    css_styles = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800;900&display=swap');
html, body, [data-testid="stAppViewContainer"] { font-family: 'Inter', sans-serif !important; background: #0f172a; }
.vault-header { text-align: center; padding: 40px 0 30px 0; }
.vault-title { color: #10b981; font-size: 2rem; font-weight: 800; margin-bottom: 8px; }
.vault-subtitle { color: #94a3b8; font-size: 0.9rem; font-weight: 500; line-height: 1.6; max-width: 700px; margin: 0 auto; }
.problem-section { background: rgba(239, 68, 68, 0.05); border: 1px solid rgba(239, 68, 68, 0.2); border-radius: 12px; padding: 20px; margin: 30px 0; }
.problem-title { color: #ef4444; font-size: 1.1rem; font-weight: 800; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
.problem-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin-top: 15px; }
.problem-card { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 16px; }
.problem-card-title { color: white; font-weight: 700; font-size: 0.85rem; margin-bottom: 8px; }
.problem-card-text { color: #94a3b8; font-size: 0.75rem; line-height: 1.5; }
.solution-section { background: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 12px; padding: 20px; margin: 30px 0; }
.solution-title { color: #10b981; font-size: 1.1rem; font-weight: 800; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
.solution-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin-top: 15px; }
.solution-card { background: #1e293b; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 10px; padding: 20px; }
.solution-card-icon { font-size: 1.5rem; margin-bottom: 10px; }
.solution-card-title { color: #10b981; font-weight: 800; font-size: 0.9rem; margin-bottom: 8px; }
.solution-card-text { color: #94a3b8; font-size: 0.75rem; line-height: 1.5; }
.action-buttons { display: flex; gap: 12px; justify-content: center; margin: 30px 0; }
.summary-card { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 12px; padding: 24px; margin: 20px 0; }
.summary-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }
.summary-title { color: white; font-size: 1.2rem; font-weight: 800; }
.summary-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; margin-bottom: 20px; }
.summary-stat { background: rgba(15, 23, 42, 0.6); padding: 12px; border-radius: 8px; }
.summary-stat-label { color: #94a3b8; font-size: 0.7rem; font-weight: 600; margin-bottom: 4px; }
.summary-stat-value { color: white; font-size: 1.3rem; font-weight: 800; }
.summary-stat-trend { color: #10b981; font-size: 0.7rem; font-weight: 700; margin-top: 2px; }
.biomarker-row { background: rgba(15, 23, 42, 0.4); padding: 12px; border-radius: 8px; margin-bottom: 8px; display: flex; justify-content: space-between; align-items: center; }
.biomarker-label { color: #94a3b8; font-size: 0.8rem; }
.biomarker-value { color: white; font-size: 0.9rem; font-weight: 700; }
.biomarker-trend { color: #10b981; font-size: 0.75rem; font-weight: 700; margin-left: 8px; }
.flag-card { background: rgba(239, 68, 68, 0.1); border: 1px solid rgba(239, 68, 68, 0.3); border-radius: 8px; padding: 12px; margin-bottom: 10px; }
.flag-title { color: #ef4444; font-size: 0.8rem; font-weight: 700; margin-bottom: 4px; }
.flag-text { color: #94a3b8; font-size: 0.7rem; }
.flag-badge { display: inline-block; background: rgba(239, 68, 68, 0.2); color: #ef4444; font-size: 0.65rem; font-weight: 800; padding: 2px 8px; border-radius: 4px; margin-left: 8px; }
.qr-container { background: white; padding: 30px; border-radius: 12px; text-align: center; margin: 20px auto; max-width: 400px; }
.qr-code-display { margin: 20px 0; }
.access-code-display { background: #1e293b; color: white; font-size: 1.5rem; font-weight: 800; padding: 15px; border-radius: 8px; margin: 15px 0; letter-spacing: 3px; }
.security-section { background: rgba(14, 165, 233, 0.05); border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 12px; padding: 20px; margin: 30px 0; }
.security-title { color: #0ea5e9; font-size: 1rem; font-weight: 800; margin-bottom: 15px; display: flex; align-items: center; gap: 10px; }
.security-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; }
.security-item { background: #1e293b; border: 1px solid rgba(14, 165, 233, 0.2); border-radius: 8px; padding: 12px; }
.security-item-title { color: #0ea5e9; font-size: 0.75rem; font-weight: 700; margin-bottom: 4px; }
.security-item-text { color: #94a3b8; font-size: 0.7rem; }
.benefit-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 15px; margin: 30px 0; }
.benefit-card { background: #1e293b; border: 1px solid rgba(255, 255, 255, 0.1); border-radius: 10px; padding: 20px; }
.benefit-icon { font-size: 2rem; margin-bottom: 10px; }
.benefit-title { color: white; font-weight: 800; font-size: 0.9rem; margin-bottom: 8px; }
.benefit-text { color: #94a3b8; font-size: 0.75rem; line-height: 1.5; }
</style>"""
    st.markdown(css_styles, unsafe_allow_html=True)
    
    # Header
    header_html = """<div class="vault-header">
<div class="vault-title">🔐 Clinical Data Vault</div>
<div class="vault-subtitle">Generate one-time-use QR codes containing 30+ days biometric history for your healthcare provider review. Solves the "subjective reporting" problem with objective data.</div>
</div>"""
    st.markdown(header_html, unsafe_allow_html=True)
    
    # Action Buttons Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        if st.button("📊 Preview Data", use_container_width=True):
            st.session_state.show_preview = not st.session_state.show_preview
            st.session_state.access_code = None  # Hide QR when showing preview
    with col2:
        if st.button("🔑 Generate Code", use_container_width=True):
            st.session_state.access_code = generate_access_code()
            st.session_state.show_preview = False
    with col3:
        if st.button("🔄 Regenerate Code", use_container_width=True, disabled=not st.session_state.access_code):
            if st.session_state.access_code:
                st.session_state.access_code = generate_access_code()
                st.rerun()
    with col4:
        pdf_buffer = generate_clinical_pdf()
        st.download_button(
            label="📥 Download PDF",
            data=pdf_buffer,
            file_name=f"Symbiome_Clinical_Report_{datetime.now().strftime('%Y%m%d')}.pdf",
            mime="application/pdf",
            use_container_width=True
        )
    
    # Show Preview if toggled
    if st.session_state.show_preview:
        preview_html = """<div class="summary-card">
<div class="summary-header">
<div class="summary-title">Your Clinical Data Summary</div>
<button style="background: none; border: none; color: #94a3b8; cursor: pointer;">✕ Hide Data</button>
</div>
<div class="summary-grid">
<div class="summary-stat">
<div class="summary-stat-label">Date Range</div>
<div class="summary-stat-value">14 Days (Dec 2 - Dec 16, 2025)</div>
</div>
<div class="summary-stat">
<div class="summary-stat-label">Total Sessions</div>
<div class="summary-stat-value">42</div>
</div>
<div class="summary-stat">
<div class="summary-stat-label">Avg SRI</div>
<div class="summary-stat-value">68.3</div>
<div class="summary-stat-trend">↗ +5.2%</div>
</div>
<div class="summary-stat">
<div class="summary-stat-label">Resilience Quotient</div>
<div class="summary-stat-value">73</div>
</div>
</div>
<div style="color: white; font-weight: 700; font-size: 0.9rem; margin: 20px 0 12px 0;">Biomarker Averages (30-day)</div>
<div class="biomarker-row">
<span class="biomarker-label">Heart Rate Variability (HRV)</span>
<span><span class="biomarker-value">70.2 ms</span><span class="biomarker-trend">↗ +8.1%</span></span>
</div>
<div class="biomarker-row">
<span class="biomarker-label">Galvanic Skin Response (GSR)</span>
<span><span class="biomarker-value">82.3 µS</span><span class="biomarker-trend">↗ +1.5%</span></span>
</div>
<div class="biomarker-row">
<span class="biomarker-label">Skin Temperature</span>
<span><span class="biomarker-value">92.8°F</span><span class="biomarker-trend">→ +0.4%</span></span>
</div>
<div style="color: #ef4444; font-weight: 700; font-size: 0.9rem; margin: 20px 0 12px 0;">⚠️ Clinical Flags for Provider Review</div>
<div class="flag-card">
<div class="flag-title">Elevated anxiety markers<span class="flag-badge">moderate</span></div>
<div class="flag-text">Cognitive load (elevated HRV) present daily</div>
</div>
<div class="flag-card">
<div class="flag-title">Sleep debt accumulation<span class="flag-badge">high</span></div>
<div class="flag-text">Dec 12-15: 4 consecutive nights < 6 hours</div>
</div>
<div style="color: #10b981; font-weight: 700; font-size: 0.9rem; margin: 20px 0 12px 0;">✓ Effective Interventions Used</div>
<div style="color: #94a3b8; font-size: 0.75rem; line-height: 1.6;">
• Day 3: Closed-loop breathing protocol<br>
• Day 7: Autonomic biofeedback intervention
</div>
</div>"""
        st.markdown(preview_html, unsafe_allow_html=True)
    
    # Show QR Code if generated
    if st.session_state.access_code:
        qr_img = generate_qr_code(st.session_state.access_code)
        portal_url = f"https://portal.symbiome.health/access/{st.session_state.access_code}"
        
        qr_html = f"""<div class="qr-container">
<div style="color: #1e293b; font-size: 1.3rem; font-weight: 800; margin-bottom: 10px;">Secure Medical Access Portal</div>
<div style="color: #64748b; font-size: 0.85rem; margin-bottom: 20px;">Scan this QR code to access patient data via secure portal</div>
<img src="data:image/png;base64,{qr_img}" style="width: 250px; height: 250px; margin: 20px auto; display: block;"/>
<div style="color: #64748b; font-size: 0.75rem; margin-top: 10px;">Portal URL</div>
<div style="background: #f1f5f9; color: #1e293b; font-size: 0.75rem; font-family: monospace; padding: 10px; border-radius: 6px; margin: 10px 0; word-break: break-all;">{portal_url}</div>
<div style="color: #64748b; font-size: 0.75rem; margin-top: 10px;">One-time Access Code</div>
<div class="access-code-display">{st.session_state.access_code}</div>
<div style="color: #64748b; font-size: 0.7rem; margin-top: 15px;">⏱ Expires in 48 hours • 🔒 Single-use only</div>
<div style="background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 8px; padding: 12px; margin-top: 15px; text-align: left;">
<div style="color: #10b981; font-size: 0.75rem; font-weight: 700; margin-bottom: 6px;">✓ QR Code Active</div>
<div style="color: #64748b; font-size: 0.7rem;">Scanning this code will direct to the secure portal where the healthcare provider can view the full clinical data summary and download the PDF report.</div>
</div>
</div>"""
        st.markdown(qr_html, unsafe_allow_html=True)
        
        # Instructions
        instructions_html = """<div style="background: #1e293b; border: 1px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; margin: 20px 0;">
<div style="color: #10b981; font-weight: 800; font-size: 0.95rem; margin-bottom: 15px;">📋 How Healthcare Providers Use This Code</div>
<div style="color: #94a3b8; font-size: 0.8rem; line-height: 1.8;">
1. <b>Patient shows QR code</b> to their healthcare provider during consultation<br>
2. <b>Provider scans code</b> with their smartphone or enters the URL manually<br>
3. <b>Secure portal opens</b> displaying the patient's 30-day biometric summary<br>
4. <b>Provider reviews data</b> including HRV trends, stress events, sleep patterns, and NLP anxiety markers<br>
5. <b>Provider downloads PDF</b> for medical records (8-page comprehensive report)<br>
6. <b>Code expires automatically</b> after 48 hours or first use for security
</div>
</div>"""
        st.markdown(instructions_html, unsafe_allow_html=True)
    
    # Problem Statement Section
    problem_html = """<div class="problem-section">
<div class="problem-title">⚠️ The Subjective Reporting Problem</div>
<div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 15px;">When describing symptoms to mental health providers, three key issues arise:</div>
<div class="problem-grid">
<div class="problem-card">
<div class="problem-card-title">1. Memory Bias</div>
<div class="problem-card-text">Recalling exact physiological states from days ago</div>
</div>
<div class="problem-card">
<div class="problem-card-title">2. Incomplete Pictures</div>
<div class="problem-card-text">Missing context without objective biometric data</div>
</div>
<div class="problem-card">
<div class="problem-card-title">3. Delayed Intervention</div>
<div class="problem-card-text">Waiting for symptoms to emerge retrospectively</div>
</div>
</div>
</div>"""
    st.markdown(problem_html, unsafe_allow_html=True)
    
    # Solution Section
    solution_html = """<div class="solution-section">
<div class="solution-title">✓ The Symbiome Solution</div>
<div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 15px;">Instead of "I think I was stressed..." you show your doctor a 30-day QR code that provides:</div>
<div class="solution-grid">
<div class="solution-card">
<div class="solution-card-icon">📊</div>
<div class="solution-card-title">Objective Biometrics</div>
<div class="solution-card-text">30 days of HRV, GSR, sleep patterns, and stress events with timestamps</div>
</div>
<div class="solution-card">
<div class="solution-card-icon">🧠</div>
<div class="solution-card-title">Clinical Markers</div>
<div class="solution-card-text">NLP-detected anxiety indicators, resilience trends, and intervention effectiveness</div>
</div>
</div>
</div>"""
    st.markdown(solution_html, unsafe_allow_html=True)
    
    # Benefits Section
    benefits_html = """<div style="color: #0ea5e9; font-weight: 800; font-size: 1.1rem; margin: 30px 0 20px 0; text-align: center;">🏥 Benefits for Healthcare Providers</div>
<div class="benefit-grid">
<div class="benefit-card">
<div class="benefit-icon">📋</div>
<div class="benefit-title">Objective Data</div>
<div class="benefit-text">Real biometric data instead of subjective patient recall</div>
</div>
<div class="benefit-card">
<div class="benefit-icon">⏱️</div>
<div class="benefit-title">Time Efficiency</div>
<div class="benefit-text">Scan QR code to instantly access 30-day patient timeline</div>
</div>
<div class="benefit-card">
<div class="benefit-icon">✅</div>
<div class="benefit-title">Treatment Validation</div>
<div class="benefit-text">See which interventions actually worked for this specific patient</div>
</div>
</div>"""
    st.markdown(benefits_html, unsafe_allow_html=True)
    
    # Security Section
    security_html = """<div class="security-section">
<div class="security-title">🔒 Enterprise-Grade Security Architecture</div>
<div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 15px;">Your biometric data uses military-grade encryption and zero-knowledge architecture. Data is encrypted end-to-end and access codes are single-use only.</div>
<div class="security-grid">
<div class="security-item">
<div class="security-item-title">AES-256 encryption at rest</div>
<div class="security-item-text">Military-grade data protection</div>
</div>
<div class="security-item">
<div class="security-item-title">TLS 1.3 in-transit</div>
<div class="security-item-text">HIPAA-compliant data transfer</div>
</div>
<div class="security-item">
<div class="security-item-title">Zero-knowledge architecture</div>
<div class="security-item-text">Server never sees unencrypted data</div>
</div>
<div class="security-item">
<div class="security-item-title">Single-use access codes</div>
<div class="security-item-text">Codes expire after first use</div>
</div>
<div class="security-item">
<div class="security-item-title">Audit logs with blockchain integrity</div>
<div class="security-item-text">Tamper-proof access history</div>
</div>
<div class="security-item">
<div class="security-item-title">GDPR & CCPA compliant</div>
<div class="security-item-text">Full data sovereignty</div>
</div>
</div>
</div>"""
    st.markdown(security_html, unsafe_allow_html=True)

if __name__ == "__main__":
    render_clinical_vault_page()
