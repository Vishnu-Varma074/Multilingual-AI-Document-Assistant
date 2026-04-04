# 📚 DocuLens – Multilingual AI Document Assistant

> **Upload PDFs & TXTs → Ask questions in any language → Get instant AI-powered answers**  
> Powered by Groq + LLaMA 3.1 + LangChain + FAISS

---

## 📌 What is this?

**DocuLens** is an AI-powered document assistant that lets you upload PDF or TXT files and interact with them using natural language. Ask questions, request summaries, or translate content — all in your preferred language including English, Hindi, Telugu, and more.

Built with **Streamlit + FastAPI + LangChain RAG pipeline + Groq LLM**.

---

## ✨ Features

- 📤 **Multi-document Upload** — Upload multiple PDFs and TXT files at once
- 🔍 **RAG-powered Q&A** — Ask questions and get accurate answers grounded in your documents
- 🌍 **Multilingual Support** — Query and receive responses in English, Hindi (हिंदी), Telugu (తెలుగు), and more
- 📝 **Smart Summarization** — Auto-detects summarization requests and generates concise summaries
- 🔄 **Intelligent Translation** — Translates full documents or specific sections into the target language
- 📄 **Document Filtering** — Select specific documents to query instead of searching across all
- ⚡ **Fast Inference** — Powered by Groq's ultra-fast LLaMA 3.1 8B Instant model
- 🧠 **Vector Search** — Uses FAISS + HuggingFace embeddings for semantic document retrieval
- 🖥️ **Dual Interface** — Use via Streamlit UI or REST API (FastAPI)
- 🔐 **Session Management** — FastAPI backend supports isolated sessions per user

---

## 🗂️ Project Structure

```
doculens/
│
├── app.py                  # Streamlit frontend — UI + document interaction
├── main.py                 # FastAPI backend — REST API with session management
├── rag.py                  # RAG pipeline — document processing, embeddings, LLM querying
├── requirements.txt        # All project dependencies
├── .gitignore
└── README.md
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | FastAPI + Uvicorn |
| LLM | Groq — LLaMA 3.1 8B Instant |
| Embeddings | HuggingFace — `all-MiniLM-L6-v2` |
| Vector Store | FAISS (CPU) |
| RAG Framework | LangChain + LangChain-Classic |
| PDF Parsing | PyPDF |
| Language | Python 3.10+ |

---

## ⚙️ Setup & Installation

### Prerequisites
- Python 3.10 or higher
- A free [Groq API Key](https://console.groq.com/)

---

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/doculens.git
cd doculens
```

---

### 2. Create a Virtual Environment

```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On Mac/Linux:
source venv/bin/activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Set up your `.env` file

Create a `.env` file in the project root:

```
GROQ_API_KEY=gsk_your_actual_key_here
```

> ⚠️ **Never share or commit this file.** It is already covered by `.gitignore`.

---

## 🚀 Running the App

### Option A — Streamlit UI (Recommended)

```bash
streamlit run app.py
```

Opens at: [http://localhost:8501](http://localhost:8501)

> You can also enter your Groq API key directly in the sidebar if you haven't set up a `.env` file.

---

### Option B — FastAPI Backend (For API / developers)

```bash
uvicorn main:app --host 127.0.0.1 --port 8000 --reload
```

API docs available at: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🖥️ How to Use (Streamlit)

1. Open the app in your browser
2. Enter your Groq API key in the sidebar (if not set in `.env`)
3. Upload one or more **PDF or TXT** files
4. Click **🚀 Process Documents**
5. (Optional) Select specific documents to query
6. Type your question or command in the text box
7. Click **🚀 Submit Query** and view the answer

---

## 🌐 API Endpoints (FastAPI)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `GET` | `/health` | Health status |
| `POST` | `/documents/process` | Upload and process documents |
| `GET` | `/sessions/{session_id}` | Get session info and available docs |
| `DELETE` | `/sessions/{session_id}` | Delete session and free memory |
| `POST` | `/query` | Ask a question against processed documents |

### Example API Usage

**Step 1 — Upload and process documents:**
```bash
curl -X POST "http://127.0.0.1:8000/documents/process" \
  -H "X-Groq-Api-Key: gsk_your_key_here" \
  -F "files=@document.pdf"
```

**Step 2 — Query the documents:**
```bash
curl -X POST "http://127.0.0.1:8000/query" \
  -H "X-Groq-Api-Key: gsk_your_key_here" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "your-session-id", "query": "Summarize the document"}'
```

---

## 💬 Example Queries

| Query | What it does |
|---|---|
| `Summarize the document` | Generates a concise summary |
| `What is mentioned about taxes?` | Answers a specific question |
| `Translate to Telugu` | Translates content into Telugu |
| `Translate the introduction section to Hindi` | Translates a specific section |
| `What are the key points in section 3?` | Extracts information from a section |

---

## 📦 Dependencies (`requirements.txt`)

```
fastapi>=0.111.0
uvicorn[standard]>=0.29.0
python-multipart>=0.0.9
pydantic>=2.7.0
python-dotenv>=1.0.0
langchain>=0.2.0
langchain-groq>=0.1.3
langchain-community>=0.2.0
faiss-cpu>=1.8.0
pypdf>=4.2.0
```

---

## ⚠️ Known Limitations

- Large documents may take a minute to process during embedding generation
- FAISS runs on CPU — no GPU required but processing is slower for very large files
- Session data is stored in memory — restarting the FastAPI server clears all sessions
- Supported file formats: `.pdf` and `.txt` only

---

## 🔐 Environment Variables

| Variable | Description |
|---|---|
| `GROQ_API_KEY` | Your Groq API key from [console.groq.com](https://console.groq.com/) |

---

*Built with ❤️ using Groq + LLaMA 3.1 + LangChain — Ask your documents anything, in any language.*
