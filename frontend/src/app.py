import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Welcome! Use the sidebar to navigate:")

st.markdown("""
- **Upload:** Upload and translate a new video
- **Library:** View & play your translated videos
""")

st.image("src/images/world.jpg", use_container_width=True)
