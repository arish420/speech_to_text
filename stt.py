import streamlit as st
import os
from groq import Groq
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

sheet_id = '1R01qyrYpZn9CUtSGiI0IWysXwY7yP-jKo7YZ4xhu1uE' # replace with your sheet's ID
url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
df_groq=pd.read_csv(url)


# https://docs.google.com/spreadsheets/d/1R01qyrYpZn9CUtSGiI0IWysXwY7yP-jKo7YZ4xhu1uE/edit?gid=0#gid=0

os.environ["GROQ_API_KEY"] =  df_groq.keys()[0]



st.title("Speech to Text AI")

client = Groq()
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

if uploaded_file:

    st.audio(uploaded_file, format=uploaded_file.type)
    # Save the uploaded file temporarily
    with open("temp_audio_input." + uploaded_file.name.split(".")[-1], "wb") as f:
        f.write(uploaded_file.getbuffer())
    input_filepath = "temp_audio_input." + uploaded_file.name.split(".")[-1]

  
    with open(input_filepath, "rb") as file:
          transcription = client.audio.transcriptions.create(
          file=(input_filepath, file.read()),
          model="whisper-large-v3",
          language="ur",
          response_format="verbose_json",)
          st.write(transcription.text)
      





















