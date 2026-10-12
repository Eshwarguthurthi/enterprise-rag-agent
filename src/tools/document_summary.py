from pathlib import Path
import os
import sys

from dotenv import load_dotenv
import cohere


# Add src directory to Python path
SRC_DIR = Path(__file__).resolve().parents[1]

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# Load environment variables
BASE_DIR = Path(__file__).resolve().parents[2]
load_dotenv(BASE_DIR / ".env")

COHERE_API_KEY = os.getenv("COHERE_API_KEY")

if not COHERE_API_KEY:
    raise ValueError(
        "COHERE_API_KEY is not configured in the .env file."
    )


client = cohere.ClientV2(api_key=COHERE_API_KEY)


class DocumentSummaryTool:
    """
    Tool for summarizing enterprise knowledge base content.
    """

    def summarize(self, content, source="Unknown"):
        """
        Summarize the provided document content.

        Args:
            content (str): Document content to summarize.
            source (str): Source document name.

        Returns:
            str: Concise summary.
        """

        if not content or not content.strip():
            return "No document content was provided."

        prompt = f"""
You are an enterprise document summarization assistant.

Summarize the following knowledge base document.

Rules:
1. Use ONLY the provided document content.
2. Do not add outside information.
3. Do not invent facts.
4. Keep the summary concise.
5. Preserve important rules, numbers, requirements, and procedures.
6. If the document contains multiple sections, summarize the important points.
7. Mention the document name in the summary.

Document:
{source}

Content:
{content}

Summary:
"""

        response = client.chat(
            model="command-r7b-12-2024",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response.message.content[0].text.strip()


def document_summary(content, source="Unknown"):
    """
    Simple function interface for the document summary tool.
    """

    tool = DocumentSummaryTool()

    return tool.summarize(
        content=content,
        source=source
    )


if __name__ == "__main__":

    tool = DocumentSummaryTool()

    test_content = """
    Employee Leave Policy

    Employees are entitled to 12 casual leave days per calendar year.
    Employees are entitled to 10 sick leave days per calendar year.
    Employees receive 18 annual leave days per year.

    Leave requests should be submitted through the employee portal.
    Planned leave should normally be submitted at least two working days
    before the requested leave date.

    Emergency leave may be submitted after the absence when circumstances
    prevent advance submission.

    Manager approval is required and leave requests are subject
    to organizational requirements.
    """

    print("\n" + "=" * 70)
    print("DOCUMENT SUMMARY TOOL TEST")
    print("=" * 70)

    print("\nSource:")
    print("leave_policy.pdf")

    print("\nGenerating summary...")

    summary = tool.summarize(
        content=test_content,
        source="leave_policy.pdf"
    )

    print("\nSummary:")
    print(summary)