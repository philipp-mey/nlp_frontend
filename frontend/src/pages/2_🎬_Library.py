import os
from urllib.parse import quote

import requests
import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Library")

API_URL = "http://backend:8000/v1"
BASE_URL = "http://localhost:8000"

st.title("📚 Video Library")
st.write(
    "Browse your processed videos. Click on any video to watch it with subtitles."
)

col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🔄 Refresh"):
        st.rerun()

if "selected_video" not in st.session_state:
    st.session_state.selected_video = None

try:
    response = requests.get(f"{API_URL}/videos/")
    response.raise_for_status()
    data = response.json()
    videos = data.get("videos", [])

    if not videos:
        st.info(
            "📭 No videos found. Upload a video on the Upload page to get started!"
        )
    else:
        if st.session_state.selected_video:
            # Video player view
            video = st.session_state.selected_video
            video_id = video.get("video_id")

            if st.button("← Back to Library"):
                st.session_state.selected_video = None
                st.rerun()

            st.subheader(f"🎬 {video.get('name', 'Unnamed Video')}")

            # Get available subtitles
            available_subtitles = []
            try:
                subtitles_response = requests.get(
                    f"{API_URL}/videos/{video_id}/subtitles"
                )
                if subtitles_response.status_code == 200:
                    available_subtitles = subtitles_response.json().get(
                        "subtitles", []
                    )
            except Exception as e:
                st.error(f"Error fetching subtitles: {e}")

            col1, col2 = st.columns([3, 1])

            with col1:
                video_url = f"{BASE_URL}/media/{video.get('path')}"
                subtitle_url = f"{BASE_URL}/media/{video.get('path')}"
                if available_subtitles:
                    if len(available_subtitles) > 1:
                        subtitle_options = {
                            f"{s['language']} ({s['type']})": s
                            for s in available_subtitles
                        }
                        selected_language = st.selectbox(
                            "Select subtitle language:",
                            options=list(subtitle_options.keys()),
                        )
                        selected_subtitle = subtitle_options[selected_language]
                    else:
                        selected_subtitle = available_subtitles[0]

                    subtitle_url = (
                        f"../backend/media/{selected_subtitle['path']}"
                    )
                    if not os.path.exists(subtitle_url):
                        raise ValueError(
                            "Subtitle file does not exist on the server."
                        )
                # Video player with subtitles
                enable_subtitles = st.checkbox("Enable subtitles", value=True)

                if subtitle_url and enable_subtitles:
                    try:
                        st.video(
                            video_url,
                            subtitles=subtitle_url,
                        )
                    except Exception as e:
                        st.warning(f"Error loading subtitles: {e}")
                        st.video(video_url)
                else:
                    st.video(video_url)

            with col2:
                st.write("**Available Subtitles:**")
                if available_subtitles:
                    for subtitle in available_subtitles:
                        st.write(
                            f"🌐 {subtitle['language']} ({subtitle['type']})"
                        )
                        download_url = (
                            f"{BASE_URL}/media/{quote(subtitle['path'])}"
                        )
                        st.markdown(
                            f"[📥 Download {subtitle['language']}]({download_url})",
                            unsafe_allow_html=True,
                        )
                else:
                    st.write("No subtitles available")

                # Video info
                st.write("**Video Info:**")
                st.write(f"ID: {video_id}")
                if video.get("subtitle_count", 0) > 0:
                    st.write(f"Subtitles: {video['subtitle_count']} files")

        else:
            # Video grid view
            st.write(f"Found {len(videos)} video(s) in your library")

            # Create a responsive grid
            cols_per_row = 3
            for i in range(0, len(videos), cols_per_row):
                cols = st.columns(cols_per_row)

                for j in range(cols_per_row):
                    if i + j < len(videos):
                        video = videos[i + j]

                        with cols[j]:
                            with st.container():
                                st.markdown("---")

                                video_name = video.get("name", "Unnamed")
                                st.write(f"**{video_name}**")

                                # Show subtitle info
                                subtitle_count = video.get("subtitle_count", 0)
                                if subtitle_count > 0:
                                    st.caption(
                                        f"🌐 {subtitle_count} subtitle file(s)"
                                    )
                                else:
                                    st.caption("🚫 No subtitles")

                                # Get subtitle languages
                                try:
                                    video_id = video.get("video_id")
                                    subs_resp = requests.get(
                                        f"{API_URL}/videos/{video_id}/subtitles"
                                    )
                                    if subs_resp.status_code == 200:
                                        subs = subs_resp.json().get(
                                            "subtitles", []
                                        )
                                        if subs:
                                            languages = [
                                                s["language"] for s in subs
                                            ]
                                            st.caption(
                                                f"Languages: {', '.join(languages)}"
                                            )
                                except:
                                    pass

                                if st.button("▶️ Watch", key=f"watch_{i + j}"):
                                    st.session_state.selected_video = video
                                    st.rerun()

except requests.exceptions.RequestException as e:
    st.error(f"❌ Failed to connect to the server: {str(e)}")
    st.info("Make sure the backend server is running.")
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {str(e)}")
