import streamlit as st

video_url = "/Users/meyerp/Documents/DHBW/6Semester/nlp_frontend/backend/media/004a3d21-675d-4c0e-9c43-d0055b581319.mp4"
subtitle_url = "http://localhost:8000/media/processed/5a01ce63-12ff-4a3c-8535-c5872865f2d2/What%20is%20GitHub.de.srt"

st.header("Video Player with Subtitles")

st.video(data=video_url, subtitles=subtitle_url)
