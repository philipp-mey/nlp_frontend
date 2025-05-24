import requests
import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Library")

API_URL = "http://backend:8000/v1"
MEDIA_URL = "http://localhost:8000/media/"

st.write(
    "Welcome to your video library! Here you can manage your videos, view subtitles, and more."
)

try:
    response = requests.get(f"{API_URL}/videos/")
    response.raise_for_status()
    videos = response.json().get("videos", [])

    if not videos:
        st.info("No videos found. Upload a video on the Upload page.")
    else:
        for video in videos:
            video_name = video.get("name", "Unnamed")
            with st.expander(f"{video_name}", expanded=False):
                video_url = f"{MEDIA_URL}{video_name}"
                st.video(data=video_url)

                st.markdown(
                    f"**Language:** {video.get('language', 'unknown')}"
                )
                st.markdown("**Original Subtitles:**")
                st.code(video.get("original_text", ""))
                st.markdown("**Translated Subtitles:**")
                st.code(video.get("translated_text", ""))

                if video.get("translated_srt_url"):
                    srt_url = f"{MEDIA_URL}{video['translated_srt_url']}"
                    st.download_button(
                        "Download translated subtitles (.srt)",
                        data=requests.get(srt_url).content,
                        file_name=f"{video_name}.srt",
                    )
except Exception as e:
    st.error(f"An error occurred while fetching videos: {e}")
