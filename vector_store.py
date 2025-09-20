from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

class VectorStore:
    def __init__(self, embed_model="all-MiniLM-L6-v2"):
        self.model = SentenceTransformer(embed_model)
        self.texts = []
        self.index = None

    def build(self, documents):
        self.texts = [doc['content'] for doc in documents]
        vectors = self.model.encode(self.texts, convert_to_numpy=True)
        dim = vectors.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(vectors)

    def query(self, question, top_k=3):
        q_vector = self.model.encode([question], convert_to_numpy=True)
        distances, indices = self.index.search(q_vector, top_k)
        return [self.texts[i] for i in indices[0]]
