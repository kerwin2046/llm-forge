"""检索相关文档并组装成 prompt。"""

from rag.embed import embed_one
from rag.store import VectorStore

CONTEXT_TEMPLATE = """Use the following context to answer the user's question.
If the context doesn't contain enough information, say so.

--- Context ---
{context}
--- End Context ---
"""

# 根据用户问题检索最相关的文档片段，返回拼接后的上下文。
# 参数：query: 用户问题，store: 向量存储，top_k: 返回的文档数量
# 返回：拼接后的上下文
def retrieve_context(query: str, store: VectorStore, top_k: int = 3) -> str:
    """根据用户问题检索最相关的文档片段，返回拼接后的上下文。"""
    query_vector = embed_one(query)
    # 向量搜索
    # 参数：query_vector: 用户问题的向量，top_k: 返回的文档数量
    # 返回：相关文档片段列表
    results = store.search(query_vector, top_k=top_k)
    # 拼接文档片段
    # 参数：results: 相关文档片段列表
    # 返回：拼接后的上下文
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
