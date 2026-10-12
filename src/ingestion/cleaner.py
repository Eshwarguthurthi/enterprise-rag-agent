from pathlib import Path
import re

from ingestion.loader import load_all_documents


def clean_text(text: str) -> str:
    """
    Basic text cleaning.

    We intentionally avoid aggressive cleaning so that
    semantic information is preserved.
    """

    if not text:
        return ""

    # Normalize line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Remove spaces around line breaks
    text = re.sub(r" *\n *", "\n", text)

    return text.strip()


def inspect_documents(documents):
    """
    Inspect loaded documents before cleaning.
    """

    print("\n" + "=" * 70)
    print("DOCUMENT TEXT INSPECTION")
    print("=" * 70)

    empty_documents = []
    short_documents = []

    for index, document in enumerate(documents, start=1):

        text = document.page_content.strip()

        source = document.metadata.get(
            "source",
            "unknown"
        )

        category = document.metadata.get(
            "category",
            "unknown"
        )

        page = document.metadata.get(
            "page_number",
            "unknown"
        )

        character_count = len(text)

        print(f"\n[{index}] {source}")
        print(f"Category : {category}")
        print(f"Page     : {page}")
        print(f"Characters: {character_count}")

        if not text:
            empty_documents.append(source)

        if character_count < 100:
            short_documents.append(source)

    print("\n" + "-" * 70)

    print(f"Total documents/pages : {len(documents)}")
    print(f"Empty documents       : {len(empty_documents)}")
    print(f"Very short documents  : {len(short_documents)}")

    if empty_documents:
        print("\nEmpty documents:")
        for item in empty_documents:
            print(f"  - {item}")

    if short_documents:
        print("\nVery short documents:")
        for item in short_documents:
            print(f"  - {item}")


def clean_documents(documents):

    cleaned_documents = []

    for document in documents:

        original_text = document.page_content

        cleaned_text = clean_text(original_text)

        document.page_content = cleaned_text

        cleaned_documents.append(document)

    return cleaned_documents


if __name__ == "__main__":

    documents = load_all_documents()

    inspect_documents(documents)

    cleaned_documents = clean_documents(documents)

    print("\n" + "=" * 70)
    print("CLEANING COMPLETED")
    print("=" * 70)

    print(
        f"Documents cleaned: {len(cleaned_documents)}"
    )

    if cleaned_documents:

        print("\nSample cleaned document:")
        print("-" * 70)

        print(
            cleaned_documents[0].page_content[:1000]
        )