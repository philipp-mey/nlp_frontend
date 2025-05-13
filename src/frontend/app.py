import streamlit as st

from frontend.utils.page_setup import set_page_layout

set_page_layout(page_title="Video Subtitle Translator")


st.markdown("""

Welcome! Use the sidebar to navigate:
- **Upload:** Upload and translate a new video
- **Library:** View & play your translated videos
""")
