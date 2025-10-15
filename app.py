# ---- Python 3.13 audioop compatibility fix ----
import sys
import types

if "pyaudioop" not in sys.modules:
    fake = types.ModuleType("pyaudioop")
    def _fakefunc(*args, **kwargs): return None
    for name in ["add", "adpcm2lin", "alaw2lin", "bias", "lin2adpcm",
                 "lin2alaw", "lin2ulaw", "ulaw2lin", "mul", "avg", "max"]:
        setattr(fake, name, _fakefunc)
    sys.modules["pyaudioop"] = fake
# ------------------------------------------------

import os
import streamlit as st
import whisper
from pydub import AudioSegment
import tempfile
from datetime import datetime
import requests
import json

# ---------------- Streamlit UI -----------------
st.set_page_config(page_title="Meeting Summarizer (Gemini Free)", layout="centered")
st.title("🎙️ Meeting Summarizer (Gemini Free API)")
st.markdown("Upload a meeting audio file and get a concise summary, key decisions, and action items using **Google Gemini (MakerSuite Free API)**.")

with st.sidebar:
    st.header("Settings")
    gemini_key = st.text_input("Enter your Gemini API Key (from makersuite.google.com/app/apikey)", type="password")
    model_choice = st.selectbox("Whisper model", ["tiny", "base", "small"])
    if gemini_key:
        os.environ["GEMINI_API_KEY"] = gemini_key

uploaded_file = st.file_uploader("Upload meeting audio", type=["mp3", "wav", "m4a"])

# -------------- Helper functions -----------------
def convert_audio_to_wav(in_bytes, out_path):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(in_bytes)
    temp.flush()
    audio = AudioSegment.from_file(temp.name)
    audio.export(out_path, format="wav")

@st.cache_resource
def load_whisper_model(name):
    return whisper.load_model(name)

def transcribe_with_whisper(model, audio_path):
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_with_gemini(transcript):
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("Gemini API key not set. Add it in sidebar or as GEMINI_API_KEY.")

    # MakerSuite (Free) endpoint
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={api_key}"
    headers = {"Content-Type": "application/json"}

    prompt = f"""
You are an assistant that reads a meeting transcript and produces:
1. A concise 5-line summary.
2. A list of key decisions made.
3. A list of actionable tasks with owners and deadlines.

Return output clearly under the headings:
- Summary
- Key Decisions
- Action Items

Transcript:
{transcript}
"""

    data = {
        "contents": [
            {"parts": [{"text": prompt}]}
        ]
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code != 200:
        raise Exception(f"Gemini API error: {response.status_code} - {response.text}")

    result = response.json()
    try:
        return result["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        raise Exception(f"Unexpected response format: {result}") from e

# ------------------- Main logic -------------------
if uploaded_file is not None:
    with st.spinner("Processing audio..."):
        audio_bytes = uploaded_file.read()
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        tmp_wav = f"temp_{timestamp}.wav"
        convert_audio_to_wav(audio_bytes, tmp_wav)

    st.info("Loading Whisper model (may take a minute first time)...")
    model = load_whisper_model(model_choice)

    with st.spinner("Transcribing meeting..."):
        transcript = transcribe_with_whisper(model, tmp_wav)

    st.subheader("🗒️ Transcript")
