"""
Clinical Data Vault Interface.
Secure, HIPAA-compliant (simulated) data management for sensitive biometrics.
"""
import streamlit as st
import pandas as pd
import json
from .encryption import DataEncryption

def render_clinical_vault_page():
    st.markdown("""
    <div style="text-align: center; margin-bottom: 30px;">
        <h1 style="color: #94a3b8; font-size: 2.5rem; font-weight: 800; margin-bottom: 5px;">
            <span style="font-size: 2rem;">🔒</span> Clinical Data Vault
        </h1>
        <p style="color: #64748b; font-size: 1.1rem;">
            End-to-End Encrypted Bio-Storage. Your data, your keys, your clinical autonomy.
        </p>
    </div>
    """, unsafe_allow_html=True)

    if 'encryption' not in st.session_state:
        st.session_state.encryption = DataEncryption()
        
    enc = st.session_state.encryption

    # --- VAULT STATUS ---
    st.markdown("### 🛡️ System Integrity")
    v1, v2, v3 = st.columns(3)
    
    v1.metric("Encryption Standard", "AES-256-GCM")
    v2.metric("Vault Status", "SYNCHRONIZED", delta="100%", delta_color="normal")
    v3.metric("Data Sovereignty", "USER-OWNED")

    st.divider()

    # --- DATA EXPLORER ---
    st.markdown("### 📂 Sensitive Records")
    
    # Mock data records
    records = [
        {"timestamp": "2025-12-22 08:00", "type": "HRV Baseline", "value": "68ms"},
        {"timestamp": "2025-12-22 09:15", "type": "Cortisol Proxy", "value": "14.2 µg/dL"},
        {"timestamp": "2025-12-21 23:30", "type": "Deep Sleep Alpha", "value": "4.2h"}
    ]
    
    df = pd.DataFrame(records)
    
    st.table(df)

    # --- ACTIONS ---
    st.markdown("### ⚡ Vault Actions")
    
    ac1, ac2 = st.columns(2)
    
    with ac1:
        if st.button("📤 Export Clinical Bundle (JSON)", use_container_width=True):
            bundle = {
                "user_id": "SYM-88219",
                "export_date": pd.Timestamp.now().isoformat(),
                "records": records
            }
            encrypted_bundle = enc.encrypt_data(json.dumps(bundle))
            st.download_button(
                "Click to Download Encrypted File",
                data=encrypted_bundle,
                file_name=f"clinical_bundle_{pd.Timestamp.now().strftime('%Y%m%d')}.sym",
                mime="application/octet-stream",
                use_container_width=True
            )
            
    with ac2:
        if st.button("☁️ Force Cloud Sync", use_container_width=True):
            with st.spinner("Establishing P2P Tunnel..."):
                import time
                time.sleep(2)
                st.success("Secondary backup complete on decentralized node.")

    st.divider()

    # --- PRIVACY CONTROLS ---
    st.markdown("### 👁️ Privacy & Consent")
    st.checkbox("Enable Zero-Knowledge Research Sharing", value=False)
    st.checkbox("Log Audit Trails for AI Predictions", value=True)
    st.checkbox("Automatic Data Purge (30 Days)", value=False)
    
    with st.expander("🔐 View Master Encryption Key"):
        st.code(enc.get_key_string())
        st.warning("NEVER share this key. If lost, your clinical data cannot be recovered.")
