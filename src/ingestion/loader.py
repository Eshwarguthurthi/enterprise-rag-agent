from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader


BASE_DIR = Path(__file__).resolve().parents[2]
DATA_DIR = BASE_DIR / "data" / "raw"


CATEGORY_FOLDERS = [
    "hr",
    "it",
    "support",
    "products",
]


def load_pdf(file_path: Path):
    """Load a single PDF using LangChain's PyPDFLoader."""

    loader = PyPDFLoader(str(file_path))
    documents = loader.load()

    category = file_path.parent.name

    for document in documents:
        document.metadata["source"] = file_path.name
        document.metadata["filename"] = file_path.name
        document.metadata["category"] = category

        # PyPDFLoader already provides page information.
        if "page" in document.metadata:
            document.metadata["page_number"] = (
                document.metadata["page"] + 1
            )

    return documents


def load_all_documents():
    """Load all PDFs from the knowledge base."""

    all_documents = []

    for category in CATEGORY_FOLDERS:

        category_path = DATA_DIR / category

        if not category_path.exists():
            print(f"Warning: {category_path} does not exist.")
            continue

        pdf_files = list(category_path.glob("*.pdf"))

        for pdf_file in pdf_files:

            print(f"Loading: {category}/{pdf_file.name}")

            documents = load_pdf(pdf_file)

            all_documents.extend(documents)

            print(
                f"  Pages loaded: {len(documents)}"
            )

    return all_documents


if __name__ == "__main__":

    documents = load_all_documents()

    print("\n" + "=" * 60)
    print("DOCUMENT LOADING SUMMARY")
    print("=" * 60)

    print(f"Total pages loaded: {len(documents)}")

    if documents:

        print("\nFirst document:")
        print("-" * 60)

        print("Content:")
        print(documents[0].page_content[:500])

        print("\nMetadata:")
        print(documents[0].metadata)