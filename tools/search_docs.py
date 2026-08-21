"""把 RAG 检索暴露成 Agent 可调用的工具。"""

import json

from rag.retrieve import retrieve_context
from rag.store import DEFAULT_STORE_PATH, VectorStore

# 搜索文档 暴露成 Agent 可调用的工具
def search_docs(query: str, top_k: int = 3) -> str:
    store = VectorStore(DEFAULT_STORE_PATH)
    if store.size == 0:
        return json.dumps({
            "error": "vector store is empty",
            "hint": "Run: python main_rag.py index docs/example.md",
        })

    # retrieve_context 检索相关文档并组装成 prompt。
    # 参数：query: 用户问题，store: 向量存储，top_k: 返回的文档数量
    # 返回：拼接后的上下文
    context = retrieve_context(query, store, top_k=top_k)
    if not context.strip():
        return json.dumps({"error": "no relevant chunks found", "query": query})

    return json.dumps({"query": query, "context": context})
