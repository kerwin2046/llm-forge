"""RAG 演示：索引文档 → 检索 → 回答。

用法：
    # 第一次：索引文档
    python main_rag.py index docs/example.md

    # 之后：提问
    python main_rag.py ask "这篇文档讲了什么？"
"""

import sys

from api.stream import create_chat_completion_stream, iter_content
from model import chat_params
from provider import custom_client
from rag.chunk import chunk_file
from rag.embed import embed_texts
from rag.retrieve import build_rag_messages
from rag.store import VectorStore

STORE_PATH = "rag_store.json"


def cmd_index(file_path: str) -> None:
    """切片 + 向量化 + 存储。"""
    print(f"正在索引: {file_path}")
    chunks = chunk_file(file_path)
    print(f"  切片数: {len(chunks)}")

    texts = [c.text for c in chunks]
    print("  正在向量化...")
    vectors = embed_texts(texts)

    store = VectorStore(STORE_PATH)
    for chunk, vector in zip(chunks, vectors):
        store.add(text=chunk.text, source=chunk.source, index=chunk.index, vector=vector)
    store.save()

    print(f"  完成！向量库大小: {store.size} 条")


def cmd_ask(query: str) -> None:
    """检索 + 生成回答。"""
    store = VectorStore(STORE_PATH)
    if store.size == 0:
        print("向量库为空，请先运行: python main_rag.py index <file>")
        return

    print(f"检索中... (库中 {store.size} 条)")
    messages = build_rag_messages(query, store)

    print(f"\n回答: ", end="", flush=True)
    client = custom_client()
    params = chat_params(stream=True)
    stream = create_chat_completion_stream(client, messages, **params)
    for text in iter_content(stream):
        print(text, end="", flush=True)
    print()


def main() -> None:
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)

    cmd = sys.argv[1]
    if cmd == "index":
        cmd_index(sys.argv[2])
    elif cmd == "ask":
        cmd_ask(sys.argv[2])
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)
        sys.exit(1)


if __name__ == "__main__":
    main()
