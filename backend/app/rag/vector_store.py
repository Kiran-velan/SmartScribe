# Step 3: FAISS logic

import faiss
import numpy as np
from typing import List, Tuple


class TranscriptVectorStore:
    def __init__(self, dim: int):
        self.dim = dim
        self.index = faiss.IndexFlatL2(dim)  # L2 = Euclidean distance
        self.chunks: List[str] = []  # Store the original text chunks in parallel

    def add_embeddings(self, embeddings: List[List[float]], chunks: List[str]):
        """
        Add embeddings and their corresponding text chunks to the index.
        """
        np_embeddings = np.array(embeddings).astype("float32")
        self.index.add(np_embeddings)
        self.chunks.extend(chunks)

    def search(self, query_embedding: List[float], top_k: int = 3) -> List[Tuple[str, float]]:
        """
        Return top_k = 3 most similar chunks to the query embedding.
        """
        query_vector = np.array([query_embedding]).astype("float32")
        distances, indices = self.index.search(query_vector, top_k)

        results = []
        for i, dist in zip(indices[0], distances[0]):
            if i < len(self.chunks):
                results.append((self.chunks[i], float(dist)))
        return results


# 🔍 Optional test

# if __name__ == "__main__":
#     from app.rag.embedder import get_embeddings
#     from app.rag.chunker import chunk_transcript

#     transcript = (
#         "Gradient descent is a technique used to minimize the error in neural networks. "
#         "It works by calculating the gradient of the loss function and adjusting weights accordingly. "
#     ) * 5

#     chunks = chunk_transcript(transcript)
#     embeddings = get_embeddings(chunks)

#     store = TranscriptVectorStore(dim=len(embeddings[0]))
#     store.add_embeddings(embeddings, chunks)

#     print(f"Added {len(embeddings)} vectors to FAISS index.")

#     # Simulate a query
#     query = "How does gradient descent help in training?"
#     query_embedding = get_embeddings([query])[0]
#     results = store.search(query_embedding)

#     print("\nTop results:")
#     for chunk, dist in results:
#         print(f"\nScore: {dist:.4f}\nChunk: {chunk[:100]}...")
