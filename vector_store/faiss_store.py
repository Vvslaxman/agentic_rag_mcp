import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class FaissStore:
    def __init__(self, embedding_model_name='all-MiniLM-L6-v2'):
        self.model = SentenceTransformer(embedding_model_name)
        self.index = None
        self.embeddings = []
        self.metadatas = []
        self.dimension = self.model.get_sentence_embedding_dimension()

    def add_embeddings(self, texts, metadatas):
        # texts: list of strings, metadatas: list of dicts
        new_embs = self.model.encode(texts, show_progress_bar=False)
        new_embs = np.array(new_embs).astype('float32')
        if self.index is None:
            self.index = faiss.IndexFlatL2(self.dimension)
        self.index.add(new_embs)
        self.embeddings.extend(new_embs)
        self.metadatas.extend(metadatas)

    def query(self, query_text, top_k=5):
        query_emb = self.model.encode([query_text]).astype('float32')
        D, I = self.index.search(query_emb, top_k)
        results = []
        for idx in I[0]:
            if idx < len(self.metadatas):
                results.append(self.metadatas[idx])
        return results 