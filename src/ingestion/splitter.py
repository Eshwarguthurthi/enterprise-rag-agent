from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter

from ingestion.loader import load_all_documents
from ingestion.cleaner import clean_documents


def create_chunks(
    documents,
    chunk_size,
    chunk_overlap
):
    """
    Split documents into smaller chunks.

    Metadata from the original document is automatically
    preserved by LangChain.
    """

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=[
            "\n\n",
            "\n",
            ". ",
            " ",
            ""
        ]
    )

    chunks = splitter.split_documents(documents)

    return chunks


def inspect_chunks(chunks, experiment_name):

    print("\n" + "=" * 70)
    print(f"CHUNKING EXPERIMENT: {experiment_name}")
    print("=" * 70)

    print(f"Total chunks: {len(chunks)}")

    if not chunks:
        return

    lengths = [
        len(chunk.page_content)
        for chunk in chunks
    ]

    print(f"Minimum chunk length : {min(lengths)}")
    print(f"Maximum chunk length : {max(lengths)}")
    print(
        f"Average chunk length : "
        f"{sum(lengths) / len(lengths):.2f}"
    )

    print("\nFirst 3 chunks:")
    print("-" * 70)

    for index, chunk in enumerate(chunks[:3], start=1):

        print(f"\nChunk {index}")

        print(
            f"Source   : "
            f"{chunk.metadata.get('source')}"
        )

        print(
            f"Category : "
            f"{chunk.metadata.get('category')}"
        )

        print(
            f"Page     : "
            f"{chunk.metadata.get('page_number')}"
        )

        print(
            f"Length   : "
            f"{len(chunk.page_content)}"
        )

        print("\nContent:")
        print(chunk.page_content)


def run_experiments(documents):

    experiments = [
        {
            "name": "Experiment A",
            "chunk_size": 300,
            "chunk_overlap": 30,
        },
        {
            "name": "Experiment B",
            "chunk_size": 700,
            "chunk_overlap": 100,
        },
        {
            "name": "Experiment C",
            "chunk_size": 1200,
            "chunk_overlap": 150,
        },
    ]

    results = []

    for experiment in experiments:

        chunks = create_chunks(
            documents,
            experiment["chunk_size"],
            experiment["chunk_overlap"]
        )

        inspect_chunks(
            chunks,
            experiment["name"]
        )

        results.append({
            "name": experiment["name"],
            "chunk_size": experiment["chunk_size"],
            "chunk_overlap": experiment["chunk_overlap"],
            "total_chunks": len(chunks),
        })

    return results


if __name__ == "__main__":

    print("Loading documents...")

    documents = load_all_documents()

    print("\nCleaning documents...")

    documents = clean_documents(documents)

    results = run_experiments(documents)

    print("\n" + "=" * 70)
    print("EXPERIMENT SUMMARY")
    print("=" * 70)

    for result in results:

        print(
            f"{result['name']}: "
            f"size={result['chunk_size']}, "
            f"overlap={result['chunk_overlap']}, "
            f"chunks={result['total_chunks']}"
        )