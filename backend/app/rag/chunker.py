# Step 1: chunk_transcript()

def chunk_transcript(text: str, max_chunk_size: int = 500, overlap: int = 100) -> list[str]:
    """
    Splits a long transcript into overlapping chunks for RAG search.
    """
    chunks = []
    start = 0
    text_length = len(text)

    while start < text_length:
        end = min(start + max_chunk_size, text_length)
        chunk = text[start:end]
        chunks.append(chunk.strip())
        start += max_chunk_size - overlap

    return chunks


# Optional: run directly to test chunking

# if __name__ == "__main__":
#     sample_text = (
#         "Welcome to the introduction to machine learning. "
#         "In this lecture, we'll cover supervised and unsupervised learning, "
#         "gradient descent, and how models generalize from data. "
#         "This course is suitable for beginners and will include both theory and practical demos. "
#         "By the end, you'll be able to build simple ML models in Python."
#     ) * 10  # simulate a longer transcript

#     chunks = chunk_transcript(sample_text)
#     for i, chunk in enumerate(chunks):
#         print(f"\n--- Chunk {i+1} ---\n{chunk}")
