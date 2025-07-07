# 🎓 SmartScribe

**SmartScribe** is your intelligent co-watching companion for videos, lectures, and podcasts. Upload any audio, video, or YouTube link — and SmartScribe will transcribe, summarize, and answer your questions like a smart tutor who already watched the content.

> ✨ Ask questions. 📄 Read transcripts. 💡 Learn deeply.

---

## 📌 Features

- 🎥 **Upload or Paste YouTube Links**  
  Transcribe content from your own files or online videos.

- ✏️ **Accurate Transcriptions**  
  Powered by local OpenAI Whisper.

- 🧠 **Ask Questions About the Media**  
  Ask SmartScribe to summarize, explain, or clarify concepts based on the transcript.

- 🗃️ **Chat History Per Session**  
  Navigate your learning sessions easily from the sidebar.

- 🧾 **Semantic Search & RAG-Powered Answers**  
  AI uses vector embeddings to retrieve relevant content chunks before responding.

- 🖥️ **Clean ChatGPT-style Interface**  
  Built with React + TailwindCSS for a smooth user experience.

---

## 🧩 Tech Stack

| Layer       | Tech                      |
|-------------|---------------------------|
| Frontend    | React, TailwindCSS        |
| Backend     | FastAPI                   |
| Transcripts | OpenAI-Whisper       |
| Embeddings  | `all-MiniLM-L6-v2` via SentenceTransformers |
| Storage     | Appwrite (Docker)         |
| Model for generator    | google/flan-t5-base   |
| Deployment  | Docker, WSL (for dev)     |

The responder logic using local LLM is implemented [here](https://github.com/Kiran-velan/SmartScribe/blob/main/Optional_Enhancement.md).
Instead of using **google/flan-t5-base** as the generator model.
---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.10+
- Node.js + npm
- Docker (for Appwrite)
- WSL (for local dev on Windows) or Linux

### 🐍 Backend (FastAPI)
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start FastAPI server
uvicorn main:app --reload
```
### 💻 Frontend (React + Vite)
```bash
cd frontend/client
npm install
npm run dev
```
### 🗃️ Start Appwrite (Docker)
```bash
cd docker/appwrite
docker compose up -d
```
Make sure Appwrite dashboard is accessible at:
http://localhost

### OS dependencies (manual step)
sudo apt update && sudo apt install ffmpeg

## Appwrite Setup
## Database
### Collections
- Sessions : user_id, created_at, title
- Messages : session_id, timestamp, text, sender
- Transcripts : session_id, user_id, original_text, created_at, title
- Embedding : session_id, number_of_transcripts, vector_file_id
## Storage
- vector_cache
### API key Permissions
- Storage, Database.

## 📸 Screenshots
![Screenshot 2025-07-07 180707](https://github.com/user-attachments/assets/dd0679b9-9ace-4f72-8914-8330c234bb76)
![Screenshot 2025-07-07 180727](https://github.com/user-attachments/assets/8cb0c9d6-d643-4f6a-853f-8de0dc0f8164)
![Screenshot 2025-07-07 180814](https://github.com/user-attachments/assets/59d076bc-c35b-4e97-8dc8-364efa9e8514)
![Screenshot 2025-07-07 180841](https://github.com/user-attachments/assets/33dca02d-615c-4170-963a-50f1bfe98751)


## 🧠 Philosophy
SmartScribe isn't just a transcript viewer. It's an interactive learning assistant designed for:
- Students reviewing lectures
- Learners consuming complex tutorials
- Researchers organizing long-form video/audio data
It’s like having a personal tutor who has already watched the video — and is ready to answer.
