# 🎤 Conversational Skill Mirror

> **Interview & Public Speaking Coach powered by GenAI + NLP**  
> Record your speech → Get instant AI-powered feedback → Improve with confidence

---

## 📌 What is this?

**Conversational Skill Mirror** is an AI-powered coaching tool designed to help users — especially Indian English and Hinglish speakers — improve their interview and public speaking skills. It transcribes your spoken response, analyzes it using large language models, and gives you detailed, actionable feedback instantly.

Built with **FastAPI + Faster-Whisper + Groq (LLaMA 3.3 70B) + Streamlit**.

---

## ✨ Features

- 🎙️ **Audio Recording** directly in the browser via Streamlit
- 📝 **Speech Transcription** using OpenAI's Whisper (via `faster-whisper`)
- 🤖 **AI Analysis** powered by Groq's LLaMA 3.3 70B model
- 📊 **Detailed Metrics** — Filler word count, Pace (WPM), Clarity score, Topic coverage
- 🌍 **Cultural Nuance Feedback** — Tailored for Indian English / Hyderabad / Telangana context
- ✅ **Strengths & Improvement Areas** — Bullet-pointed feedback
- ⚠️ **Bias Detection** — Flags any unintentional biased language
- 🔥 **Improved Response Generator** — Polished, professional rephrasing of your answer
- 🚀 **Confidence Boosting Tips** — 3–4 actionable tips per session
- 🎭 **Role Play Continuation** — Suggested next interviewer question + ideal reply
- 🖥️ Two modes: **Interview Practice** and **Public Speaking**

---

## 🗂️ Project Structure

```
conversational-skill-mirror/
│
├── backend/
│   ├── main.py              # FastAPI backend — transcription + AI analysis
│   └── requirements.txt     # Backend dependencies
│
├── frontend/
│   ├── app.py               # Streamlit frontend — UI + API calls
│   └── requirements.txt     # Frontend dependencies
│
├── .gitignore               # Ignores .env, __pycache__, venv, etc.
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| Transcription | Faster-Whisper (small model, CPU) |
| AI Analysis | Groq API — LLaMA 3.3 70B Versatile |
| Language | Python 3.10+ |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A free [Groq API Key](https://console.groq.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/conversational-skill-mirror.git
cd conversational-skill-mirror
```

---

### 2. Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Create your `.env` file

Inside the `backend/` folder, create a file named `.env`:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

> ⚠️ **Important:** Never share or commit this file. It's already covered by `.gitignore`.

#### Start the Backend

```bash
uvicorn main:app --host 127.0.0.1 --port 8000
```

You should see:
```
✅ GROQ_API_KEY loaded successfully!
Loading faster-whisper 'small' model...
✅ Whisper model loaded successfully!
```

API docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

### 3. Frontend Setup

Open a **new terminal**:

```bash
cd frontend

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

#### Start the Frontend

```bash
streamlit run app.py
```

The app will open at: [http://localhost:8501](http://localhost:8501)

---

## 🚀 How to Use

1. Open the Streamlit app in your browser
2. Select a mode: **Interview Practice** or **Public Speaking**
3. (Optional) Enter your practice question or topic
4. Click the microphone to **record your response** (up to 4 minutes)
5. Click **📤 Analyze Speech**
6. View your detailed feedback — transcript, scores, tips, improved response, and more!

---

## 📊 Analysis Output

| Metric | Description |
|---|---|
| Filler Count | Number of filler words (um, uh, like, etc.) |
| Pace (WPM) | Words per minute — ideal is 120–150 WPM |
| Clarity Score | 1–10 rating of speech clarity |
| Topic Coverage | 1–10 rating of how well the topic was addressed |
| Bias Detected | Flags unintentional biased language |
| Cultural Nuance | Feedback tailored to Indian English speakers |
| Improved Response | AI-rewritten version of your answer |
| Confidence Tips | 3–4 personalized tips to speak better |
| Role Play | Suggested next question + ideal answer |

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com/) |

---

## 📦 Dependencies

### Backend (`backend/requirements.txt`)
```
fastapi==0.115.*
uvicorn==0.34.*
faster-whisper==1.1.*
groq==0.15.*
python-dotenv==1.0.*
pydub==0.25.*
python-multipart==0.0.*
```

### Frontend (`frontend/requirements.txt`)
```
streamlit==1.42.*
requests==2.32.*
python-dotenv==1.0.*
```

---

## ⚠️ Known Limitations

- Analysis may take up to 40 seconds for 4-minute recordings
- Whisper `small` model runs on CPU — first load takes 15–30 seconds
- Audio files larger than 20 MB may slow down analysis
- Supported audio formats: `.wav`, `.mp3`, `.m4a`, `.webm`

---

## 🙌 Acknowledgements

- [OpenAI Whisper](https://github.com/openai/whisper) — Speech recognition
- [Faster-Whisper](https://github.com/SYSTRAN/faster-whisper) — Optimized Whisper inference
- [Groq](https://groq.com/) — Ultra-fast LLM inference
- [Streamlit](https://streamlit.io/) — Frontend UI framework
- [FastAPI](https://fastapi.tiangolo.com/) — Backend API framework

---

