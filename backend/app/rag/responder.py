# Step 4: send to OpenAI GPT

from sentence_transformers import SentenceTransformer
from transformers import pipeline
from app.rag.vector_store import TranscriptVectorStore
from app.rag.chunker import chunk_transcript
from app.rag.embedder import get_embeddings

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Load HF language model (replace with larger model later)
generator = pipeline("text2text-generation", model="google/flan-t5-base", device=0 if embedder.device.type == "cuda" else -1)


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
    prompt = f"Answer the question based on the context.\n\nContext:\n{context}\n\nQuestion: {question}"

    try:
        response = generator(prompt, max_new_tokens=256)
        return response[0]["generated_text"].strip()
    except Exception as e:
        return f"[Generation error] {e}"


# 🧪 Optional test block
# Initialize vector store (same dim as embeddings)

# vector_store = TranscriptVectorStore(dim=384)
# if __name__ == "__main__":
#     # Dummy transcript to simulate full RAG flow
#     transcript = (
#         "Gradient descent helps train neural networks by minimizing the loss function "
#         "using the calculated gradients to update weights layer by layer."
#     ) * 5

#     chunks = chunk_transcript(transcript)
#     embeddings = get_embeddings(chunks)

#     vector_store.add_embeddings(embeddings, chunks)

#     query = "How is gradient descent useful in neural networks?"
#     answer = answer_question(query, vector_store)

#     print("\n💬 Answer:\n", answer)
