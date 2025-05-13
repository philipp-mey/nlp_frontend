import requests
import streamlit as st

from frontend.utils.page_setup import set_page_layout

set_page_layout(page_title="Upload Video")


video = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov"])
target_language = st.selectbox(
    "Select target language", ["English", "Spanish", "French", "German"]
)

if video and st.button("Upload and Translate"):
    files = {"file": video}
    data = {
        "target_language": target_language,
    }
    response = requests.post(
        "http://localhost:8000/upload/", files=files, data=data
    )
    st.write(response.json())
