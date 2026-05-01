import os
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
COLLECTION_NAME = "tai_lieu_rag"


def _get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-small")


def add_documents(chunks: List[Document]) -> Chroma:
    """Xoá collection cũ và tạo mới từ danh sách chunks."""
    embeddings = _get_embeddings()

    # Xoá collection cũ nếu tồn tại
    if os.path.exists(CHROMA_DIR):
        import shutil
        shutil.rmtree(CHROMA_DIR)

    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )
    return vectorstore


def get_vectorstore() -> Chroma:
    """Load vector store đã được lưu trên disk."""
    embeddings = _get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
