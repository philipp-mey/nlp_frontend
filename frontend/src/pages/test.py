import streamlit as st

video_url = "/Users/meyerp/Documents/DHBW/6Semester/nlp_frontend/backend/media/004a3d21-675d-4c0e-9c43-d0055b581319.mp4"
subtitle_url = "/Users/meyerp/Documents/DHBW/6Semester/nlp_frontend/backend/media/004a3d21-675d-4c0e-9c43-d0055b581319.en.srt"

st.header("Video Player with Subtitles")

st.video(data=video_url, subtitles=subtitle_url)
