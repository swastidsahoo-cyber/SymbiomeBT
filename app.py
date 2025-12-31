import streamlit as st

st.set_page_config(page_title="Symbiome Recovery", layout="centered")
st.title("✅ System Online")
st.success("The application environment has stabilized.")
st.write("We are currently in **Low-Memory Recovery Mode**.")
st.write("Heavy AI modules (DeepFace, Torch) have been temporarily disabled to prevent server crashes.")

if st.button("Check Dependencies"):
    import numpy as np
    import pandas as pd
    import cv2
    import av
    st.write("Basic modules loaded successfully!")
    st.write(f"OpenCV Version: {cv2.__version__}")
