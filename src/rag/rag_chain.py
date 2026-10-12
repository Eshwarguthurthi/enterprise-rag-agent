from pathlib import Path
import os
import sys

from dotenv import load_dotenv
import cohere


# --------------------------------------------------
# Add src directory to Python path
# --------------------------------------------------

SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# --------------------------------------------------
# Project imports
# --------------------------------------------------

from retrieval.retriever import Retriever
from rag.prompts import SYSTEM_PROMPT, build_rag_prompt
from rag.memory import ConversationMemory


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

client = cohere.ClientV2(
    api_key=COHERE_API_KEY
)


# --------------------------------------------------
# RAG Chain
# --------------------------------------------------

class RAGChain:

    def __init__(self, top_k=3):

        self.retriever = Retriever(top_k=top_k)
        self.memory = ConversationMemory()


    # --------------------------------------------------
    # Rewrite follow-up question
    # --------------------------------------------------

    def rewrite_question(self, question):

        history = self.memory.format_history()

        # No previous conversation
        if not self.memory.get_history():
            return question

        rewrite_prompt = f"""
You are a query rewriting assistant.

Rewrite the user's latest question into a standalone question
that can be understood without the previous conversation.

Use the conversation history to resolve words such as:
"it", "this", "that", "they", "them", "there", etc.

Do not answer the question.
Only return the rewritten standalone question.

Previous conversation:
{history}

Latest user question:
{question}

Standalone question:
"""

        response = client.chat(
            model="command-r7b-12-2024",
            messages=[
                {
                    "role": "user",
                    "content": rewrite_prompt
                }
            ]
        )

        rewritten = response.message.content[0].text.strip()

        return rewritten


    # --------------------------------------------------
    # Build context
    # --------------------------------------------------

    def build_context(self, results):

        context_parts = []

        for index, result in enumerate(results, start=1):

            metadata = result["metadata"]

            source = metadata.get(
                "source",
                "Unknown"
            )

            category = metadata.get(
                "category",
                "Unknown"
            )

            page = metadata.get(
                "page_number",
                "Unknown"
            )

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


    # --------------------------------------------------
    # Ask question
    # --------------------------------------------------

    def ask(self, question):

        # ------------------------------------------
        # Rewrite using conversation history
        # ------------------------------------------

        standalone_question = self.rewrite_question(
            question
        )

        print(
            f"\nRewritten question: "
            f"{standalone_question}"
        )


        # ------------------------------------------
        # Retrieve using rewritten question
        # ------------------------------------------

        results = self.retriever.search(
            standalone_question
        )


        # ------------------------------------------
        # Store original user message
        # ------------------------------------------

        self.memory.add_user_message(question)


        # ------------------------------------------
        # No relevant result
        # ------------------------------------------

        if not results:

            answer = (
                "I could not find this information "
                "in the knowledge base."
            )

            self.memory.add_assistant_message(answer)

            return {
                "answer": answer,
                "sources": []
            }


        # ------------------------------------------
        # Build context
        # ------------------------------------------

        context = self.build_context(results)


        # ------------------------------------------
        # Conversation history
        # ------------------------------------------

        history = self.memory.format_history()


        # ------------------------------------------
        # Build RAG prompt
        # ------------------------------------------

        user_prompt = f"""
Previous Conversation:

{history}

{build_rag_prompt(
    standalone_question,
    context
)}
"""


        # ------------------------------------------
        # Generate answer
        # ------------------------------------------

        response = client.chat(
            model="command-r7b-12-2024",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": user_prompt
                }
            ]
        )


        answer = response.message.content[0].text


        # ------------------------------------------
        # Store assistant response
        # ------------------------------------------

        self.memory.add_assistant_message(answer)


        # ------------------------------------------
        # Sources
        # ------------------------------------------

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
# Test conversational RAG
# --------------------------------------------------

if __name__ == "__main__":

    rag = RAGChain(top_k=3)


    # ==================================================
    # QUESTION 1
    # ==================================================

    question1 = "How many casual leave days do employees get?"

    result1 = rag.ask(question1)

    print("\n" + "=" * 70)
    print("CONVERSATION TEST")
    print("=" * 70)

    print("\nUser:")
    print(question1)

    print("\nAssistant:")
    print(result1["answer"])


    # ==================================================
    # QUESTION 2
    # ==================================================

    question2 = "How do I apply for it?"

    result2 = rag.ask(question2)

    print("\nUser:")
    print(question2)

    print("\nAssistant:")
    print(result2["answer"])


    # ==================================================
    # SOURCES
    # ==================================================

    print("\n" + "=" * 70)
    print("SOURCES FOR QUESTION 2")
    print("=" * 70)

    for source in result2["sources"]:

        print(
            f"- {source['source']} | "
            f"{source['category']} | "
            f"Page {source['page']} | "
            f"Score: {source['score']:.4f}"
        )


    # ==================================================
    # MEMORY
    # ==================================================

    print("\n" + "=" * 70)
    print("CONVERSATION HISTORY")
    print("=" * 70)

    print(rag.memory.format_history())