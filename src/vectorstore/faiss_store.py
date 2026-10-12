from pathlib import Path
import pickle
import sys

import faiss


# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_DIR))


from ingestion.loader import load_all_documents
from ingestion.cleaner import clean_documents
from ingestion.splitter import create_chunks
from embeddings.embedder import EmbeddingModel


# Project directories
BASE_DIR = Path(__file__).resolve().parents[2]
VECTOR_DB_DIR = BASE_DIR / "vector_db" / "faiss_index"

VECTOR_DB_DIR.mkdir(parents=True, exist_ok=True)


def build_vector_store():

    print("=" * 70)
    print("BUILDING FAISS VECTOR STORE")
    print("=" * 70)

    # --------------------------------------------------
    # 1. Load documents
    # --------------------------------------------------
    print("\n[1] Loading documents...")

    documents = load_all_documents()

    print(f"Documents/pages loaded: {len(documents)}")

    # --------------------------------------------------
    # 2. Clean documents
    # --------------------------------------------------
    print("\n[2] Cleaning documents...")

    documents = clean_documents(documents)

    print(f"Documents cleaned: {len(documents)}")

    # --------------------------------------------------
    # 3. Create chunks
    # --------------------------------------------------
    print("\n[3] Creating chunks...")

    chunks = create_chunks(
        documents,
        chunk_size=700,
        chunk_overlap=100
    )

    print(f"Total chunks created: {len(chunks)}")

    # --------------------------------------------------
    # 4. Extract text
    # --------------------------------------------------
    texts = [chunk.page_content for chunk in chunks]

    # --------------------------------------------------
    # 5. Create embeddings
    # --------------------------------------------------
    print("\n[4] Creating embeddings...")

    embedder = EmbeddingModel()

    embeddings = embedder.embed_documents(texts)

    print(f"Embedding shape: {embeddings.shape}")

    # --------------------------------------------------
    # 6. Create FAISS index
    # --------------------------------------------------
    print("\n[5] Creating FAISS index...")

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatIP(dimension)

    index.add(embeddings)

    print(f"Vectors stored in FAISS: {index.ntotal}")

    # --------------------------------------------------
    # 7. Save FAISS index
    # --------------------------------------------------
    index_path = VECTOR_DB_DIR / "index.faiss"

    faiss.write_index(
        index,
        str(index_path)
    )

    # --------------------------------------------------
    # 8. Save chunks
    # --------------------------------------------------
    chunks_path = VECTOR_DB_DIR / "chunks.pkl"

    with open(chunks_path, "wb") as file:
        pickle.dump(chunks, file)

    # --------------------------------------------------
    # Final result
    # --------------------------------------------------
    print("\n" + "=" * 70)
    print("FAISS VECTOR STORE CREATED SUCCESSFULLY")
    print("=" * 70)

    print(f"Index file : {index_path}")
    print(f"Chunks file: {chunks_path}")
    print(f"Vectors    : {index.ntotal}")
    print(f"Dimension  : {dimension}")


if __name__ == "__main__":
    build_vector_store()