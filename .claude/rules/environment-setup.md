---
description: Cài đặt môi trường, biến môi trường và cách chạy ứng dụng
---

# Môi trường & Cài đặt

## Cài đặt lần đầu

```bash
pip install -r requirements.txt
cp .env.example .env
# Mở .env và điền OPENAI_API_KEY
```

## Chạy ứng dụng

```bash
streamlit run app.py
```

## Biến môi trường

| Biến | Bắt buộc | Mô tả |
|------|----------|-------|
| `OPENAI_API_KEY` | ✅ | OpenAI API key — dùng cho cả LLM và embeddings |

## Quy tắc bảo mật

- File `.env` tuyệt đối **không được commit** vào git
- Chỉ commit `.env.example` (không chứa key thật)
- Thư mục `data/` không commit (đã có trong `.gitignore`)
- Khi thêm biến môi trường mới, luôn cập nhật `.env.example` cùng lúc
