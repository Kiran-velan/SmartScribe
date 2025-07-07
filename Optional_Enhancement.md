# 💡 Optional Enhancement: Local LLM Server Integration for Response Generation

This enhancement replaces the direct use of Hugging Face `pipeline` (e.g., `google/flan-t5-base`) with a locally hosted LLM server to handle question-answering tasks more efficiently and securely.

---

## 🧠 Motivation

Using a local LLM server offers:
- **Faster inference** after initial load
- **Offline capabilities**
- **Lower latency** in repeated queries
- **Better control** over memory and compute resources
- **Scalability** for larger models or concurrent users

---

## 🛠️ Code Changes

### ✅ Modified: `responder.py`

```python
# Step 4: send to OpenAI GPT

from sentence_transformers import SentenceTransformer
from app.rag.vector_store import TranscriptVectorStore
from app.rag.chunker import chunk_transcript
from app.rag.embedder import get_embeddings
import requests

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")


def build_context(vector_store: TranscriptVectorStore, question: str, top_k: int = 3) -> str:
    """
    Embed question, search top chunks, and return context string.
    """
    query_embedding = embedder.encode([question])[0]
    top_chunks = vector_store.search(query_embedding, top_k=top_k)
    context = "\n".join([chunk for chunk, _ in top_chunks])
    return context


def answer_question(question: str, vector_store: TranscriptVectorStore) -> str:
    """
    Build context and run local HF generation.
    """
    context = build_context(vector_store, question)
    prompt = f"Imagine yourself as a tutor and Answer the question based on the context.\n\nContext:\n{context}\n\nQuestion: {question}"

    try:
        response = requests.post(
            "http://localhost:8888/generate",
            json={
                "prompt": prompt,
                "model": "mistral:instruct",
                "max_tokens": 256  # Optional, depends on your server
            },
            timeout=60  # Adjust timeout as needed
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()
    except Exception as e:
        print(f"Generation error: {e}")
        return "Sorry, I couldn't generate a response at the moment."

```

---

## You can find the local LLM server setup in the [Local LLM Server Repo](https://github.com/Kiran-velan/Local-LLM-Server).