# Step 2: OpenAI embeddings

from sentence_transformers import SentenceTransformer
import os

# Load embedding model (first time it will download and cache)
model_name = "all-MiniLM-L6-v2"
embedder = SentenceTransformer(model_name, device="cpu")

def get_embeddings(chunks: list[str]) -> list[list[float]]:
    """
    Generate embeddings using Hugging Face's sentence-transformers.
    """
    try:
        embeddings = embedder.encode(chunks, show_progress_bar=True)
        return embeddings
    except Exception as e:
        print(f"[Embedder] Error: {e}")
        return []


# Optional: test this module directly

# if __name__ == "__main__":
#     from app.rag.chunker import chunk_transcript
#     import torch
#     print("CUDA available:", torch.cuda.is_available())
#     print("Device:", embedder.device)

#     transcript = (
#         "Today we're discussing how backpropagation works in neural networks, "
#         "including the concept of gradient descent and how weights are updated layer by layer..."
#     ) * 5

#     chunks = chunk_transcript(transcript)
#     print(f"Generated {len(chunks)} chunks.")

#     embeddings = get_embeddings(chunks)
#     print(f"Got {len(embeddings)} embeddings.")
#     if len(embeddings) > 0:
#         print(f"First embedding (truncated): {embeddings[0][:5]}...")
#     else:
#         print("No embeddings generated.")
