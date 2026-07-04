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
    retriever = SemanticRetriever(embedder=embedder, vector_store=store)

    if store.count() == 0:
        _index(retriever)

    return retriever


def _index(retriever: SemanticRetriever) -> None:
    loader = DirectoryLoader(_DOCS_DIR, glob="**/*.md")
    splitter = RecursiveTextSplitter(chunk_size=400, overlap=50)

    documents = loader.load()
    chunks = []
    for doc in documents:
        chunks.extend(splitter.split(doc))

    retriever.add(chunks)


def load() -> None:
    """Force re-index docs/ into ChromaDB."""
    retriever = build_retriever()
    _index(retriever)
    print(f"Indexed docs from {_DOCS_DIR} into ChromaDB.")


if __name__ == "__main__":
    load()
