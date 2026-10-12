from pathlib import Path
import sys

# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from retrieval.retriever import Retriever


class KnowledgeSearchTool:
    """
    Tool for searching the enterprise knowledge base.

    This tool uses the existing FAISS-based Retriever
    and returns relevant knowledge base documents.
    """

    def __init__(self, top_k=3):
        self.retriever = Retriever(top_k=top_k)

    def search(self, query):
        """
        Search the knowledge base.

        Args:
            query (str): User's search question.

        Returns:
            list: Relevant knowledge base results.
        """

        if not query or not query.strip():
            return []

        results = self.retriever.search(query.strip())

        formatted_results = []

        for result in results:
            metadata = result.get("metadata", {})

            formatted_results.append(
                {
                    "score": result.get("score"),
                    "content": result.get("content"),
                    "source": metadata.get("source", "Unknown"),
                    "category": metadata.get("category", "Unknown"),
                    "page": metadata.get("page_number", "Unknown"),
                }
            )

        return formatted_results


def knowledge_search(query, top_k=3):
    """
    Simple function interface for the knowledge search tool.
    """

    tool = KnowledgeSearchTool(top_k=top_k)

    return tool.search(query)


if __name__ == "__main__":

    tool = KnowledgeSearchTool(top_k=3)

    test_query = "How many casual leave days do employees get?"

    print("\n" + "=" * 70)
    print("KNOWLEDGE SEARCH TOOL TEST")
    print("=" * 70)

    print(f"\nQuery:")
    print(test_query)

    results = tool.search(test_query)

    print(f"\nResults found: {len(results)}")

    for index, result in enumerate(results, start=1):

        print("\n" + "-" * 70)
        print(f"RESULT {index}")
        print("-" * 70)

        print(f"Score    : {result['score']:.4f}")
        print(f"Source   : {result['source']}")
        print(f"Category : {result['category']}")
        print(f"Page     : {result['page']}")

        print("\nContent:")
        print(result["content"])