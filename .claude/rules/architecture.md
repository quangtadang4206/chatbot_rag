---
description: Cấu trúc thư mục và luồng dữ liệu từ upload đến câu trả lời
---

# Kiến trúc & Luồng dữ liệu

## Cấu trúc thư mục

```
├── app.py                  # Streamlit UI — điểm vào chính
├── rag/
│   ├── loader.py           # Load PDF, DOCX → List[Document]
│   ├── chunking.py         # Chia văn bản (semantic / recursive / fixed)
│   ├── vector_store.py     # ChromaDB: lưu và load embeddings
│   ├── retriever.py        # Truy xuất (mmr / similarity / threshold)
│   └── chain.py            # RAG chain LCEL + 2 loại prompt
├── data/
│   ├── raw/                # File upload tạm — không commit
│   └── chroma_db/          # Vector store persistent — không commit
├── .env                    # API keys — KHÔNG commit
├── .env.example            # Template để setup
└── requirements.txt
```

## Luồng dữ liệu

```
Upload file (PDF/DOCX)
    ↓ loader.py       — load_document()
List[Document]
    ↓ chunking.py     — split_documents(strategy)
List[Document] (chunks)
    ↓ vector_store.py — add_documents()
ChromaDB (lưu trên disk)
    ↓ retriever.py    — get_retriever(strategy)
VectorStoreRetriever
    ↓ chain.py        — create_rag_chain(prompt_type)
RAG Chain (LCEL)
    ↓ app.py          — chain.stream(question)
Câu trả lời streaming → Streamlit UI
```

## Quy tắc phân tách trách nhiệm

- Module `rag/` không được import bất kỳ thứ gì từ `app.py`
- `app.py` chỉ gọi các hàm public của `rag/`, không chứa logic RAG
- `data/` không được commit vào git
