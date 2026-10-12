from pathlib import Path
import os
import sys
import time

from dotenv import load_dotenv
import cohere


# ============================================================
# PATH CONFIGURATION
# ============================================================

SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ============================================================
# IMPORT TOOLS
# ============================================================

from tools.knowledge_search import KnowledgeSearchTool
from tools.policy_search import PolicySearchTool
from tools.document_summary import DocumentSummaryTool


# ============================================================
# ENVIRONMENT CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]

load_dotenv(BASE_DIR / ".env")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY is not configured in the .env file."
    )


# ============================================================
# COHERE CLIENT
# ============================================================

client = cohere.ClientV2(
    api_key=COHERE_API_KEY
)


# ============================================================
# RAG AGENT
# ============================================================

class RAGAgent:
    """
    Enterprise RAG Agent.

    The agent:
    1. Receives a user question.
    2. Selects an appropriate tool.
    3. Executes the selected tool.
    4. Generates a grounded answer.
    5. Returns source information.
    """

    def __init__(self):

        print("Initializing RAG Agent...")

        self.knowledge_search_tool = KnowledgeSearchTool(
            top_k=3
        )

        self.policy_search_tool = PolicySearchTool(
            top_k=5
        )

        self.document_summary_tool = DocumentSummaryTool()

        print("RAG Agent initialized successfully.")

    # ========================================================
    # COHERE CALL HELPER
    # ========================================================

    def cohere_chat(self, messages, max_retries=2):
        """
        Call Cohere with basic retry handling.

        Handles temporary rate-limit errors without
        crashing the entire Agent.
        """

        for attempt in range(max_retries + 1):

            try:

                response = client.chat(
                    model="command-r7b-12-2024",
                    messages=messages
                )

                return response

            except Exception as error:

                error_text = str(error)

                # ------------------------------------------------
                # Rate limit
                # ------------------------------------------------

                if "429" in error_text:

                    if attempt < max_retries:

                        wait_time = 5 * (attempt + 1)

                        print(
                            f"\nCohere rate limit reached."
                            f" Waiting {wait_time} seconds..."
                        )

                        time.sleep(wait_time)

                        continue

                    print(
                        "\nCohere API rate limit reached."
                    )

                    raise

                # ------------------------------------------------
                # Other API errors
                # ------------------------------------------------

                raise

        raise RuntimeError(
            "Cohere API request failed."
        )

    # ========================================================
    # KNOWLEDGE SEARCH
    # ========================================================

    def knowledge_search(self, query):

        return self.knowledge_search_tool.search(
            query
        )

    # ========================================================
    # POLICY SEARCH
    # ========================================================

    def policy_search(self, query):

        return self.policy_search_tool.search(
            query
        )

    # ========================================================
    # DOCUMENT SUMMARY
    # ========================================================

    def document_summary(self, content, source):

        return self.document_summary_tool.summarize(
            content=content,
            source=source
        )

    # ========================================================
    # TOOL SELECTION
    # ========================================================

    def select_tool(self, question):
        """
        Select the most appropriate tool for the question.
        """

        router_prompt = f"""
You are a routing assistant for an enterprise knowledge base.

Choose exactly ONE tool.

Available tools:

knowledge_search
- Use for general questions about information
  stored in the enterprise knowledge base.
- Use for IT support, account information,
  password reset, product information, support
  information, and general knowledge questions.

policy_search
- Use for questions specifically about policies,
  rules, procedures, eligibility, approvals,
  requirements, leave, work from home,
  employee policies, support escalation policies,
  warranty policies, and similar policy information.

document_summary
- Use when the user explicitly asks to summarize
  a document or policy.

Return ONLY one of:

knowledge_search
policy_search
document_summary

User question:
{question}
"""

        response = self.cohere_chat(
            messages=[
                {
                    "role": "user",
                    "content": router_prompt
                }
            ]
        )

        selected_tool = (
            response.message.content[0].text
            .strip()
            .lower()
        )

        valid_tools = {
            "knowledge_search",
            "policy_search",
            "document_summary"
        }

        if selected_tool not in valid_tools:

            selected_tool = "knowledge_search"

        return selected_tool

    # ========================================================
    # FORMAT SEARCH RESULTS
    # ========================================================

    def format_search_results(self, results):

        if not results:

            return (
                "No relevant information was found "
                "in the knowledge base."
            )

        context_parts = []

        for index, result in enumerate(
            results,
            start=1
        ):

            score = result.get(
                "score",
                0
            )

            context_parts.append(
                f"""
SOURCE {index}

Document:
{result.get("source", "Unknown")}

Category:
{result.get("category", "Unknown")}

Page:
{result.get("page", "Unknown")}

Similarity Score:
{score:.4f}

Content:
{result.get("content", "")}
"""
            )

        return "\n".join(
            context_parts
        )

    # ========================================================
    # GENERATE FINAL ANSWER
    # ========================================================

    def generate_answer(
        self,
        question,
        tool_name,
        tool_result
    ):
        """
        Generate final grounded answer.
        """

        if tool_name == "document_summary":

            context = tool_result

        else:

            context = self.format_search_results(
                tool_result
            )

        prompt = f"""
You are an enterprise knowledge base assistant.

Answer the user's question using ONLY the
knowledge base information provided below.

Rules:

1. Use only the provided information.
2. Do not use outside knowledge.
3. Do not invent facts.
4. Do not make assumptions.
5. If the answer is not available, say exactly:
   "I could not find this information in the knowledge base."
6. Keep the answer clear and concise.
7. Preserve important numbers, rules,
   requirements, and procedures.
8. When appropriate, mention the source document.
9. Do not claim information that is not present
   in the provided context.

Selected tool:
{tool_name}

Knowledge base information:
{context}

User question:
{question}

Answer:
"""

        response = self.cohere_chat(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return (
            response.message.content[0].text
            .strip()
        )

    # ========================================================
    # ASK
    # ========================================================

    def ask(self, question):
        """
        Main Agent entry point.
        """

        if not question or not question.strip():

            return {
                "question": question,
                "tool": None,
                "answer": "Please provide a question.",
                "sources": []
            }

        question = question.strip()

        # ----------------------------------------------------
        # Step 1: Select tool
        # ----------------------------------------------------

        selected_tool = self.select_tool(
            question
        )

        print(
            f"\nSelected tool: {selected_tool}"
        )

        # ----------------------------------------------------
        # Step 2: Execute selected tool
        # ----------------------------------------------------

        if selected_tool == "knowledge_search":

            results = self.knowledge_search(
                question
            )

            answer = self.generate_answer(
                question=question,
                tool_name=selected_tool,
                tool_result=results
            )

        elif selected_tool == "policy_search":

            results = self.policy_search(
                question
            )

            answer = self.generate_answer(
                question=question,
                tool_name=selected_tool,
                tool_result=results
            )

        elif selected_tool == "document_summary":

            # First search for the relevant document.
            results = self.knowledge_search(
                question
            )

            if results:

                best_result = results[0]

                summary = self.document_summary(
                    content=best_result.get(
                        "content",
                        ""
                    ),
                    source=best_result.get(
                        "source",
                        "Unknown"
                    )
                )

                answer = summary

            else:

                answer = (
                    "I could not find this information "
                    "in the knowledge base."
                )

        else:

            results = []

            answer = (
                "I could not find this information "
                "in the knowledge base."
            )

        # ----------------------------------------------------
        # Step 3: Build sources
        # ----------------------------------------------------

        sources = []

        if selected_tool == "document_summary":

            if results:

                best_result = results[0]

                sources.append(
                    {
                        "source": best_result.get(
                            "source"
                        ),
                        "category": best_result.get(
                            "category"
                        ),
                        "page": best_result.get(
                            "page"
                        ),
                        "score": best_result.get(
                            "score"
                        )
                    }
                )

        else:

            for result in results:

                sources.append(
                    {
                        "source": result.get(
                            "source"
                        ),
                        "category": result.get(
                            "category"
                        ),
                        "page": result.get(
                            "page"
                        ),
                        "score": result.get(
                            "score"
                        )
                    }
                )

        # ----------------------------------------------------
        # Step 4: Return response
        # ----------------------------------------------------

        return {
            "question": question,
            "tool": selected_tool,
            "answer": answer,
            "sources": sources
        }


# ============================================================
# COMPREHENSIVE TEST
# ============================================================

if __name__ == "__main__":

    agent = RAGAgent()

    test_questions = [
        {
            "category": "HR POLICY",
            "question": "How many casual leave days do employees get?"
        },
        {
            "category": "HR POLICY",
            "question": "What are the work from home rules?"
        },
        {
            "category": "IT SUPPORT",
            "question": "How do I reset my password?"
        },
        {
            "category": "SUPPORT",
            "question": "How should a critical support ticket be escalated?"
        },
        {
            "category": "PRODUCT",
            "question": "What is the warranty period for the product?"
        },
        {
            "category": "DOCUMENT SUMMARY",
            "question": "Summarize the employee leave policy."
        },
        {
            "category": "UNKNOWN INFORMATION",
            "question": "What is the maternity leave policy?"
        },
        {
            "category": "UNKNOWN INFORMATION",
            "question": "What is the employee salary structure?"
        }
    ]

    print("\n")
    print("=" * 80)
    print("ENTERPRISE RAG AGENT - COMPREHENSIVE TEST")
    print("=" * 80)

    passed = 0
    failed = 0

    for index, test in enumerate(
        test_questions,
        start=1
    ):

        question = test["question"]
        category = test["category"]

        print("\n")
        print("#" * 80)
        print(f"TEST {index}")
        print(f"CATEGORY : {category}")
        print(f"QUESTION : {question}")
        print("#" * 80)

        try:

            result = agent.ask(
                question
            )

            print("\nSelected Tool:")
            print(result["tool"])

            print("\nAnswer:")
            print(result["answer"])

            print("\nSources:")

            if result["sources"]:

                for source in result["sources"]:

                    score = source.get(
                        "score",
                        0
                    )

                    print(
                        f"- {source['source']} | "
                        f"{source['category']} | "
                        f"Page {source['page']} | "
                        f"Score: {score:.4f}"
                    )

            else:

                print(
                    "- No sources found."
                )

            # ------------------------------------------------
            # Basic validation
            # ------------------------------------------------

            if result["answer"].strip():

                passed += 1

                print(
                    "\nSTATUS: PASS"
                )

            else:

                failed += 1

                print(
                    "\nSTATUS: FAIL"
                )

        except Exception as error:

            failed += 1

            print(
                "\nSTATUS: FAIL"
            )

            print(
                f"ERROR: {error}"
            )

    # ========================================================
    # TEST SUMMARY
    # ========================================================

    print("\n")
    print("=" * 80)
    print("TEST SUMMARY")
    print("=" * 80)

    print(
        f"Total tests : {len(test_questions)}"
    )

    print(
        f"Passed      : {passed}"
    )

    print(
        f"Failed      : {failed}"
    )

    print("\n")

    if failed == 0:

        print(
            "ALL AGENT TESTS PASSED"
        )

    else:

        print(
            "SOME AGENT TESTS FAILED"
        )

    print("=" * 80)