"""
Resilience Science Portal
Learn the science behind biometrics, HRV, AI, and the symbiotic relationship between mind and body
"""
import streamlit as st

def render_educational_portal_page():
    st.markdown('<div style="text-align: center; margin-bottom: 30px;"><div style="color: #a78bfa; font-size: 2.5rem; margin-bottom: 10px;">🎓</div><h2 style="color: #a78bfa;">Resilience Science Portal</h2><p style="color: #94a3b8;">Learn the science behind biometrics, HRV, AI, and the symbiotic relationship between mind and body</p></div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📚 Basics", "💓 Biometrics", "🤖 AI & Data", "🎯 Applications"])
    
    with tab1:
        render_basics_tab()
    
    with tab2:
        render_biometrics_tab()
    
    with tab3:
        render_ai_data_tab()
    
    with tab4:
        render_applications_tab()


def render_basics_tab():
    st.markdown('<h3 style="color: #a78bfa; margin-top: 20px;">Your Learning Progress</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">4 of 10 lessons completed</p>', unsafe_allow_html=True)
    
    # What is Resilience?
    with st.expander("📖 **What is Resilience?** - Understanding the neuroscience of stress recovery and adaptation", expanded=False):
        st.markdown("""
        <div style="color: #cbd5e1; line-height: 1.8;">
        <strong style="color: #10b981;">Resilience</strong> is your body's ability to recover from stress and adapt to challenges. It's not about avoiding stress—it's about bouncing back stronger.
        
        <div style="margin-top: 16px; padding: 16px; background: rgba(16, 185, 129, 0.1); border-left: 3px solid #10b981; border-radius: 4px;">
        <strong style="color: #10b981;">Key Concepts:</strong><br>
        • <strong>Homeostasis:</strong> Your body's natural balance<br>
        • <strong>Allostatic Load:</strong> Cumulative stress burden<br>
        • <strong>Vagal Tone:</strong> Parasympathetic nervous system activity<br>
        • <strong>Neuroplasticity:</strong> Your brain's ability to rewire itself
        </div>
        
        <div style="margin-top: 16px;">
        The <strong style="color: #06b6d4;">Symbiome Resilience Scale (SRS)</strong> measures your capacity to handle stress based on real-time physiological data—not just how you feel, but what your body is actually experiencing.
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Read in Depth", key="read_resilience"):
            st.info("Full article: Understanding Resilience - A Neuroscience Perspective")
    
    # Understanding SRS
    with st.expander("📊 **Understanding the Symbiome Resilience Scale (SRS)** - How we quantify your stress resilience", expanded=False):
        st.markdown("""
        <div style="color: #cbd5e1; line-height: 1.8;">
        The <strong style="color: #06b6d4;">SRS</strong> is a composite score (0-100) that combines multiple physiological signals to give you a single, actionable resilience metric.
        
        <div style="margin-top: 16px; padding: 16px; background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; border-radius: 4px;">
        <strong style="color: #f59e0b;">Formula Breakdown:</strong><br>
        <code style="color: #10b981;">SRS = (0.5 × HRV) + (0.3 × GSR) + (0.2 × Recovery)</code><br><br>
        
        <strong>HRV (Heart Rate Variability):</strong> Time variation between heartbeats (higher = better)<br>
        <strong>GSR (Galvanic Skin Response):</strong> Skin conductance (lower = calmer)<br>
        <strong>Recovery:</strong> How quickly you return to baseline after stress
        </div>
        
        <div style="margin-top: 16px;">
        <strong style="color: #06b6d4;">Score Interpretation:</strong><br>
        • <span style="color: #10b981;">70-100:</span> High resilience (green zone)<br>
        • <span style="color: #f59e0b;">40-69:</span> Moderate resilience (yellow zone)<br>
        • <span style="color: #ef4444;">0-39:</span> Low resilience (red zone - needs intervention)
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Read in Depth", key="read_srs"):
            st.info("Full article: The Science Behind the Symbiome Resilience Scale")
    
    # Gut-Brain Axis
    with st.expander("🦠 **Your Gut-Brain Axis** - The microbiome-stress connection", expanded=False):
        st.markdown("""
        <div style="color: #cbd5e1; line-height: 1.8;">
        Your gut and brain are in constant communication via the <strong style="color: #a78bfa;">vagus nerve</strong>. The trillions of bacteria in your gut (your microbiome) directly influence your stress response, mood, and resilience.
        
        <div style="margin-top: 16px; padding: 16px; background: rgba(139, 92, 246, 0.1); border-left: 3px solid #a78bfa; border-radius: 4px;">
        <strong style="color: #a78bfa;">Key Points:</strong><br>
        • <strong>Microbiome Diversity:</strong> More bacterial species = better stress resilience<br>
        • <strong>SCFA Production:</strong> Gut bacteria produce short-chain fatty acids that regulate inflammation<br>
        • <strong>Serotonin Synthesis:</strong> 90% of your serotonin is made in your gut<br>
        • <strong>Vagal Stimulation:</strong> Deep breathing activates the vagus nerve, calming both gut and brain
        </div>
        
        <div style="margin-top: 16px;">
        This is why diet, sleep, and stress management aren't separate—they're all part of the same <strong style="color: #10b981;">symbiotic system</strong>.
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Read in Depth", key="read_gut"):
            st.info("Full article: The Gut-Brain Axis and Resilience")
    
    # Did You Know?
    st.markdown('<h4 style="color: #f59e0b; margin-top: 30px;">💡 Did You Know?</h4>', unsafe_allow_html=True)
    
    facts = [
        ("Breathing HRV can raise your HRV within 10 minutes", "Deep, slow breathing (5-6 breaths/min) activates the parasympathetic nervous system."),
        ("Blue light after 9 PM can disrupt HRV by 15%", "Screen exposure suppresses melatonin and disrupts circadian rhythms."),
        ("Your gut produces more neurotransmitters than your brain", "The enteric nervous system is often called the 'second brain.'"),
        ("5 minutes of coherent breathing can lower stress by 30%", "Rhythmic breathing synchronizes heart, brain, and respiratory systems.")
    ]
    
    for title, desc in facts:
        st.markdown(f'<div style="background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; padding: 12px; margin: 10px 0; border-radius: 4px;"><div style="color: #f59e0b; font-weight: 700; font-size: 0.9rem;">💡 {title}</div><div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 6px;">{desc}</div></div>', unsafe_allow_html=True)


def render_biometrics_tab():
    st.markdown('<h3 style="color: #a78bfa; margin-top: 20px;">Your Learning Progress</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">2 of 10 lessons completed</p>', unsafe_allow_html=True)
    
    # HRV Explained
    with st.expander("💓 **Heart Rate Variability (HRV) Explained** - The gold standard for resilience measurement", expanded=False):
        st.markdown("""
        <div style="color: #cbd5e1; line-height: 1.8;">
        <strong style="color: #ef4444;">HRV</strong> measures the time variation between consecutive heartbeats. Counterintuitively, <strong>higher variability = better health</strong>.
        
        <div style="margin-top: 16px; padding: 16px; background: rgba(239, 68, 68, 0.1); border-left: 3px solid #ef4444; border-radius: 4px;">
        <strong style="color: #ef4444;">Why It Matters:</strong><br>
        • High HRV = Your nervous system is flexible and adaptive<br>
        • Low HRV = Your body is stuck in "fight or flight" mode<br>
        • HRV predicts cardiovascular health, stress resilience, and even longevity
        </div>
        
        <div style="margin-top: 16px; display: flex; gap: 20px;">
        <div style="flex: 1; padding: 16px; background: rgba(245, 158, 11, 0.1); border-radius: 8px;">
        <strong style="color: #f59e0b;">Time Domain</strong><br>
        <code style="color: #10b981;">SDNN = Standard Deviation of NN intervals</code><br>
        <span style="color: #94a3b8; font-size: 0.85rem;">Measures overall variability</span>
        </div>
        <div style="flex: 1; padding: 16px; background: rgba(245, 158, 11, 0.1); border-radius: 8px;">
        <strong style="color: #f59e0b;">Frequency Domain</strong><br>
        <code style="color: #10b981;">LF/HF Ratio = Low Freq / High Freq power</code><br>
        <span style="color: #94a3b8; font-size: 0.85rem;">Sympathetic vs parasympathetic balance</span>
        </div>
        </div>
        
        <div style="margin-top: 16px;">
        Symbiome uses <strong style="color: #06b6d4;">photoplethysmography (PPG)</strong> to measure HRV non-invasively through your fingertip. The same technology used in medical-grade pulse oximeters.
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Read in Depth", key="read_hrv"):
            st.info("Full article: Heart Rate Variability - The Ultimate Resilience Biomarker")
    
    # GSR Explained
    with st.expander("⚡ **Galvanic Skin Response (GSR)** - Measuring emotional arousal through skin conductance", expanded=False):
        st.markdown("""
        <div style="color: #cbd5e1; line-height: 1.8;">
        <strong style="color: #06b6d4;">GSR</strong> (also called electrodermal activity) measures how well your skin conducts electricity—which changes based on sweat gland activity controlled by your sympathetic nervous system.
        
        <div style="margin-top: 16px; padding: 16px; background: rgba(6, 182, 212, 0.1); border-left: 3px solid #06b6d4; border-radius: 4px;">
        <strong style="color: #06b6d4;">How It Works:</strong><br>
        • Stress triggers sweat gland activation (even if you don't feel sweaty)<br>
        • More sweat = higher skin conductance = higher GSR<br>
        • GSR responds within 1-3 seconds of emotional stimulus<br>
        • Used in lie detection, psychology research, and stress monitoring
        </div>
        
        <div style="margin-top: 16px;">
        <strong style="color: #10b981;">Applications:</strong><br>
        • <strong>Stress Detection:</strong> Instant feedback on emotional arousal<br>
        • <strong>Biofeedback Training:</strong> Learn to control your stress response<br>
        • <strong>Sleep Quality:</strong> Low GSR during sleep = deeper rest<br>
        • <strong>Cognitive Load:</strong> Mental effort increases GSR
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Read in Depth", key="read_gsr"):
            st.info("Full article: Galvanic Skin Response and Stress Measurement")
    
    # Did You Know?
    st.markdown('<h4 style="color: #f59e0b; margin-top: 30px;">💡 Did You Know?</h4>', unsafe_allow_html=True)
    
    facts = [
        ("Elite athletes have HRV scores 2-3x higher than average", "Training increases vagal tone and parasympathetic dominance."),
        ("Your HRV is highest when you first wake up", "Morning HRV reflects overnight recovery and readiness for the day."),
        ("Chronic stress can lower HRV by 40% in just 2 weeks", "Sustained cortisol exposure reduces heart rate variability.")
    ]
    
    for title, desc in facts:
        st.markdown(f'<div style="background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; padding: 12px; margin: 10px 0; border-radius: 4px;"><div style="color: #f59e0b; font-weight: 700; font-size: 0.9rem;">💡 {title}</div><div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 6px;">{desc}</div></div>', unsafe_allow_html=True)


def render_ai_data_tab():
    st.markdown('<h3 style="color: #a78bfa; margin-top: 20px;">Your Learning Progress</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">1 of 10 lessons completed</p>', unsafe_allow_html=True)
    
    # Digital Twin Model
    with st.expander("🤖 **Your Digital Twin Model** - AI-powered stress prediction and personalized interventions", expanded=False):
        st.markdown("""
        <div style="color: #cbd5e1; line-height: 1.8;">
        Your <strong style="color: #a78bfa;">Digital Twin</strong> is an AI model trained exclusively on YOUR data. It learns your unique stress patterns, recovery dynamics, and resilience capacity.
        
        <div style="margin-top: 16px; padding: 16px; background: linear-gradient(135deg, rgba(139, 92, 246, 0.15) 0%, rgba(99, 102, 241, 0.1) 100%); border-radius: 12px;">
        <strong style="color: #a78bfa; font-size: 1.1rem;">How It Works:</strong><br><br>
        
        <div style="margin-bottom: 12px;">
        <strong style="color: #10b981;">1. Capture your physiological fingerprint:</strong><br>
        <span style="color: #94a3b8; font-size: 0.85rem;">HRV patterns, GSR reactivity, recovery speed, circadian rhythms</span>
        </div>
        
        <div style="margin-bottom: 12px;">
        <strong style="color: #10b981;">2. Identify your stress triggers:</strong><br>
        <span style="color: #94a3b8; font-size: 0.85rem;">Environmental factors, social interactions, cognitive load, sleep debt</span>
        </div>
        
        <div style="margin-bottom: 12px;">
        <strong style="color: #10b981;">3. Predict future vulnerability:</strong><br>
        <span style="color: #94a3b8; font-size: 0.85rem;">48-hour stress forecast based on your historical patterns and upcoming schedule</span>
        </div>
        
        <div>
        <strong style="color: #10b981;">4. Recommend personalized interventions:</strong><br>
        <span style="color: #94a3b8; font-size: 0.85rem;">Breathing exercises, music therapy, optimal sleep timing, nutrition adjustments</span>
        </div>
        </div>
        
        <div style="margin-top: 16px; padding: 12px; background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; border-radius: 4px;">
        <strong style="color: #f59e0b;">Privacy-First AI:</strong><br>
        <span style="color: #cbd5e1; font-size: 0.85rem;">Your Digital Twin runs entirely on your device. No data leaves your phone. You own your model 100%.</span>
        </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("📚 Read in Depth", key="read_twin"):
            st.info("Full article: Digital Twin Technology for Personalized Health")
    
    # Did You Know?
    st.markdown('<h4 style="color: #f59e0b; margin-top: 30px;">💡 Did You Know?</h4>', unsafe_allow_html=True)
    
    facts = [
        ("AI can predict stress spikes 2 hours before you feel them", "Machine learning models detect subtle physiological changes invisible to conscious awareness."),
        ("Your Digital Twin improves accuracy by 15% every month", "Continuous learning from your data makes predictions increasingly personalized.")
    ]
    
    for title, desc in facts:
        st.markdown(f'<div style="background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; padding: 12px; margin: 10px 0; border-radius: 4px;"><div style="color: #f59e0b; font-weight: 700; font-size: 0.9rem;">💡 {title}</div><div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 6px;">{desc}</div></div>', unsafe_allow_html=True)


def render_applications_tab():
    st.markdown('<h3 style="color: #a78bfa; margin-top: 20px;">Your Learning Progress</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem;">0 of 10 lessons completed</p>', unsafe_allow_html=True)
    
    # Real-World Applications
    st.markdown("""
    <div style="color: #cbd5e1; line-height: 1.8; margin-top: 20px;">
    <h4 style="color: #06b6d4;">🎯 Real-World Applications</h4>
    
    <div style="margin-top: 20px; padding: 20px; background: rgba(30, 41, 59, 0.8); border-radius: 12px;">
    <strong style="color: #10b981; font-size: 1.1rem;">For Students:</strong><br>
    <div style="margin-top: 12px; color: #94a3b8; font-size: 0.9rem; line-height: 1.8;">
    • Optimize study schedules based on cognitive resilience<br>
    • Reduce exam anxiety through biofeedback training<br>
    • Improve sleep quality and academic performance<br>
    • Build long-term stress management skills
    </div>
    </div>
    
    <div style="margin-top: 20px; padding: 20px; background: rgba(30, 41, 59, 0.8); border-radius: 12px;">
    <strong style="color: #06b6d4; font-size: 1.1rem;">For Professionals:</strong><br>
    <div style="margin-top: 12px; color: #94a3b8; font-size: 0.9rem; line-height: 1.8;">
    • Prevent burnout through early stress detection<br>
    • Optimize work-life balance with data-driven insights<br>
    • Improve focus and productivity during peak hours<br>
    • Track recovery from work-related stress
    </div>
    </div>
    
    <div style="margin-top: 20px; padding: 20px; background: rgba(30, 41, 59, 0.8); border-radius: 12px;">
    <strong style="color: #a78bfa; font-size: 1.1rem;">For Athletes:</strong><br>
    <div style="margin-top: 12px; color: #94a3b8; font-size: 0.9rem; line-height: 1.8;">
    • Monitor training load and recovery status<br>
    • Prevent overtraining syndrome<br>
    • Optimize performance through HRV-guided training<br>
    • Track mental resilience alongside physical fitness
    </div>
    </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Did You Know?
    st.markdown('<h4 style="color: #f59e0b; margin-top: 30px;">💡 Did You Know?</h4>', unsafe_allow_html=True)
    
    facts = [
        ("Schools using HRV training see 20% reduction in student anxiety", "Biofeedback interventions improve emotional regulation and academic outcomes."),
        ("Companies with wellness programs report 25% lower absenteeism", "Proactive stress management reduces sick days and healthcare costs."),
        ("Athletes using HRV-guided training reduce injury risk by 30%", "Monitoring recovery prevents overtraining and optimizes performance.")
    ]
    
    for title, desc in facts:
        st.markdown(f'<div style="background: rgba(245, 158, 11, 0.1); border-left: 3px solid #f59e0b; padding: 12px; margin: 10px 0; border-radius: 4px;"><div style="color: #f59e0b; font-weight: 700; font-size: 0.9rem;">💡 {title}</div><div style="color: #cbd5e1; font-size: 0.85rem; margin-top: 6px;">{desc}</div></div>', unsafe_allow_html=True)
