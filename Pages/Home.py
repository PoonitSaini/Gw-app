import streamlit as st
import warnings
from PIL import Image

warnings.filterwarnings("ignore")

st.set_page_config(
    layout="wide"
)

# st.subheader("GW")
col1 , col2 = st.columns([0.9,1])

with col1:
    image = Image.open("Images/logo.png")
    new_image = image.resize((600, 500))  # width=600, height=400
    st.image(new_image)


with col2:
    st.markdown(
        '<p style="color:#16a085; font-size:18px;">Empowering the next generation by acquiring schools and transforming them into centers of real, practical, and purpose-driven education.</p>',
        unsafe_allow_html=True
    )

