def chunk_text(text, chunk_size=500, overlap=50):
    """
    Split text into overlapping chunks.
    Returns a list of dicts: { 'text': ..., 'chunk_id': ... }
    """
    chunks = []
    start = 0
    chunk_id = 0
    while start < len(text):
        end = min(start + chunk_size, len(text))
        chunk = text[start:end]
        chunks.append({"text": chunk, "chunk_id": chunk_id})
        chunk_id += 1
        start += chunk_size - overlap
    return chunks 