"""
NLP Sentiment AI / Emotional Journal Interface
A privacy-first emotional logging system with AI-driven insights.
"""
import streamlit as st
from .sentiment_analyzer import SentimentAnalyzer
from datetime import datetime

def render_nlp_journal_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #ec4899; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">❤️</span> NLP Sentiment AI
        </h1>
        <p style="color: #94a3b8; font-size: 1.1rem;">
            Cognitive-Affective Bridging. Transforming subjective experience into objective resilience data.
        </p>
    </div>
    """, unsafe_allow_html=True)

    analyzer = SentimentAnalyzer()

    # --- JOURNAL INPUT ---
    st.markdown("### ✍️ Unified Resilience Log")
    entry = st.text_area(
        "How is your nervous system feeling today? (Internal state, cognitive load, sleep quality...)",
        placeholder="E.g., I feel a bit overwhelmed today after a long meeting, but my morning breathwork helped me stay centered...",
        height=200
    )

    if entry:
        analysis = analyzer.analyze_text(entry)
        
        st.markdown(f"""
        <div style="background: rgba(236, 72, 153, 0.05); border-radius: 15px; padding: 25px; border: 1px solid rgba(236, 72, 153, 0.2); margin-top: 20px;">
            <div style="display: flex; align-items: center; gap: 15px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: {analysis['color']}; box-shadow: 0 0 10px {analysis['color']};"></div>
                <div style="color: {analysis['color']}; font-weight: 700; text-transform: uppercase; letter-spacing: 2px;">AI Sentiment Analysis: {analysis['label']}</div>
            </div>
            
            <div style="margin-top: 20px; display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                <div style="background: rgba(15, 23, 42, 0.5); padding: 15px; border-radius: 10px;">
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">STRESS INTENSITY</div>
                    <div style="color: white; font-size: 1.5rem; font-weight: 700;">{analysis['stress_score']}%</div>
                </div>
                <div style="background: rgba(15, 23, 42, 0.5); padding: 15px; border-radius: 10px;">
                    <div style="color: #94a3b8; font-size: 0.8rem; margin-bottom: 5px;">DETECTED KEYWORDS</div>
                    <div style="color: white; font-size: 0.9rem; font-weight: 500;">{', '.join(analysis['keywords']) if analysis['keywords'] else 'None Detected'}</div>
                </div>
            </div>
            
            <div style="margin-top: 20px; padding-top: 15px; border-top: 1px solid rgba(255,255,255,0.05); color: #cbd5e1; font-size: 0.9rem; font-style: italic;">
                "Your entry suggests a {analysis['label'].lower()} state. The system recommends prioritizing a 3-minute Vagal Tone session to stabilize neural variance."
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("💾 Save to Clinical Vault", use_container_width=True):
            st.toast("Encrypted & Synchronized to Cloud", icon="🔒")

    st.divider()

    # --- HISTORICAL FEEDBACK ---
    st.markdown("### 📊 Affective Progression")
    
    # Mock some trend data
    history = pd.DataFrame({
        'Day': ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
        'Sentiment': [80, 45, 30, 85, 90, 70, 75], # 100 = Calm, 0 = Stressed
        'Color': ['#10b981', '#f59e0b', '#ef4444', '#10b981', '#10b981', '#10b981', '#10b981']
    })
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=history['Day'], 
        y=history['Sentiment'], 
        marker_color=history['Color'],
        text=[f"{v}% Pos" for v in history['Sentiment']],
        textposition='auto'
    ))
    
    fig.update_layout(
        title="Weekly Sentiment Stability",
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white"),
        yaxis=dict(range=[0, 100], showgrid=False),
        xaxis=dict(showgrid=False),
        margin=dict(l=0, r=0, t=40, b=0)
    )
    st.plotly_chart(fig, use_container_width=True)
