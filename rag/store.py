from functools import lru_cache

import faiss
from sentence_transformers import SentenceTransformer

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"


@lru_cache(maxsize=1)
def get_model():
    return SentenceTransformer(MODEL_NAME)


def embed(texts):
    vectors = get_model().encode(
        texts, batch_size=32, normalize_embeddings=True, convert_to_numpy=True
    )
    return vectors.astype("float32")


class VectorStore:
    def __init__(self, chunks):
        vectors = embed([chunk["text"] for chunk in chunks])
        self.index = faiss.IndexFlatIP(vectors.shape[1])
        self.index.add(vectors)
        self.chunks = chunks

    def search(self, query, k=4):
        k = min(k, len(self.chunks))
        scores, ids = self.index.search(embed([query]), k)
        return [
            {**self.chunks[i], "score": float(score)}
            for score, i in zip(scores[0], ids[0])
            if i != -1
        ]
