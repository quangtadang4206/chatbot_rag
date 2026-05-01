import os
import shutil
import tempfile
from typing import List
from langchain_core.documents import Document
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

CHROMA_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "chroma_db")
COLLECTION_NAME = "tai_lieu_rag"


def _get_embeddings() -> OpenAIEmbeddings:
    return OpenAIEmbeddings(model="text-embedding-3-small")


def add_documents(chunks: List[Document]) -> Chroma:
    """Ghi dữ liệu mới vào thư mục tạm, chỉ swap khi thành công — tránh mất dữ liệu nếu lỗi giữa chừng."""
    embeddings = _get_embeddings()
    parent_dir = os.path.dirname(os.path.abspath(CHROMA_DIR))
    os.makedirs(parent_dir, exist_ok=True)
    tmp_dir = tempfile.mkdtemp(dir=parent_dir, prefix="chroma_tmp_")
    try:
        Chroma.from_documents(
            documents=chunks,
            embedding=embeddings,
            collection_name=COLLECTION_NAME,
            persist_directory=tmp_dir,
        )
        if os.path.exists(CHROMA_DIR):
            shutil.rmtree(CHROMA_DIR)
        os.rename(tmp_dir, CHROMA_DIR)
        return Chroma(
            collection_name=COLLECTION_NAME,
            embedding_function=embeddings,
            persist_directory=CHROMA_DIR,
        )
    except Exception:
        shutil.rmtree(tmp_dir, ignore_errors=True)
        raise


def get_vectorstore() -> Chroma:
    """Load vector store đã được lưu trên disk."""
    embeddings = _get_embeddings()
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=embeddings,
        persist_directory=CHROMA_DIR,
    )
