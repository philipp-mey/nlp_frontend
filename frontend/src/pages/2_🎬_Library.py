import requests
import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Library")

API_URL = "http://backend:8000"

st.title("Your Video Library")
st.write(
    "Welcome to your video library! Here you can manage your videos, view subtitles, and more."
)

try:
    response = requests.get(f"{API_URL}/v1/videos/")
    response.raise_for_status()
    videos = response.json().get("videos", [])

    if not videos:
        st.info("No videos found. Upload a video on the Upload page.")
    else:
        for video in videos:
            video_name = video.get("name", "Unnamed")
            with st.expander(f"{video_name}", expanded=False):
                # Prepend API_URL so Streamlit fetches from backend
                st.video(f"{API_URL}{video.get('video_url', '')}")
                st.markdown(
                    f"**Language:** {video.get('language', 'unknown')}"
                )
                st.markdown("**Original Subtitles:**")
                st.code(video.get("original_text", ""))
                st.markdown("**Translated Subtitles:**")
                st.code(video.get("translated_text", ""))

                if "translated_srt_url" in video:
                    # Prepend API_URL so requests fetches from backend, not local Streamlit
                    srt_url = f"{API_URL}{video['translated_srt_url']}"
                    st.download_button(
                        "Download translated subtitles (.srt)",
                        data=requests.get(srt_url).content,
                        file_name=f"{video_name}.srt",
                    )
except Exception as e:
    st.error(f"An error occurred while fetching videos: {e}")
