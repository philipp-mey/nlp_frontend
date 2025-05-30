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

# Add debug mode toggle
debug_mode = st.checkbox("Show debug information")

# Initialize session state for selected video
if "selected_video" not in st.session_state:
    st.session_state.selected_video = None

try:
    response = requests.get(f"{API_URL}/videos/")
    response.raise_for_status()
    videos = response.json().get("videos", [])

    if not videos:
        st.info(
            "📭 No videos found. Upload a video on the Upload page to get started!"
        )
    else:
        if st.session_state.selected_video:
            video = st.session_state.selected_video
            video_id = video.get("video_id")

            if st.button("← Back to Library"):
                st.session_state.selected_video = None
                st.rerun()

            st.subheader(f"🎬 {video.get('name', 'Unnamed Video')}")

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

            if debug_mode:
                with st.expander("Debug Info", expanded=True):
                    st.write("Video:", video)
                    st.write("Available subtitles:", available_subtitles)

            col1, col2 = st.columns([3, 1])

            with col1:
                video_url = f"{BASE_URL}/media/{video.get('name')}"

                subtitle_url = None
                selected_subtitle = None

                if available_subtitles:
                    if len(available_subtitles) > 1:
                        subtitle_options = {
                            f"{s['language']}": s for s in available_subtitles
                        }
                        selected_language = st.selectbox(
                            "Select subtitle language:",
                            options=list(subtitle_options.keys()),
                        )
                        selected_subtitle = subtitle_options[selected_language]
                    else:
                        selected_subtitle = available_subtitles[0]

                    if selected_subtitle:
                        subtitle_url = (
                            f"{BASE_URL}/media/{selected_subtitle['filename']}"
                        )

                # Try different approaches for video with subtitles
                enable_subtitles = st.checkbox("Enable subtitles", value=True)

                if debug_mode:
                    st.code(f"Video URL: {video_url}")
                    if subtitle_url:
                        st.code(f"Subtitle URL: {subtitle_url}")

                # Approach 1: Try with subtitles if available and enabled
                if subtitle_url and enable_subtitles:
                    st.write("Playing with subtitles...")
                    try:
                        # First, let's verify the subtitle file is accessible
                        subtitle_test = requests.head(subtitle_url)
                        if subtitle_test.status_code == 200:
                            st.video(
                                data=video_url,
                                format="video/mp4",
                                subtitles=subtitle_url,
                            )
                        else:
                            st.warning(
                                f"Subtitle file not accessible (status: {subtitle_test.status_code})"
                            )
                            st.video(data=video_url, format="video/mp4")
                    except Exception as e:
                        st.error(f"Error with subtitles: {str(e)}")
                        st.info("Playing video without subtitles...")
                        st.video(data=video_url, format="video/mp4")
                else:
                    # Play without subtitles
                    st.video(data=video_url, format="video/mp4")

                # Alternative approach: Download subtitle content and save temporarily
                if (
                    enable_subtitles
                    and subtitle_url
                    and st.button("Try Alternative Subtitle Method")
                ):
                    try:
                        # Download subtitle content
                        download_url = f"http://backend:8000/media/{selected_subtitle['filename']}"
                        subtitle_content = requests.get(download_url).text

                        # Save to a temporary file
                        import os
                        import tempfile

                        with tempfile.NamedTemporaryFile(
                            mode="w", suffix=".srt", delete=False
                        ) as tmp_file:
                            tmp_file.write(subtitle_content)
                            temp_subtitle_path = tmp_file.name

                        st.info(
                            f"Temporary subtitle file created at: {temp_subtitle_path}"
                        )

                        # Try with local file path
                        st.video(
                            data=video_url,
                            format="video/mp4",
                            subtitles=temp_subtitle_path,
                        )

                        # Clean up
                        os.unlink(temp_subtitle_path)

                    except Exception as e:
                        st.error(f"Alternative method failed: {str(e)}")

            with col2:
                st.write("**Available Subtitles:**")
                if available_subtitles:
                    for subtitle in available_subtitles:
                        st.write(f"🌐 {subtitle['language']}")

                        if debug_mode:
                            test_url = (
                                f"{BASE_URL}/media/{subtitle['filename']}"
                            )
                            st.code(test_url)
                            # Test accessibility
                            try:
                                test_response = requests.head(test_url)
                                st.write(
                                    f"Status: {test_response.status_code}"
                                )
                            except:
                                st.write("Status: Failed to check")

                        try:
                            download_url = f"http://backend:8000/media/{subtitle['filename']}"
                            subtitle_content = requests.get(
                                download_url
                            ).content

                            st.download_button(
                                f"📥 Download {subtitle['language']}",
                                data=subtitle_content,
                                file_name=subtitle["filename"],
                                mime="text/plain",
                                key=f"download_{subtitle['filename']}",
                            )
                        except Exception as e:
                            st.error(
                                f"Error downloading {subtitle['language']}: {e}"
                            )
                else:
                    st.write("No subtitles available")

        else:
            # Display video grid
            st.write(f"Found {len(videos)} video(s) in your library")

            # Create a 3-column grid
            cols = st.columns(3)

            for idx, video in enumerate(videos):
                col_idx = idx % 3
                with cols[col_idx]:
                    with st.container():
                        st.write("---")

                        video_name = video.get("name", "Unnamed")
                        st.write(f"**{video_name}**")

                        video_id = video.get("video_id")
                        try:
                            subs_resp = requests.get(
                                f"{API_URL}/videos/{video_id}/subtitles"
                            )
                            if subs_resp.status_code == 200:
                                subs = subs_resp.json().get("subtitles", [])
                                if subs:
                                    languages = [s["language"] for s in subs]
                                    st.caption(
                                        f"🌐 Subtitles: {', '.join(languages)}"
                                    )
                        except:
                            pass

                        if st.button("▶️ Watch", key=f"watch_{idx}"):
                            st.session_state.selected_video = video
                            st.rerun()

                        st.write("---")

except requests.exceptions.RequestException as e:
    st.error(f"❌ Failed to connect to the server: {str(e)}")
    st.info("Make sure the backend server is running.")
except Exception as e:
    st.error(f"❌ An unexpected error occurred: {str(e)}")
