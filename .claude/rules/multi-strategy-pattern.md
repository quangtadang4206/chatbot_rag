---
description: Nguyên tắc thiết kế multi-strategy — các chiến lược chunking, retrieval và prompt hiện có
---

# Multi-Strategy Pattern

Mỗi module trong `rag/` hỗ trợ **nhiều phương pháp** thông qua tham số `strategy` hoặc `prompt_type`. Không hardcode một cách duy nhất — người dùng chọn chiến lược trực tiếp trên Sidebar của Streamlit.

## Chunking — `rag/chunking.py`

Dispatcher: `split_documents(docs, strategy="recursive")`

| Strategy | Hàm | Khi nào dùng |
|----------|-----|-------------|
| `"semantic"` | `chunk_semantic()` | Báo cáo, hợp đồng, văn xuôi dài |
| `"recursive"` | `chunk_recursive()` | Tài liệu tổng quát **(mặc định)** |
| `"fixed"` | `chunk_fixed()` | FAQ, quy trình, bảng biểu |

## Retrieval — `rag/retriever.py`

Dispatcher: `get_retriever(vectorstore, strategy="mmr")`

| Strategy | Hàm | Khi nào dùng |
|----------|-----|-------------|
| `"mmr"` | `get_mmr_retriever()` | Tài liệu dài, tránh kết quả trùng lặp **(mặc định)** |
| `"similarity"` | `get_similarity_retriever()` | Q&A đơn giản, FAQ |
| `"threshold"` | `get_threshold_retriever()` | Cần lọc kết quả có độ tin cậy thấp |

## Prompt — `rag/chain.py`

Dispatcher: `create_rag_chain(retriever, prompt_type="general")`

| Type | Khi nào dùng |
|------|-------------|
| `"general"` | Trả lời linh hoạt từ tài liệu **(mặc định)** |
| `"strict"` | Chỉ dựa đúng tài liệu, không suy luận thêm |

## Quy tắc khi làm việc với pattern này

- Mỗi strategy phải có mặt trong cả `STRATEGY_MAP` và `STRATEGY_LABELS` — thiếu một trong hai thì Sidebar sẽ không hiển thị đúng
- Label trong `STRATEGY_LABELS` phải đủ rõ để người dùng cuối hiểu, không dùng tên kỹ thuật thuần túy
- Dispatcher luôn raise `ValueError` với thông báo tiếng Việt nếu `strategy` không hợp lệ
