from sentence_transformers import CrossEncoder


class Reranker:
    def __init__(
        self,
        model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"
    ):
        print(f"Loading reranker model: {model_name}")

        self.model = CrossEncoder(model_name)

        print("Reranker model loaded successfully.")

    def rerank(self, query, results, top_k=3):
        if not results:
            return []

        pairs = [
            (query, result["content"])
            for result in results
        ]

        scores = self.model.predict(pairs)

        reranked_results = []

        for result, score in zip(results, scores):
            updated_result = result.copy()
            updated_result["rerank_score"] = float(score)
            reranked_results.append(updated_result)

        reranked_results.sort(
            key=lambda x: x["rerank_score"],
            reverse=True
        )

        return reranked_results[:top_k]


if __name__ == "__main__":

    from pathlib import Path
    import sys

    SRC_DIR = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(SRC_DIR))

    from retrieval.retriever import Retriever

    retriever = Retriever(top_k=10)
    reranker = Reranker()

    query = "How many casual leave days do employees get?"

    print("\nOriginal Retrieval Results:")
    results = retriever.search(query)

    for i, result in enumerate(results, 1):
        print(
            f"{i}. "
            f"{result['metadata'].get('filename')} "
            f"| FAISS Score: {result['score']:.4f}"
        )

    print("\nAfter Reranking:")

    reranked = reranker.rerank(
        query,
        results,
        top_k=3
    )

    for i, result in enumerate(reranked, 1):
        print(
            f"{i}. "
            f"{result['metadata'].get('filename')} "
            f"| Rerank Score: {result['rerank_score']:.4f}"
        )