<<<<<<< HEAD
# Meeting Summarizer (Gemini + Whisper + Streamlit)

A free Streamlit app that:
- Takes a meeting audio file.
- Transcribes it locally using Whisper.
- Summarizes and extracts action items using Google Gemini API.

## Setup (Windows + VS Code)

1. Create a virtual environment:
python -m venv venv
venv\Scripts\activatepython


2. Install dependencies:
pip install -r requirements.txt


3. Run the app:
streamlit run app.py


4. Enter your Gemini API key in the sidebar.

## Deploy to Streamlit Cloud

1. Push your code to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Connect repo → choose `app.py`.
4. Add secret key in “Settings → Secrets”:

GEMINI_API_KEY="your_api_key_here"

5. Click **Deploy** 🚀
=======
# Meeting Summarizer (Gemini + Whisper + Streamlit)

A free Streamlit app that:
- Takes a meeting audio file.
- Transcribes it locally using Whisper.
- Summarizes and extracts action items using Google Gemini API.

## Setup (Windows + VS Code)

1. Create a virtual environment:
python -m venv venv
venv\Scripts\activatepython


2. Install dependencies:
pip install -r requirements.txt


3. Run the app:
streamlit run app.py


4. Enter your Gemini API key in the sidebar.

## Deploy to Streamlit Cloud

1. Push your code to GitHub.
2. Go to [https://share.streamlit.io](https://share.streamlit.io).
3. Connect repo → choose `app.py`.
4. Add secret key in “Settings → Secrets”:

GEMINI_API_KEY="your_api_key_here"

5. Click **Deploy**
>>>>>>> b4ddd896070d385ca5d53d6735764765b82e4531
