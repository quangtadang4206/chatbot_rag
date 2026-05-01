---
description: Hướng dẫn thêm chiến lược chunking, retrieval hoặc prompt type mới
---

# Thêm chiến lược mới

Giao diện Streamlit tự động đọc từ `STRATEGY_MAP` và `STRATEGY_LABELS` — không cần sửa `app.py` khi thêm chiến lược mới.

## Thêm chiến lược chunking mới

Sửa file `rag/chunking.py`:

1. Viết hàm mới:
   ```python
   def chunk_ten_moi(docs: List[Document]) -> List[Document]:
       # logic chia văn bản
       ...
   ```
2. Đăng ký vào hai dict:
   ```python
   STRATEGY_MAP["ten_moi"] = chunk_ten_moi
   STRATEGY_LABELS["ten_moi"] = "Tên hiển thị — mô tả ngắn khi nào dùng"
   ```

## Thêm chiến lược retrieval mới

Sửa file `rag/retriever.py` — cùng quy trình:

1. Viết hàm `get_ten_moi_retriever(vectorstore, **kwargs) -> VectorStoreRetriever`
2. Thêm vào `STRATEGY_MAP` và `STRATEGY_LABELS`

## Thêm prompt type mới

Sửa file `rag/chain.py`:

1. Tạo `ChatPromptTemplate` mới:
   ```python
   PROMPT_TEN_MOI = ChatPromptTemplate.from_messages([...])
   ```
2. Thêm vào `PROMPT_MAP` và `PROMPT_LABELS`

## Lưu ý

- Key trong `STRATEGY_MAP` phải là string viết thường, không dấu cách (dùng `_` nếu cần)
- Luôn giữ một strategy làm mặc định rõ ràng trong `split_documents()` / `get_retriever()` / `create_rag_chain()`
