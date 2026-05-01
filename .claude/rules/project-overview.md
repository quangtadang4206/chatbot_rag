---
description: Tổng quan dự án — mục đích, stack công nghệ và các file quan trọng
---

# Tổng quan dự án

Đây là ứng dụng **Chatbot RAG (Retrieval-Augmented Generation)** cho phép người dùng upload tài liệu PDF/DOCX và đặt câu hỏi về nội dung. Hệ thống tìm kiếm các đoạn văn liên quan trong tài liệu, sau đó dùng LLM để tổng hợp câu trả lời.

## Stack công nghệ

- **UI:** Streamlit (giao diện tiếng Việt)
- **LLM:** OpenAI GPT-4o-mini
- **Embeddings:** OpenAI text-embedding-3-small
- **Vector DB:** ChromaDB (persistent trên disk)
- **RAG framework:** LangChain LCEL
- **Ngôn ngữ:** Python

## Điểm vào chính

- `app.py` — Streamlit app, điểm khởi động duy nhất (`streamlit run app.py`)
- `rag/` — Toàn bộ logic RAG, tách biệt hoàn toàn khỏi UI
