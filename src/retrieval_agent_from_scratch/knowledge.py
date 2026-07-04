from __future__ import annotations

from pathlib import Path

from sophons.embeddings import SentenceTransformerEmbeddings
from sophons.loaders import DirectoryLoader
from sophons.rag import RecursiveTextSplitter
from sophons.retrieval import SemanticRetriever
from sophons.stores import ChromaVectorStore

_DOCS_DIR = Path(__file__).parent.parent.parent / "docs"
_CHROMA_PATH = str(Path(__file__).parent.parent.parent / "chroma_db")
_COLLECTION = "company-docs"


def build_retriever() -> SemanticRetriever:
    embedder = SentenceTransformerEmbeddings()
    store = ChromaVectorStore(collection=_COLLECTION, path=_CHROMA_PATH)
    return SemanticRetriever(embedder=embedder, vector_store=store)


def load() -> None:
    """Load docs/ into ChromaDB. Run once before using retrieval-chat."""
    loader = DirectoryLoader(_DOCS_DIR, glob="**/*.md")
    splitter = RecursiveTextSplitter(chunk_size=400, overlap=50)

    documents = loader.load()
    if not documents:
        print(f"No documents found in {_DOCS_DIR}")
        return

    chunks = []
    for doc in documents:
        chunks.extend(splitter.split(doc))

    retriever = build_retriever()
    retriever.add(chunks)

    print(f"Loaded {len(documents)} documents → {len(chunks)} chunks into ChromaDB.")


if __name__ == "__main__":
    load()
