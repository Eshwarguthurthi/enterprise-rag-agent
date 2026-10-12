from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"


class EmbeddingModel:

    def __init__(self):
        print(f"Loading embedding model: {MODEL_NAME}")
        self.model = SentenceTransformer(MODEL_NAME)
        print("Embedding model loaded successfully.")

    def embed_documents(self, texts):
        return self.model.encode(
            texts,
            show_progress_bar=True,
            normalize_embeddings=True
        )

    def embed_query(self, query):
        return self.model.encode(
            [query],
            normalize_embeddings=True
        )[0]


if __name__ == "__main__":

    embedder = EmbeddingModel()

    texts = [
        "Employees are entitled to 12 casual leave days per year.",
        "VPN installation requires the approved VPN client."
    ]

    embeddings = embedder.embed_documents(texts)

    print("\n" + "=" * 60)
    print("EMBEDDING TEST")
    print("=" * 60)

    print(f"Number of texts : {len(texts)}")
    print(f"Embedding shape : {embeddings.shape}")
    print(f"Vector dimension: {embeddings.shape[1]}")

    print("\nFirst vector:")
    print(embeddings[0][:10])
