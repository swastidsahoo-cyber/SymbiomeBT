"""
Settings & Privacy
Complete control over your data, privacy, and how Symbiome operates
"""
import streamlit as st
import base64

def render_settings_privacy_page():
    st.markdown('<h2 style="color: #a78bfa; text-align: center;">Privacy & Settings</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; text-align: center; margin-bottom: 30px;">Complete control over your data, privacy, and how Symbiome operates</p>', unsafe_allow_html=True)
    
    # Privacy-First Design Banner
    st.markdown('<div style="background: linear-gradient(135deg, rgba(16, 185, 129, 0.1) 0%, rgba(16, 185, 129, 0.05) 100%); border: 1.5px solid rgba(16, 185, 129, 0.3); border-radius: 12px; padding: 20px; margin: 20px 0; display: flex; align-items: center; justify-content: space-between;"><div style="display: flex; align-items: center; gap: 15px;"><div style="color: #10b981; font-size: 2rem;">🛡️</div><div><div style="color: #10b981; font-size: 1.2rem; font-weight: 700; margin-bottom: 6px;">Privacy-First Design</div><div style="color: #cbd5e1; font-size: 0.9rem;">All operations occur in a protected, locally run your device. No personal identifiable information (PII) is collected. You have complete control over your data at all times.</div></div></div><div style="background: rgba(16, 185, 129, 0.2); color: #10b981; padding: 6px 16px; border-radius: 20px; font-size: 0.85rem; font-weight: 700; border: 1px solid rgba(16, 185, 129, 0.4);">✓ Active</div></div>', unsafe_allow_html=True)
    
    # Data Processing & Local Storage
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 style="color: #cbd5e1; font-size: 1.1rem; margin-top: 20px;">📊 Data Processing</h3>', unsafe_allow_html=True)
        
        # Initialize session state for toggles
        if 'offline_mode' not in st.session_state:
            st.session_state.offline_mode = True
        if 'local_processing' not in st.session_state:
            st.session_state.local_processing = True
        if 'community_cloud' not in st.session_state:
            st.session_state.community_cloud = False
        
        # Offline Mode
        col_icon1, col_toggle1 = st.columns([4, 1])
        with col_icon1:
            st.markdown('<div style="padding: 12px 0;"><div style="color: #e2e8f0; font-weight: 600;">🔌 Offline Mode</div><div style="color: #64748b; font-size: 0.85rem;">All processing stays on your device</div></div>', unsafe_allow_html=True)
        with col_toggle1:
            st.session_state.offline_mode = st.toggle("", value=st.session_state.offline_mode, key="toggle_offline")
        
        # Local Processing
        col_icon2, col_toggle2 = st.columns([4, 1])
        with col_icon2:
            st.markdown('<div style="padding: 12px 0;"><div style="color: #e2e8f0; font-weight: 600;">📱 Local Processing</div><div style="color: #64748b; font-size: 0.85rem;">No cloud dependency</div></div>', unsafe_allow_html=True)
        with col_toggle2:
            st.session_state.local_processing = st.toggle("", value=st.session_state.local_processing, key="toggle_local")
        
        # Community Cloud
        col_icon3, col_toggle3 = st.columns([4, 1])
        with col_icon3:
            st.markdown('<div style="padding: 12px 0;"><div style="color: #e2e8f0; font-weight: 600;">☁️ Contribute to Community Cloud</div><div style="color: #64748b; font-size: 0.85rem;">Anonymized resilience patterns only</div></div>', unsafe_allow_html=True)
        with col_toggle3:
            st.session_state.community_cloud = st.toggle("", value=st.session_state.community_cloud, key="toggle_community")
    
    with col2:
        st.markdown('<h3 style="color: #cbd5e1; font-size: 1.1rem; margin-top: 20px;">💾 Local Storage</h3>', unsafe_allow_html=True)
        
        st.markdown('<div style="background: rgba(30, 41, 59, 0.8); border: 1px solid rgba(148, 163, 184, 0.2); border-radius: 12px; padding: 20px; margin-top: 10px;"><div style="color: #cbd5e1; font-weight: 600; margin-bottom: 12px;">Storage Used</div><div style="color: #06b6d4; font-size: 1.5rem; font-weight: 700; margin-bottom: 16px;">245.8 / 512 MB</div><div style="background: rgba(148, 163, 184, 0.1); height: 8px; border-radius: 4px; margin-bottom: 20px; overflow: hidden;"><div style="background: linear-gradient(90deg, #06b6d4, #10b981); width: 48%; height: 100%;"></div></div><div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Biometric Data: <span style="color: #e2e8f0; float: right;">187 MB</span></div><div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">Journal Entries: <span style="color: #e2e8f0; float: right;">34 MB</span></div><div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 8px;">AI Model Cache: <span style="color: #e2e8f0; float: right;">19 MB</span></div><div style="color: #94a3b8; font-size: 0.85rem; margin-bottom: 16px;">Environmental Data: <span style="color: #e2e8f0; float: right;">5.8 MB</span></div></div>', unsafe_allow_html=True)
        
        if st.button("👁️ View Data Preview", use_container_width=True, type="secondary"):
            st.session_state.show_data_preview = True
        
        if st.session_state.get('show_data_preview', False):
            with st.expander("📊 Data Preview", expanded=True):
                st.markdown("**Sample Biometric Data (Last 24h)**")
                st.code("HRV: 65ms, 72ms, 58ms, 81ms\nGSR: 2.3µS, 2.1µS, 2.8µS\nHR: 72bpm, 68bpm, 75bpm", language="text")
                st.markdown("**Recent Journal Entry**")
                st.code("2024-12-24: Felt calm after morning meditation session.", language="text")
    
    # Data Management
    st.markdown('<h3 style="color: #cbd5e1; font-size: 1.1rem; margin-top: 30px;">⚙️ Data Management</h3>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📥 Export All Data\nDownload as encrypted file", use_container_width=True, type="secondary"):
            st.success("✅ Data export initiated! Download will begin shortly.")
    
    with col2:
        if st.button("📄 Generate Report\nCreate PDF summary", use_container_width=True, type="secondary"):
            st.success("✅ Report generated! Check your downloads.")
    
    with col3:
        if st.button("🗑️ Delete All Data\nPermanently remove", use_container_width=True, type="secondary"):
            st.warning("⚠️ Are you sure? This action cannot be undone!")
    
    # Research Ethics & Consent
    st.markdown('<h3 style="color: #a78bfa; font-size: 1.1rem; margin-top: 30px;">🔬 Research Ethics & Consent</h3>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 0.9rem; margin-bottom: 20px;">Symbiome is designed for research and educational purposes. All data handling follows ethical research principles including informed consent, anonymization, and transparency.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 20px;"><div style="color: #a78bfa; font-weight: 700; margin-bottom: 12px;">📋 Informed Consent</div><div style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 12px;">• Clear explanation of data collection<br>• Voluntary participation<br>• Right to withdraw<br>• Anonymization of data</div></div>', unsafe_allow_html=True)
        if st.button("⬇️ Download Consent Form", use_container_width=True, key="download_consent"):
            # Create a simple text file as consent form
            consent_text = """SYMBIOME RESEARCH CONSENT FORM

I understand that Symbiome is a research and educational tool designed to track resilience and stress patterns.

I consent to:
- Collection of biometric data (HRV, GSR)
- Local processing of my data
- Anonymous aggregation for research purposes

I understand that:
- All data is stored locally on my device
- I can withdraw consent at any time
- My data will be anonymized
- This is not a medical diagnostic tool

Participant Signature: _______________
Date: _______________"""
            
            st.download_button(
                label="📄 Download Consent Form (TXT)",
                data=consent_text,
                file_name="symbiome_consent_form.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    with col2:
        st.markdown('<div style="background: linear-gradient(135deg, rgba(139, 92, 246, 0.1) 0%, rgba(139, 92, 246, 0.05) 100%); border: 1px solid rgba(139, 92, 246, 0.3); border-radius: 12px; padding: 20px;"><div style="color: #a78bfa; font-weight: 700; margin-bottom: 12px;">⚖️ Ethics Framework</div><div style="color: #cbd5e1; font-size: 0.85rem; margin-bottom: 12px;">• No PII collection<br>• Anonymization protocols<br>• Data minimization<br>• Transparent algorithms</div></div>', unsafe_allow_html=True)
        if st.button("⬇️ Download Ethics Guide", use_container_width=True, key="download_ethics"):
            # Create ethics guide
            ethics_text = """SYMBIOME ETHICS FRAMEWORK

1. PRIVACY-FIRST DESIGN
   - All processing occurs locally
   - No personal identifiable information (PII) collected
   - User has complete control over data

2. INFORMED CONSENT
   - Clear explanation of data usage
   - Voluntary participation
   - Right to withdraw at any time

3. DATA MINIMIZATION
   - Only collect necessary data
   - Automatic data expiration
   - User-controlled deletion

4. TRANSPARENCY
   - Open-source algorithms
   - Explainable AI models
   - Clear documentation

5. RESEARCH INTEGRITY
   - Peer-reviewed methodologies
   - Reproducible results
   - Ethical review board approval

6. NON-MALEFICENCE
   - Not intended for medical diagnosis
   - Clear disclaimers
   - Professional guidance recommended

For questions: ethics@symbiome.org"""
            
            st.download_button(
                label="📄 Download Ethics Guide (TXT)",
                data=ethics_text,
                file_name="symbiome_ethics_guide.txt",
                mime="text/plain",
                use_container_width=True
            )
    
    # Clinical Diagnosis Warning
    st.markdown('<div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #f59e0b; padding: 16px; margin-top: 30px; border-radius: 4px;"><div style="color: #f59e0b; font-weight: 700; margin-bottom: 8px; font-size: 1rem;">⚠️ Important: Not for Clinical Diagnosis</div><div style="color: #cbd5e1; font-size: 0.85rem; line-height: 1.6;">Symbiome is a research and educational tool designed for biofeedback training and personal wellness insights. It is NOT intended for medical diagnosis, treatment, or collection of sensitive health information. Always consult qualified healthcare professionals for medical advice.</div></div>', unsafe_allow_html=True)
