"""
RQ PDF Export Module
Generates comprehensive Resilience Quotient™ PDF reports.
Includes: Executive Summary, Domain Breakdown, Visual Evidence, 
Interpretation Guide, Ethical Disclaimer, and Model Transparency.
"""
from reportlab.lib.pagesizes import letter, A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.pdfgen import canvas
from datetime import datetime
import io
import plotly.graph_objects as go
from PIL import Image as PILImage

class RQPDFExporter:
    """Generate comprehensive RQ PDF reports."""
    
    def __init__(self, rq_data, trend_data, stress_events):
        """
        Initialize PDF exporter.
        
        Args:
            rq_data: Dictionary with RQ score and domain metrics
            trend_data: List of trend data points
            stress_events: List of stress response events
        """
        self.rq_data = rq_data
        self.trend_data = trend_data
        self.stress_events = stress_events
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        """Setup custom paragraph styles."""
        # Title style
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#1e293b'),
            spaceAfter=30,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#334155'),
            spaceAfter=12,
            spaceBefore=20,
            fontName='Helvetica-Bold'
        ))
        
        # Disclaimer style
        self.styles.add(ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=colors.HexColor('#64748b'),
            alignment=TA_JUSTIFY,
            leftIndent=20,
            rightIndent=20,
            spaceAfter=10
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='BodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#1e293b'),
            alignment=TA_JUSTIFY,
            spaceAfter=12
        ))
    
    def generate_pdf(self, filename="rq_report.pdf"):
        """
        Generate complete PDF report.
        
        Args:
            filename: Output filename
        
        Returns:
            BytesIO buffer with PDF content
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=72,
            leftMargin=72,
            topMargin=72,
            bottomMargin=18
        )
        
        # Build document content
        story = []
        
        # Page 1: Executive Summary
        story.extend(self._build_executive_summary())
        story.append(PageBreak())
        
        # Page 2: Domain Breakdown
        story.extend(self._build_domain_breakdown())
        story.append(PageBreak())
        
        # Page 3: Visual Evidence
        story.extend(self._build_visual_evidence())
        story.append(PageBreak())
        
        # Page 4: Interpretation Guide & Ethical Disclaimer
        story.extend(self._build_interpretation_guide())
        story.extend(self._build_ethical_disclaimer())
        story.append(PageBreak())
        
        # Page 5: Model Transparency
        story.extend(self._build_model_transparency())
        
        # Build PDF
        doc.build(story)
        buffer.seek(0)
        return buffer
    
    def _build_executive_summary(self):
        """Build executive summary section."""
        elements = []
        
        # Title
        elements.append(Paragraph("Resilience Quotient™ Report", self.styles['CustomTitle']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Disclaimer box
        disclaimer_text = """
        <b>IMPORTANT NOTICE:</b> This report is a research and self-awareness tool only. 
        It is NOT a medical diagnosis, clinical assessment, or substitute for professional healthcare. 
        The Resilience Quotient™ measures adaptive capacity to stress, not mental health status.
        """
        elements.append(Paragraph(disclaimer_text, self.styles['Disclaimer']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Report metadata
        metadata = [
            ['Report Generated:', datetime.now().strftime('%B %d, %Y at %I:%M %p')],
            ['Report Type:', 'Resilience Quotient™ Analysis'],
            ['Data Timeframe:', f"{len(self.trend_data)} days of tracking"],
        ]
        
        metadata_table = Table(metadata, colWidths=[2*inch, 4*inch])
        metadata_table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (0, -1), colors.HexColor('#64748b')),
            ('TEXTCOLOR', (1, 0), (1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ]))
        elements.append(metadata_table)
        elements.append(Spacer(1, 0.4*inch))
        
        # Executive Summary
        elements.append(Paragraph("Executive Summary", self.styles['SectionHeader']))
        
        rq_score = self.rq_data['rq_score']
        descriptor = self.rq_data['descriptor']
        confidence = self.rq_data['confidence']
        
        # Current RQ Score
        summary_data = [
            ['Current Resilience Quotient™', f"{rq_score}/100"],
            ['Classification', descriptor],
            ['Model Confidence', f"{confidence:.1%}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 3*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 12),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0, 0), (-1, -1), 8),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        elements.append(summary_table)
        elements.append(Spacer(1, 0.3*inch))
        
        # Trend Overview
        if len(self.trend_data) > 1:
            first_score = self.trend_data[0]['rq_score']
            last_score = self.trend_data[-1]['rq_score']
            change = last_score - first_score
            
            if change > 5:
                trend_text = f"<b>Trend:</b> Improving (+{change} points over tracking period)"
            elif change < -5:
                trend_text = f"<b>Trend:</b> Declining ({change} points over tracking period)"
            else:
                trend_text = "<b>Trend:</b> Stable (minimal variation over tracking period)"
        else:
            trend_text = "<b>Trend:</b> Insufficient data for trend analysis"
        
        elements.append(Paragraph(trend_text, self.styles['BodyText']))
        
        # Confidence Statement
        confidence_text = f"""
        <b>Confidence Statement:</b> This RQ score is based on {len(self.trend_data)} days of data 
        with a model confidence of {confidence:.1%}. The score represents your current adaptive 
        capacity to stress, measured across four domains: Recovery Speed, Consistency, Adaptability, 
        and Load Tolerance.
        """
        elements.append(Paragraph(confidence_text, self.styles['BodyText']))
        
        return elements
    
    def _build_domain_breakdown(self):
        """Build domain breakdown section."""
        elements = []
        
        elements.append(Paragraph("Domain Breakdown", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        domains = self.rq_data['domains']
        
        # Domain 1: Recovery Speed
        elements.append(Paragraph("<b>1. Recovery Speed (Weight: 30%)</b>", self.styles['BodyText']))
        rs = domains['recovery_speed']
        rs_text = f"""
        <b>Average Recovery Time:</b> {rs['value']} (minutes to baseline)<br/>
        <b>Score:</b> {rs['score']}/100 (Percentile: {rs['percentile']}th)<br/>
        <b>Interpretation:</b> Measures how quickly your physiology returns to baseline after stress. 
        Faster recovery indicates better vagal tone and sympathetic-parasympathetic balance.
        """
        elements.append(Paragraph(rs_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Domain 2: Consistency
        elements.append(Paragraph("<b>2. Consistency (Weight: 25%)</b>", self.styles['BodyText']))
        c = domains['consistency']
        c_text = f"""
        <b>Stability Percentage:</b> {c['value']}%<br/>
        <b>Trend:</b> {c['trend']}<br/>
        <b>Interpretation:</b> Measures stability of performance and regulation across days. 
        Higher consistency indicates reliable stress management and reduced volatility.
        """
        elements.append(Paragraph(c_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Domain 3: Adaptability
        elements.append(Paragraph("<b>3. Adaptability (Weight: 25%)</b>", self.styles['BodyText']))
        a = domains['adaptability']
        a_text = f"""
        <b>30-Day Improvement:</b> {a['value']:+d}%<br/>
        <b>Interpretation:</b> Measures efficiency of improvement to repeated stressors. 
        Positive values indicate learning and adaptation; negative values suggest accumulated fatigue.
        """
        elements.append(Paragraph(a_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Domain 4: Load Tolerance
        elements.append(Paragraph("<b>4. Load Tolerance (Weight: 20%)</b>", self.styles['BodyText']))
        lt = domains['load_tolerance']
        lt_text = f"""
        <b>Stress Events Handled:</b> {lt['value']}<br/>
        <b>Degradation Level:</b> {lt['degradation'].capitalize()}<br/>
        <b>Interpretation:</b> Measures how many stress events can be handled without cumulative degradation. 
        Higher tolerance with minimal degradation indicates robust resilience capacity.
        """
        elements.append(Paragraph(lt_text, self.styles['BodyText']))
        
        return elements
    
    def _build_visual_evidence(self):
        """Build visual evidence section with charts."""
        elements = []
        
        elements.append(Paragraph("Visual Evidence", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Note about charts
        chart_note = """
        The following visualizations provide graphical evidence of your resilience patterns over time. 
        These charts are generated from your actual tracking data and show objective trends.
        """
        elements.append(Paragraph(chart_note, self.styles['BodyText']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Trend Chart (simplified for PDF)
        elements.append(Paragraph("<b>Resilience Quotient Trend</b>", self.styles['BodyText']))
        trend_text = f"""
        Tracking period: {len(self.trend_data)} days<br/>
        Mean RQ: {sum(d['rq_score'] for d in self.trend_data) / len(self.trend_data):.1f}<br/>
        Range: {min(d['rq_score'] for d in self.trend_data)} - {max(d['rq_score'] for d in self.trend_data)}
        """
        elements.append(Paragraph(trend_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.3*inch))
        
        # Stress Response Summary
        elements.append(Paragraph("<b>Stress Response Profile</b>", self.styles['BodyText']))
        
        fast_count = len([e for e in self.stress_events if e['category'] == "Fast (< 5min)"])
        moderate_count = len([e for e in self.stress_events if e['category'] == "Moderate (5-10min)"])
        slow_count = len([e for e in self.stress_events if e['category'] == "Slow (> 10min)"])
        
        stress_data = [
            ['Recovery Category', 'Event Count', 'Percentage'],
            ['Fast (< 5 min)', str(fast_count), f"{fast_count/len(self.stress_events)*100:.1f}%"],
            ['Moderate (5-10 min)', str(moderate_count), f"{moderate_count/len(self.stress_events)*100:.1f}%"],
            ['Slow (> 10 min)', str(slow_count), f"{slow_count/len(self.stress_events)*100:.1f}%"],
        ]
        
        stress_table = Table(stress_data, colWidths=[2.5*inch, 1.5*inch, 1.5*inch])
        stress_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(stress_table)
        
        return elements
    
    def _build_interpretation_guide(self):
        """Build interpretation guide section."""
        elements = []
        
        elements.append(Paragraph("Interpretation Guide", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # What RQ Means
        elements.append(Paragraph("<b>What the Resilience Quotient™ Means:</b>", self.styles['BodyText']))
        what_means = """
        • A measure of your <b>adaptive capacity</b> to stress, not your stress level<br/>
        • Reflects how well your nervous system <b>recovers, adapts, and maintains stability</b><br/>
        • Based on <b>physiological patterns</b>, not subjective feelings<br/>
        • Provides <b>objective feedback</b> for resilience training<br/>
        • Helps identify <b>patterns and trends</b> over time
        """
        elements.append(Paragraph(what_means, self.styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
        
        # What RQ Does NOT Mean
        elements.append(Paragraph("<b>What the Resilience Quotient™ Does NOT Mean:</b>", self.styles['BodyText']))
        what_not_means = """
        • <b>NOT a diagnosis</b> of any medical or mental health condition<br/>
        • <b>NOT a measure</b> of mental health, wellness, or happiness<br/>
        • <b>NOT a prediction</b> of future health outcomes<br/>
        • <b>NOT a substitute</b> for professional medical or psychological care<br/>
        • <b>NOT a comparison</b> to "normal" or "healthy" standards
        """
        elements.append(Paragraph(what_not_means, self.styles['BodyText']))
        
        return elements
    
    def _build_ethical_disclaimer(self):
        """Build ethical disclaimer section."""
        elements = []
        
        elements.append(Spacer(1, 0.3*inch))
        elements.append(Paragraph("Ethical Disclaimer", self.styles['SectionHeader']))
        
        disclaimer = """
        <b>Research & Self-Awareness Tool Only:</b> The Resilience Quotient™ is designed for 
        research and educational purposes. It provides insights into your adaptive capacity 
        but does not diagnose, treat, or prevent any disease or condition.
        <br/><br/>
        <b>Not Clinical Advice:</b> This report is not medical, psychological, or clinical advice. 
        If you have concerns about your health or wellbeing, please consult a qualified healthcare 
        professional.
        <br/><br/>
        <b>Data Privacy:</b> Your data is processed with privacy-first principles. Derived metrics 
        are stored; raw physiological data is encrypted or ephemeral based on your privacy settings.
        <br/><br/>
        <b>User Agency:</b> You maintain full control over your data, interpretations, and actions. 
        This tool is designed to empower self-awareness, not to label or limit you.
        """
        elements.append(Paragraph(disclaimer, self.styles['Disclaimer']))
        
        return elements
    
    def _build_model_transparency(self):
        """Build model transparency section."""
        elements = []
        
        elements.append(Paragraph("Model Transparency", self.styles['SectionHeader']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Algorithm Description
        elements.append(Paragraph("<b>Algorithm Description:</b>", self.styles['BodyText']))
        algo_text = """
        The Resilience Quotient™ is calculated using a weighted composite algorithm combining 
        four domains: Recovery Speed (30%), Consistency (25%), Adaptability (25%), and Load 
        Tolerance (20%). These weights are personalized weekly based on individual patterns.
        """
        elements.append(Paragraph(algo_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.15*inch))
        
        # Input Contributions
        elements.append(Paragraph("<b>Input Contributions (Current Report):</b>", self.styles['BodyText']))
        
        weights = self.rq_data['weights']
        contributions = [
            ['Domain', 'Current Weight', 'Contribution to RQ'],
            ['Recovery Speed', f"{weights['recovery_speed']:.0%}", 
             f"{self.rq_data['domains']['recovery_speed']['score'] * weights['recovery_speed']:.1f} points"],
            ['Consistency', f"{weights['consistency']:.0%}", 
             f"{self.rq_data['domains']['consistency']['value'] * weights['consistency']:.1f} points"],
            ['Adaptability', f"{weights['adaptability']:.0%}", 
             f"{(50 + self.rq_data['domains']['adaptability']['value'] * 5) * weights['adaptability']:.1f} points"],
            ['Load Tolerance', f"{weights['load_tolerance']:.0%}", 
             f"{(self.rq_data['domains']['load_tolerance']['value'] / 50 * 100) * weights['load_tolerance']:.1f} points"],
        ]
        
        contrib_table = Table(contributions, colWidths=[2*inch, 1.5*inch, 2*inch])
        contrib_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#f1f5f9')),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 9),
            ('TEXTCOLOR', (0, 0), (-1, -1), colors.HexColor('#1e293b')),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#cbd5e1')),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8fafc')]),
            ('TOPPADDING', (0, 0), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ]))
        elements.append(contrib_table)
        elements.append(Spacer(1, 0.2*inch))
        
        # Update Frequency & Confidence
        elements.append(Paragraph("<b>Update Frequency & Confidence:</b>", self.styles['BodyText']))
        update_text = f"""
        • <b>Calculation Frequency:</b> Daily (with 5-minute variation updates)<br/>
        • <b>Weight Adaptation:</b> Weekly personalization<br/>
        • <b>Current Confidence:</b> {self.rq_data['confidence']:.1%}<br/>
        • <b>Data Quality:</b> Based on {len(self.trend_data)} days of tracking
        """
        elements.append(Paragraph(update_text, self.styles['BodyText']))
        elements.append(Spacer(1, 0.2*inch))
        
        # Footer
        footer_text = f"""
        <i>Report generated on {datetime.now().strftime('%B %d, %Y at %I:%M %p')} | 
        Resilience Quotient™ v2.0 | For research and educational purposes only</i>
        """
        elements.append(Paragraph(footer_text, self.styles['Disclaimer']))
        
        return elements


def generate_rq_pdf_report(rq_data, trend_data, stress_events):
    """
    Convenience function to generate RQ PDF report.
    
    Args:
        rq_data: RQ calculation results
        trend_data: Trend data points
        stress_events: Stress response events
    
    Returns:
        BytesIO buffer with PDF content
    """
    exporter = RQPDFExporter(rq_data, trend_data, stress_events)
    return exporter.generate_pdf()
