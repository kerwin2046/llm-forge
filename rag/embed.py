"""文本向量化：调用 Jina AI embedding API。

需要环境变量：JINA_API_KEY
"""

import os

import urllib.request
import json

JINA_BASE_URL = "https://api.jina.ai/v1/embeddings"
DEFAULT_EMBED_MODEL = "jina-embeddings-v5-omni-small"


def embed_texts(
    texts: list[str],
    model: str = DEFAULT_EMBED_MODEL,
    task: str = "retrieval.passage",
) -> list[list[float]]:
    """批量向量化，返回与 texts 等长的向量列表。"""
    api_key = os.environ.get("JINA_API_KEY")
    if not api_key:
        raise ValueError("需要设置 JINA_API_KEY 环境变量")

    payload = json.dumps({
        "model": model,
        "task": task,
        "normalized": True,
        "input": [{"text": t} for t in texts],
    }).encode("utf-8")

    req = urllib.request.Request(
        JINA_BASE_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        },
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        result = json.loads(resp.read().decode("utf-8"))

    result["data"].sort(key=lambda x: x["index"])
    return [item["embedding"] for item in result["data"]]


def embed_one(text: str, model: str = DEFAULT_EMBED_MODEL, task: str = "retrieval.query") -> list[float]:
    """单条文本向量化，query 用 retrieval.query task。"""
    return embed_texts([text], model=model, task=task)[0]
