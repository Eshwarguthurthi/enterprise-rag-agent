from pathlib import Path
import os
import sys

from dotenv import load_dotenv
import cohere


# --------------------------------------------------
# Add src directory to Python path
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(SRC_DIR))


from retrieval.retriever import Retriever


# --------------------------------------------------
# Load environment variables
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY is not configured in the .env file."
    )


# --------------------------------------------------
# Cohere client
# --------------------------------------------------

cohere_client = cohere.ClientV2(
    api_key=COHERE_API_KEY
)


# --------------------------------------------------
# RAG Generator
# --------------------------------------------------

class RAGGenerator:

    def __init__(self, top_k=3):

        self.retriever = Retriever(top_k=top_k)

    def build_context(self, results):

        context_parts = []

        for index, result in enumerate(results, start=1):

            metadata = result["metadata"]

            source = metadata.get("source", "Unknown")
            category = metadata.get("category", "Unknown")
            page = metadata.get("page_number", "Unknown")

            context_parts.append(
                f"""
SOURCE {index}
Document: {source}
Category: {category}
Page: {page}

Content:
{result["content"]}
"""
            )

        return "\n".join(context_parts)

    def generate_answer(self, question):

        # --------------------------------------------------
        # Retrieve relevant documents
        # --------------------------------------------------

        results = self.retriever.search(question)

        if not results:
            return {
                "answer": (
                    "I could not find relevant information "
                    "in the knowledge base."
                ),
                "sources": []
            }

        # --------------------------------------------------
        # Build context
        # --------------------------------------------------

        context = self.build_context(results)

        # --------------------------------------------------
        # RAG prompt
        # --------------------------------------------------

        system_message = """
You are an enterprise knowledge base assistant.

Answer the user's question using ONLY the provided context.

Rules:
1. Do not use outside knowledge.
2. Do not invent information.
3. If the answer is not present in the context, say:
   "I could not find this information in the knowledge base."
4. Keep the answer clear and concise.
5. When answering, mention the relevant source document.
"""

        user_message = f"""
Context:

{context}

User Question:
{question}
"""

        # --------------------------------------------------
        # Generate answer using Cohere
        # --------------------------------------------------

        response = cohere_client.chat(
            model="command-r7b-12-2024",
            messages=[
                {
                    "role": "system",
                    "content": system_message
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ]
        )

        answer = response.message.content[0].text

        # --------------------------------------------------
        # Prepare source information
        # --------------------------------------------------

        sources = []

        for result in results:

            metadata = result["metadata"]

            sources.append({
                "source": metadata.get("source"),
                "category": metadata.get("category"),
                "page": metadata.get("page_number"),
                "score": result["score"]
            })

        return {
            "answer": answer,
            "sources": sources
        }


# --------------------------------------------------
# Test RAG
# --------------------------------------------------

if __name__ == "__main__":

    rag = RAGGenerator(top_k=3)

    test_questions = [
        "How many casual leave days do employees get?",
        "How do I reset my password?",
        "What is the warranty period for the product?",
        "What is the company's maternity leave policy?"
    ]

    for question in test_questions:

        print("\n" + "=" * 70)
        print("QUESTION")
        print("=" * 70)

        print(question)

        result = rag.generate_answer(question)

        print("\nANSWER")
        print("-" * 70)

        print(result["answer"])

        print("\nSOURCES")
        print("-" * 70)

        for source in result["sources"]:

            print(
                f"{source['source']} | "
                f"{source['category']} | "
                f"Page {source['page']} | "
                f"Score: {source['score']:.4f}"
            )