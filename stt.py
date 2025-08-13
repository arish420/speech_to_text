import streamlit as st






st.title("Speech to Text AI")


uploaded_audio = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

if uploaded_audio:
  st.write(uploaded_audio.read())
