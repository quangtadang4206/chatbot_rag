from typing import List, Optional
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate


_MULTIQUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""Bạn là trợ lý AI hỗ trợ tìm kiếm tài liệu. Hãy tạo 3 cách diễn đạt khác nhau cho câu hỏi sau bằng tiếng Việt, giúp tìm kiếm được nhiều thông tin liên quan hơn từ nhiều góc độ khác nhau.

Câu hỏi gốc: {question}

3 biến thể câu hỏi (mỗi câu một dòng, không đánh số):""",
)


def get_multiquery_retriever(vectorstore: Chroma, k: int = 5, docs=None, **kwargs):
    """
    LLM sinh 3 biến thể câu hỏi tiếng Việt → retrieval từng biến thể → union kết quả.
    Hiệu quả cao với tiếng Việt vì ngôn ngữ có nhiều cách paraphrase khác nhau.
    """
    from langchain.retrievers.multi_query import MultiQueryRetriever

    base_retriever = vectorstore.as_retriever(search_kwargs={"k": k})
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    return MultiQueryRetriever.from_llm(
        retriever=base_retriever,
        llm=llm,
        prompt=_MULTIQUERY_PROMPT,
    )


def get_hybrid_retriever(
    vectorstore: Chroma,
    docs: Optional[List[Document]] = None,
    k: int = 5,
    **kwargs,
):
    """
    BM25 (keyword) + Vector (ngữ nghĩa) → EnsembleRetriever.
    BM25 bắt tốt tên riêng, mã số, thuật ngữ chuyên ngành tiếng Việt.
    Vector bắt tốt câu hỏi ngữ nghĩa mơ hồ.
    Yêu cầu: truyền docs=chunks khi khởi tạo.
    """
    from langchain_community.retrievers import BM25Retriever
    from langchain.retrievers import EnsembleRetriever

    if not docs:
        raise ValueError("Hybrid search yêu cầu tham số docs=chunks. Vui lòng truyền danh sách chunks.")

    bm25_retriever = BM25Retriever.from_documents(docs)
    bm25_retriever.k = k

    vector_retriever = vectorstore.as_retriever(search_kwargs={"k": k})

    return EnsembleRetriever(
        retrievers=[bm25_retriever, vector_retriever],
        weights=[0.4, 0.6],
    )


def get_rerank_retriever(
    vectorstore: Chroma,
    k: int = 5,
    fetch_k: int = 15,
    docs=None,
    **kwargs,
):
    """
    Retrieve fetch_k chunks → FlashrankRerank cross-encoder → lấy top k chính xác nhất.
    Tăng precision +10–20%. Model cross-encoder tải lần đầu ~90MB, sau đó cache local.
    """
    from langchain.retrievers import ContextualCompressionRetriever
    from langchain_community.document_compressors import FlashrankRerank

    base_retriever = vectorstore.as_retriever(search_kwargs={"k": fetch_k})
    compressor = FlashrankRerank(top_n=k)
    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever,
    )


STRATEGY_MAP = {
    "multiquery": get_multiquery_retriever,
    "hybrid": get_hybrid_retriever,
    "rerank": get_rerank_retriever,
}

STRATEGY_LABELS = {
    "multiquery": "Multi-Query — LLM sinh 3–5 biến thể câu hỏi",
    "hybrid": "Hybrid BM25 + Vector — keyword + ngữ nghĩa",
    "rerank": "Rerank — cross-encoder lọc top kết quả chính xác nhất",
}


def get_retriever(
    vectorstore: Chroma,
    strategy: str = "multiquery",
    docs: Optional[List[Document]] = None,
    **kwargs,
):
    if strategy not in STRATEGY_MAP:
        raise ValueError(f"Chiến lược không hợp lệ: '{strategy}'. Chọn một trong: {list(STRATEGY_MAP.keys())}")
    return STRATEGY_MAP[strategy](vectorstore, docs=docs, **kwargs)
