"""检索相关文档并组装成 prompt。"""

from rag.embed import embed_one
from rag.store import VectorStore

CONTEXT_TEMPLATE = """Use the following context to answer the user's question.
If the context doesn't contain enough information, say so.

--- Context ---
{context}
--- End Context ---
"""


def retrieve_context(query: str, store: VectorStore, top_k: int = 3) -> str:
    """根据用户问题检索最相关的文档片段，返回拼接后的上下文。"""
    query_vector = embed_one(query)
    results = store.search(query_vector, top_k=top_k)

    chunks_text = []
    for chunk, score in results:
        chunks_text.append(f"[{chunk.source} chunk#{chunk.index}] (score: {score:.3f})\n{chunk.text}")

    return "\n\n".join(chunks_text)


def build_rag_messages(query: str, store: VectorStore, top_k: int = 3) -> list[dict[str, str]]:
    """构建带 RAG 上下文的 messages 列表。"""
    context = retrieve_context(query, store, top_k)
    system_content = CONTEXT_TEMPLATE.format(context=context)

    return [
        {"role": "system", "content": system_content},
        {"role": "user", "content": query},
    ]
