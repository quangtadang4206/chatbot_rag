from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# --- Prompts ---

PROMPT_GENERAL = ChatPromptTemplate.from_messages([
    ("system", """Bạn là trợ lý AI thông minh, trả lời câu hỏi dựa trên nội dung tài liệu được cung cấp.

Hướng dẫn:
- Trả lời dựa trên ngữ cảnh bên dưới.
- Nếu không tìm thấy thông tin trong tài liệu, hãy nói thẳng: "Tôi không tìm thấy thông tin này trong tài liệu."
- Trả lời rõ ràng, súc tích bằng tiếng Việt.

Ngữ cảnh từ tài liệu:
{context}"""),
    ("human", "{question}"),
])

PROMPT_STRICT = ChatPromptTemplate.from_messages([
    ("system", """Bạn là trợ lý AI chuyên nghiệp. Chỉ được phép trả lời dựa trên nội dung tài liệu bên dưới, không được suy luận hay bổ sung thông tin ngoài tài liệu.

Quy tắc nghiêm ngặt:
- Chỉ trích dẫn thông tin có trong ngữ cảnh.
- Nếu câu hỏi không liên quan hoặc không có trong tài liệu, trả lời: "Thông tin này không có trong tài liệu được cung cấp."
- Không đưa ra ý kiến cá nhân hoặc kiến thức bên ngoài.

Ngữ cảnh từ tài liệu:
{context}"""),
    ("human", "{question}"),
])

PROMPT_MAP = {
    "general": PROMPT_GENERAL,
    "strict": PROMPT_STRICT,
}

PROMPT_LABELS = {
    "general": "Tổng quát — trả lời linh hoạt",
    "strict": "Chặt chẽ — chỉ dựa trên tài liệu",
}


def _format_docs(docs) -> str:
    return "\n\n---\n\n".join(doc.page_content for doc in docs)


def create_rag_chain(retriever, prompt_type: str = "general"):
    if prompt_type not in PROMPT_MAP:
        raise ValueError(f"Loại prompt không hợp lệ: '{prompt_type}'. Chọn: {list(PROMPT_MAP.keys())}")

    prompt = PROMPT_MAP[prompt_type]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, streaming=True)

    chain = (
        {"context": retriever | _format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain
