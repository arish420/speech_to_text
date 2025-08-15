import streamlit as st
from openai import OpenAI
import os
from groq import Groq
import pandas as pd
from dotenv import load_dotenv
import re
# Load environment variables
load_dotenv()


#groq
# https://docs.google.com/spreadsheets/d/1R01qyrYpZn9CUtSGiI0IWysXwY7yP-jKo7YZ4xhu1uE/edit?gid=0#gid=0

sheet_id = '1R01qyrYpZn9CUtSGiI0IWysXwY7yP-jKo7YZ4xhu1uE' # replace with your sheet's ID
url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
df_groq=pd.read_csv(url)


sheet_id = '150_Ht0_ecl8EwQa14sne4U_C8N0nPYoNhIpIW0dG7Mc' # replace with your sheet's ID
url=f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
df_openai=pd.read_csv(url)

#openai
#https://docs.google.com/spreadsheets/d/150_Ht0_ecl8EwQa14sne4U_C8N0nPYoNhIpIW0dG7Mc/edit?usp=sharing

os.environ["OPENAI_API_KEY"] =  df_openai.keys()[0]
os.environ["GROQ_API_KEY"] =  df_groq.keys()[0]





st.title("Speech to Text AI")
client1 = OpenAI()
client = Groq()
uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav", "ogg"])

col1, col2 = st.columns(2)
with col1:
    selection = st.selectbox("Select Output Language", ("Dutch","Spanish","French"))
with col2:
    translation_option = st.selectbox("Select Translation Option", ("Whisper","GPT-4o-transcribe"))


platform = st.selectbox("Select Platform", ("Groq","OpenAI"))


lang_dict = {"Dutch":"nl","Spanish":"es","French":"fr"}
translation_dict = {"Whisper":"whisper-1","GPT-4o-transcribe":"gpt-4o-transcribe"}

if st.button("Sumbit"):
    if uploaded_file:
        st.audio(uploaded_file, format=uploaded_file.type)
        # Save the uploaded file temporarily
        with open("temp_audio_input." + uploaded_file.name.split(".")[-1], "wb") as f:
            f.write(uploaded_file.getbuffer())
        input_filepath = "temp_audio_input." + uploaded_file.name.split(".")[-1]

        
        if platform == "OpenAI":
            audio_file = open(input_filepath, "rb")
            transcription = client1.audio.transcriptions.create(file=audio_file,model=translation_dict[translation_option])
            st.write(transcription.text)

        else:
            with open(input_filepath, "rb") as file:
              transcription = client.audio.transcriptions.create(file=(input_filepath, file.read()),
              model="whisper-large-v3",
              language=lang_dict[selection],
              response_format="verbose_json",)
              st.write(transcription.text)
            
    else:
        st.error("Upload an Audio File First")
          





















