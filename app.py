import os
import tempfile
import streamlit as st
from dotenv import load_dotenv

from rag.loader import load_document
from rag.chunking import split_documents, STRATEGY_LABELS as CHUNK_LABELS
from rag.vector_store import add_documents, get_vectorstore
from rag.retriever import get_retriever, STRATEGY_LABELS as RETRIEVER_LABELS
from rag.chain import create_rag_chain, PROMPT_LABELS

load_dotenv()

st.set_page_config(
    page_title="Chatbot RAG",
    page_icon="🤖",
    layout="wide",
)

# --- Sidebar ---
with st.sidebar:
    st.title("⚙️ Cấu hình")

    st.subheader("📄 Tải tài liệu")
    uploaded_files = st.file_uploader(
        "Chọn file PDF hoặc DOCX",
        type=["pdf", "docx", "doc"],
        accept_multiple_files=True,
    )

    # Lưu bytes ngay khi upload — tránh mất data khi Streamlit rerun do widget khác thay đổi
    if uploaded_files:
        st.session_state["cached_files"] = [
            {"name": f.name, "suffix": os.path.splitext(f.name)[-1], "data": f.getvalue()}
            for f in uploaded_files
        ]

    st.subheader("🔧 Các tùy chọn xử lý")

    chunk_strategy = st.selectbox(
        "Các phương pháp chia văn bản",
        options=list(CHUNK_LABELS.keys()),
        format_func=lambda k: CHUNK_LABELS[k],
        index=1,  # mặc định: recursive
    )

    retriever_strategy = st.selectbox(
        "Các phương pháp truy xuất",
        options=list(RETRIEVER_LABELS.keys()),
        format_func=lambda k: RETRIEVER_LABELS[k],
        index=0,  # mặc định: mmr
    )

    prompt_type = st.selectbox(
        "Kiểu prompt",
        options=list(PROMPT_LABELS.keys()),
        format_func=lambda k: PROMPT_LABELS[k],
        index=0,  # mặc định: general
    )

    st.divider()

    process_btn = st.button("🚀 Xử lý tài liệu", use_container_width=True, type="primary")

    if process_btn:
        files_to_process = st.session_state.get("cached_files", [])
        if not files_to_process:
            st.warning("Vui lòng chọn ít nhất một file.")
        else:
            with st.spinner("Đang xử lý tài liệu..."):
                try:
                    all_docs = []
                    tmp_files = []
                    for file_data in files_to_process:
                        with tempfile.NamedTemporaryFile(delete=False, suffix=file_data["suffix"]) as tmp:
                            tmp.write(file_data["data"])
                            tmp_path = tmp.name
                        docs = load_document(tmp_path)
                        all_docs.extend(docs)
                        tmp_files.append(tmp_path)

                    # Chunking trước, xóa temp file sau — document-based strategy cần đọc lại file gốc
                    chunks = split_documents(all_docs, strategy=chunk_strategy)
                    for tmp_path in tmp_files:
                        os.unlink(tmp_path)
                    vectorstore = add_documents(chunks)
                    retriever = get_retriever(vectorstore, strategy=retriever_strategy, docs=chunks)
                    chain = create_rag_chain(retriever, prompt_type=prompt_type)

                    st.session_state["retriever"] = retriever
                    st.session_state["chain"] = chain
                    st.session_state["vectorstore_ready"] = True

                    st.success(f"✅ Đã xử lý {len(all_docs)} trang / {len(chunks)} đoạn văn bản.")
                except Exception as e:
                    st.error(f"Lỗi xử lý tài liệu: {e}")

    # Trạng thái vector store
    if st.session_state.get("vectorstore_ready"):
        st.success("📚 Tài liệu đã sẵn sàng")
    else:
        st.info("📭 Chưa có tài liệu nào được xử lý")

    st.divider()

    if st.button("🗑️ Xoá lịch sử trò chuyện", use_container_width=True):
        st.session_state["messages"] = []
        st.rerun()

# --- Main area ---
st.title("🤖 Chatbot RAG")
st.caption("Đặt câu hỏi về nội dung tài liệu bạn đã upload.")

# Khởi tạo session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []
if "vectorstore_ready" not in st.session_state:
    st.session_state["vectorstore_ready"] = False

# Hiển thị lịch sử chat
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
if question := st.chat_input("Đặt câu hỏi về tài liệu..."):
    if not st.session_state.get("vectorstore_ready"):
        st.warning("⚠️ Vui lòng upload và xử lý tài liệu trước khi đặt câu hỏi.")
    else:
        st.session_state["messages"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            chain = st.session_state["chain"]
            response = st.write_stream(chain.stream(question))

        st.session_state["messages"].append({"role": "assistant", "content": response})
