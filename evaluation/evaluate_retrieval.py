from pathlib import Path
import sys

# Add project src directory
PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from retrieval.retriever import Retriever
from evaluation_dataset import EVALUATION_DATASET


def unique_documents(documents):
    """Remove duplicate document names while preserving order."""
    return list(dict.fromkeys(documents))


def calculate_precision(retrieved, relevant):
    if not retrieved:
        return 0.0

    relevant_count = sum(
        1 for doc in retrieved
        if doc in relevant
    )

    return relevant_count / len(retrieved)


def calculate_recall(retrieved, relevant):
    if not relevant:
        return 0.0

    retrieved_relevant = set(retrieved) & set(relevant)

    return len(retrieved_relevant) / len(relevant)


def calculate_reciprocal_rank(retrieved, relevant):
    for rank, doc in enumerate(retrieved, start=1):
        if doc in relevant:
            return 1 / rank

    return 0.0


def evaluate_retriever(top_k=3):

    retriever = Retriever(top_k=top_k)

    precision_scores = []
    recall_scores = []
    reciprocal_ranks = []

    print("\n" + "=" * 70)
    print("RETRIEVER EVALUATION")
    print("=" * 70)

    for i, item in enumerate(EVALUATION_DATASET, start=1):

        question = item["question"]
        relevant_documents = set(item["relevant_documents"])

        results = retriever.search(question)

        retrieved_documents = [
            result["metadata"].get("filename")
            for result in results
        ]

        # Remove duplicate documents
        unique_retrieved = unique_documents(retrieved_documents)

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
        print(f"Retrieved: {unique_retrieved}")
        print(f"Precision: {precision:.3f}")
        print(f"Recall: {recall:.3f}")
        print(f"Reciprocal Rank: {reciprocal_rank:.3f}")

    # Calculate averages
    avg_precision = sum(precision_scores) / len(precision_scores)
    avg_recall = sum(recall_scores) / len(recall_scores)
    mrr = sum(reciprocal_ranks) / len(reciprocal_ranks)

    print("\n" + "=" * 70)
    print("FINAL RESULTS")
    print("=" * 70)

    print(f"Precision: {avg_precision:.3f}")
    print(f"Recall:    {avg_recall:.3f}")
    print(f"MRR:       {mrr:.3f}")

    print("=" * 70)


if __name__ == "__main__":
    evaluate_retriever(top_k=3)