"""RAG utilities for resume advice."""

from functools import lru_cache

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from career_advisor.config import RESUME_TIPS_PATH


@lru_cache(maxsize=1)
def build_resume_db():
    """Build a small FAISS index from the local resume tips manual."""
    if not RESUME_TIPS_PATH.exists():
        return None

    resume_tips = RESUME_TIPS_PATH.read_text(encoding="utf-8").strip()
    if not resume_tips:
        return None

    docs = [Document(page_content=resume_tips)]
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(docs)
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )
    return FAISS.from_documents(chunks, embeddings)


def search_resume_tips(query: str, k: int = 3) -> str:
    """Return relevant resume advice context for a user resume/profile."""
    db = build_resume_db()
    if not db or not query.strip():
        return ""

    relevant = db.similarity_search(query, k=k)
    return "\n\n".join(doc.page_content for doc in relevant)
