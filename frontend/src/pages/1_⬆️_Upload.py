import time

import requests
import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Upload Video")

API_URL = "http://backend:8000/v1"

st.write(
    ":hourglass_flowing_sand: **Note:** Video processing and translation may take several minutes due to on-premises processing. Please be patient after submitting your video."
)

# Language mapping for API
LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
}

with st.form("upload_form", clear_on_submit=True):
    video = st.file_uploader(
        "Upload a video file", type=["mp4", "avi", "mov", "mpeg4"]
    )
    target_language = st.selectbox(
        "Select target language",
        ["English", "Spanish", "French", "German"],
    )
    submit_button = st.form_submit_button("Upload and Translate")

if submit_button and video:
    with st.spinner("Uploading video..."):
        try:
            files = {"file": (video.name, video, video.type)}
            data = {
                "target_language": LANGUAGE_CODES[target_language],
            }
            response = requests.post(
                f"{API_URL}/upload/", files=files, data=data
            )
            response.raise_for_status()

            upload_result = response.json()
            video_id = upload_result["video_id"]
            st.success(upload_result["message"])

        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {str(e)}")
            st.stop()

    with st.spinner("Starting video processing..."):
        try:
            response = requests.post(f"{API_URL}/process/{video_id}")
            response.raise_for_status()

        except requests.exceptions.RequestException as e:
            st.error(f"Failed to start processing: {str(e)}")
            st.stop()

    progress_placeholder = st.empty()
    status_placeholder = st.empty()

    with st.spinner("Processing video..."):
        while True:
            try:
                response = requests.get(f"{API_URL}/status/{video_id}")
                response.raise_for_status()
                status_data = response.json()

                status = status_data["status"]
                status_placeholder.info(f"Status: {status}")

                if status == "completed":
                    st.balloons()
                    st.success("Video processed successfully!")

                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric(
                            "Source Language",
                            status_data.get("source_language", "N/A"),
                        )
                    with col2:
                        st.metric("Target Language", target_language)

                    if "processed_videos" not in st.session_state:
                        st.session_state.processed_videos = []
                    st.session_state.processed_videos.append(
                        {
                            "video_id": video_id,
                            "filename": video.name,
                            "source_language": status_data.get(
                                "source_language"
                            ),
                            "target_language": target_language,
                        }
                    )

                    st.info(f"Video ID: {video_id}")
                    st.info(
                        "You can download the subtitles from the Download page."
                    )
                    break

                elif status == "failed":
                    st.error("Video processing failed!")
                    break

                time.sleep(2)

            except requests.exceptions.RequestException as e:
                st.error(f"Failed to check status: {str(e)}")
                break
