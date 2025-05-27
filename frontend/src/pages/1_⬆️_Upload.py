import requests
import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Upload Video")

API_URL = "http://backend:8000"

st.write(
    ":hourglass_flowing_sand: **Note:** Video processing and translation may take several minutes due to on-premises processing. Please be patient after submitting your video."
)

with st.form("upload_form", clear_on_submit=True):
    video = st.file_uploader(
        "Upload a video file", type=["mp4", "avi", "mov", "mpeg4"]
    )
    target_language = st.selectbox(
        "Select target language",
        ["None", "English", "Spanish", "French", "German"],
    )
    submit_button = st.form_submit_button("Upload and Translate")

if submit_button and video:
    with st.spinner("Uploading and processing video..."):
        try:
            file = {"file": video}
            data = {
                "target_language": target_language,
            }
            response = requests.post(
                f"{API_URL}/v1/upload/", files=file, data=data
            )
            response.raise_for_status()

            result = response.json()
            st.balloons()
            st.success(result["message"])

        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {str(e)}")
