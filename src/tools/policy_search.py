from pathlib import Path
import sys

# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from retrieval.retriever import Retriever


class PolicySearchTool:
    """
    Tool for searching policy-related information
    in the enterprise knowledge base.
    """

    def __init__(self, top_k=5):
        self.retriever = Retriever(top_k=top_k)

    def search(self, query):
        """
        Search the knowledge base for policy-related information.

        Args:
            query (str): Policy-related user question.

        Returns:
            list: Relevant policy results.
        """

        if not query or not query.strip():
            return []

        results = self.retriever.search(query.strip())

        policy_results = []

        for result in results:
            metadata = result.get("metadata", {})

            source = metadata.get("source", "").lower()
            category = metadata.get("category", "").lower()

            # Policy-related documents/categories
            if (
                "policy" in source
                or category in {"hr", "it", "support", "products"}
            ):
                policy_results.append(
                    {
                        "score": result.get("score"),
                        "content": result.get("content"),
                        "source": metadata.get("source", "Unknown"),
                        "category": metadata.get("category", "Unknown"),
                        "page": metadata.get("page_number", "Unknown"),
                    }
                )

        return policy_results


def policy_search(query, top_k=5):
    """
    Simple function interface for the policy search tool.
    """

    tool = PolicySearchTool(top_k=top_k)

    return tool.search(query)


if __name__ == "__main__":

    tool = PolicySearchTool(top_k=5)

    test_queries = [
        "What is the leave policy?",
        "How many sick leave days are available?",
        "What are the work from home rules?",
    ]

    print("\n" + "=" * 70)
    print("POLICY SEARCH TOOL TEST")
    print("=" * 70)

    for query in test_queries:

        print("\n" + "-" * 70)
        print(f"QUERY: {query}")
        print("-" * 70)

        results = tool.search(query)

        print(f"Results found: {len(results)}")

        for index, result in enumerate(results, start=1):

            print(f"\nRESULT {index}")

            print(f"Score    : {result['score']:.4f}")
            print(f"Source   : {result['source']}")
            print(f"Category : {result['category']}")
            print(f"Page     : {result['page']}")

            print("\nContent:")
            print(result["content"][:500])