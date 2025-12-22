"""
Settings & Privacy Interface.
Centralized control for user profiles, data preference, and security.
"""
import streamlit as st

def render_settings_privacy_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #94a3b8; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">⚙️</span> Settings & Privacy
        </h1>
        <p style="color: #64748b; font-size: 1.1rem;">
            Control Center. Manage your autonomic identity and data sovereignty.
        </p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["👤 Profile", "🔒 Privacy & Data", "🎨 Appearance"])

    with tab1:
        st.markdown("### User Profile")
        col1, col2 = st.columns(2)
        with col1:
            st.text_input("Display Name", "Bio-User 882")
            st.text_input("Email", "user@symbiome.ai")
        with col2:
            st.selectbox("Nervous System Profile", ["Sensitive (High HRV Var)", "Fortified (Elite)", "Standard"])
            st.date_input("Monitoring Since", value=None)
        
        st.button("Update Profile", use_container_width=True)

    with tab2:
        st.markdown("### Privacy Sovereignty")
        st.toggle("Enable End-to-End Encryption for Journal", value=True)
        st.toggle("Allow Zero-Knowledge Proofs for Community Leaderboards", value=False)
        st.toggle("Share Anonymized Biometrics for Global Research", value=True)
        
        st.divider()
        st.markdown("### Data Management")
        c1, c2 = st.columns(2)
        c1.button("📥 Download All Data (Encrypted)", use_container_width=True)
        c2.button("🗑️ Delete Account & Purge Data", type="primary", use_container_width=True)

    with tab3:
        st.markdown("### Interface Customization")
        st.select_slider("Haptic Feedback Intensity", options=["Off", "Subtle", "Dynamic", "Intense"], value="Dynamic")
        st.toggle("Enable Glassmorphism Glass Blur", value=True)
        st.selectbox("Theme Engine", ["Deep Space (Default)", "Clinical White", "Bio-Luminescent"])
        
    st.divider()
    
    # SYSTEM INFO
    st.markdown("""
    <div style="background: rgba(15, 23, 42, 0.5); padding: 20px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.05);">
        <div style="font-size: 0.8rem; color: #64748b;">VERSION: 2.4.0-STABLE</div>
        <div style="font-size: 0.8rem; color: #64748b;">BUILD ID: AE-99-B</div>
        <div style="font-size: 0.8rem; color: #64748b;">ENCRYPTION STATUS: VERIFIED</div>
    </div>
    """, unsafe_allow_html=True)
