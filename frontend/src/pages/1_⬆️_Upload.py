import time

import requests
import streamlit as st
from utils.page_setup import set_page_layout

set_page_layout(page_title="Upload Video")

API_URL = "http://backend:8000/v1"

st.write(
    ":hourglass_flowing_sand: **Note:** Video processing and translation may take several minutes due to on-premises processing. Please be patient after submitting your video."
)

# Language mapping for API (matching common language codes)
LANGUAGE_CODES = {
    "English": "en",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Portuguese": "pt",
    "Russian": "ru",
    "Japanese": "ja",
    "Korean": "ko",
    "Chinese": "zh",
    "Dutch": "nl",
    "Arabic": "ar",
    "Hindi": "hi",
}

with st.form("upload_form", clear_on_submit=True):
    video = st.file_uploader(
        "Upload a video file",
        type=["mp4", "avi", "mov", "mkv", "webm", "flv", "mpeg4"],
    )
    target_language = st.selectbox(
        "Select target language for translation",
        list(LANGUAGE_CODES.keys()),
    )
    submit_button = st.form_submit_button("Upload and Process Video")

if submit_button and video:
    # File size validation
    if video.size > 500 * 1024 * 1024:  # 500MB limit
        st.error(
            "File size too large. Please upload a video smaller than 500MB."
        )
        st.stop()

    with st.spinner("Uploading and starting video processing..."):
        try:
            files = {"video": (video.name, video.getvalue(), video.type)}
            data = {"target_lang": LANGUAGE_CODES[target_language]}

            response = requests.post(
                f"{API_URL}/upload/",
                files=files,
                data=data,
                timeout=60,
            )
            response.raise_for_status()

            upload_result = response.json()

            st.success(upload_result["message"])

            col1, col2 = st.columns(2)
            with col1:
                st.metric("Uploaded File", upload_result["filename"])
            with col2:
                st.metric("Target Language", target_language)

            if "uploaded_videos" not in st.session_state:
                st.session_state.uploaded_videos = []

            video_info = {
                "filename": upload_result["filename"],
                "saved_path": upload_result["saved_path"],
                "target_language": target_language,
                "target_lang_code": upload_result["target_lang"],
                "upload_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "status": "processing",
            }

            st.session_state.uploaded_videos.append(video_info)

            st.info("🎬 Your video is now being processed in the background!")
            st.info("📁 File saved at: " + upload_result["saved_path"])

            st.markdown("""
            ### What happens next?
            1. **Audio extraction** - Converting video to audio format
            2. **Transcription** - Generating subtitles from audio
            3. **Translation** - Translating subtitles to your target language
            4. **File generation** - Creating SRT subtitle files
            
            ### How to check your results:
            - Processing typically takes 2-10 minutes depending on video length
            - Check the **Download** page periodically for your processed files
            - Look for files with your target language code: `{upload_result["target_lang"]}`
            """)

            base_name = upload_result["filename"].rsplit(".", 1)[0]
            st.markdown("### Expected output files:")
            st.code(f"""
Original subtitles: {base_name}.srt
Translated subtitles: {base_name}.{upload_result["target_lang"]}.srt
            """)

        except requests.exceptions.Timeout:
            st.error(
                "Upload timed out. Please check your internet connection and try again."
            )

        except requests.exceptions.RequestException as e:
            st.error(f"Upload failed: {str(e)}")

            if hasattr(e, "response") and e.response is not None:
                try:
                    error_details = e.response.json()
                    if "detail" in error_details:
                        st.error(f"Server error: {error_details['detail']}")
                except:
                    st.error(
                        f"HTTP {e.response.status_code}: {e.response.text}"
                    )

        except Exception as e:
            st.error(f"An unexpected error occurred: {str(e)}")

elif submit_button and not video:
    st.warning("Please upload a video file before submitting.")


if "uploaded_videos" in st.session_state and st.session_state.uploaded_videos:
    st.subheader("Recently Uploaded Videos")

    for i, video_info in enumerate(
        reversed(st.session_state.uploaded_videos[-5:])
    ):
        with st.expander(
            f"📹 {video_info['filename']} - {video_info['upload_time']}"
        ):
            col1, col2 = st.columns(2)
            with col1:
                st.text(f"Target Language: {video_info['target_language']}")
                st.text(f"Language Code: {video_info['target_lang_code']}")
            with col2:
                st.text(f"Upload Time: {video_info['upload_time']}")
                st.text(f"Status: {video_info['status']}")

            st.text(f"Saved Path: {video_info['saved_path']}")


st.markdown("""
---
### 💡 Tips:
- **Large files** take longer to process
- **Longer videos** require more processing time
- **Clear audio** produces better transcription results
- Check the **Download** page for your processed subtitle files
- Both original and translated subtitle files will be available
""")


if st.button("🔄 Refresh Page"):
    st.rerun()
