from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from retrieval.retriever import Retriever
from retrieval.reranker import Reranker
from evaluation_dataset import EVALUATION_DATASET


def unique_documents(documents):
    return list(dict.fromkeys(documents))


def calculate_precision(retrieved, relevant):
    if not retrieved:
        return 0.0

    return sum(
        1 for doc in retrieved
        if doc in relevant
    ) / len(retrieved)


def calculate_recall(retrieved, relevant):
    if not relevant:
        return 0.0

    return len(set(retrieved) & set(relevant)) / len(relevant)


def calculate_reciprocal_rank(retrieved, relevant):
    for rank, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1 / rank

    return 0.0


def evaluate_reranker():

    # Retrieve more candidates before reranking
    retriever = Retriever(top_k=10)

    # Load Cross-Encoder
    reranker = Reranker()

    precision_scores = []
    recall_scores = []
    reciprocal_ranks = []

    print("\n" + "=" * 70)
    print("RERANKER EVALUATION")
    print("=" * 70)

    for i, item in enumerate(EVALUATION_DATASET, start=1):

        question = item["question"]
        relevant_documents = set(item["relevant_documents"])

        # Step 1: Retrieve candidates
        results = retriever.search(question)

        # Step 2: Rerank candidates
        reranked_results = reranker.rerank(
            question,
            results,
            top_k=3
        )

        retrieved_documents = [
            result["metadata"].get("filename")
            for result in reranked_results
        ]

        # Remove duplicate documents
        unique_retrieved = unique_documents(
            retrieved_documents
        )

        precision = calculate_precision(
            unique_retrieved,
            relevant_documents
        )

        recall = calculate_recall(
            unique_retrieved,
            relevant_documents
        )

        reciprocal_rank = calculate_reciprocal_rank(
            unique_retrieved,
            relevant_documents
        )

        precision_scores.append(precision)
        recall_scores.append(recall)
        reciprocal_ranks.append(reciprocal_rank)

        print(f"\nQuestion {i}: {question}")
        print(f"Expected: {list(relevant_documents)}")
        print(f"Reranked: {unique_retrieved}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall: {recall:.3f}")
        print(f"Reciprocal Rank: {reciprocal_rank:.3f}")

    avg_precision = sum(precision_scores) / len(precision_scores)
    avg_recall = sum(recall_scores) / len(recall_scores)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n" + "=" * 70)
    print("FINAL RERANKER RESULTS")
    print("=" * 70)

    print(f"Precision: {avg_precision:.3f}")
    print(f"Recall:    {avg_recall:.3f}")
    print(f"MRR:       {mrr:.3f}")

    print("=" * 70)


if __name__ == "__main__":
    evaluate_reranker()