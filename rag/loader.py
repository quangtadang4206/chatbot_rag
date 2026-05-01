import os
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader


def load_pdf(file_path: str) -> List[Document]:
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    for doc in docs:
        doc.metadata["file_type"] = "pdf"
    return docs


def load_docx(file_path: str) -> List[Document]:
    loader = Docx2txtLoader(file_path)
    docs = loader.load()
    for doc in docs:
        doc.metadata["file_type"] = "docx"
    return docs


def load_document(file_path: str) -> List[Document]:
    ext = os.path.splitext(file_path)[-1].lower()
    if ext == ".pdf":
        return load_pdf(file_path)
    elif ext in (".docx", ".doc"):
        return load_docx(file_path)
    else:
        raise ValueError(f"Định dạng file không được hỗ trợ: {ext}. Vui lòng dùng PDF hoặc DOCX.")
