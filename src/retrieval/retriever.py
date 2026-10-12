from pathlib import Path
import pickle
import sys

import faiss


# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_DIR))


from embeddings.embedder import EmbeddingModel


# --------------------------------------------------
# Project paths
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

VECTOR_DB_DIR = BASE_DIR / "vector_db" / "faiss_index"

INDEX_PATH = VECTOR_DB_DIR / "index.faiss"
CHUNKS_PATH = VECTOR_DB_DIR / "chunks.pkl"


class Retriever:

    def __init__(self, top_k=3):

        self.top_k = top_k

        print("Loading FAISS index...")

        self.index = faiss.read_index(
            str(INDEX_PATH)
        )

        print(f"FAISS vectors loaded: {self.index.ntotal}")

        print("Loading chunks...")

        with open(CHUNKS_PATH, "rb") as file:
            self.chunks = pickle.load(file)

        print(f"Chunks loaded: {len(self.chunks)}")

        print("Loading embedding model...")

        self.embedder = EmbeddingModel()

        print("Retriever initialized successfully.")

    def search(self, query):

        # Convert query into embedding
        query_embedding = self.embedder.embed_query(query)

        # FAISS expects a 2D array
        query_embedding = query_embedding.reshape(1, -1)

        # Search FAISS
        scores, indices = self.index.search(
            query_embedding,
            self.top_k
        )

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            chunk = self.chunks[index]

            results.append({
                "score": float(score),
                "content": chunk.page_content,
                "metadata": chunk.metadata
            })

        return results


def print_results(query, results):

    print("\n" + "=" * 70)
    print("SEMANTIC SEARCH RESULTS")
    print("=" * 70)

    print(f"\nQuery: {query}")

    print(f"\nResults found: {len(results)}")

    for position, result in enumerate(results, start=1):

        metadata = result["metadata"]

        print("\n" + "-" * 70)

        print(f"Result #{position}")
        print(f"Similarity score : {result['score']:.4f}")
        print(f"Source           : {metadata.get('source')}")
        print(f"Category         : {metadata.get('category')}")
        print(f"Page             : {metadata.get('page_number')}")

        print("\nContent:")
        print(result["content"])


if __name__ == "__main__":

    retriever = Retriever(top_k=3)

    test_queries = [
        "How many casual leave days do employees get?",
        "How do I reset my password?",
        "What is the warranty period for the product?",
        "How should a critical support ticket be escalated?"
    ]

    for query in test_queries:

        results = retriever.search(query)

        print_results(query, results)