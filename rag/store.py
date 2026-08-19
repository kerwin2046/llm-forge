"""最小向量存储：JSON 持久化 + 余弦相似度检索。"""

import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class StoredChunk:
    text: str
    source: str
    index: int
    vector: list[float]


DEFAULT_STORE_PATH = "rag_store.json"


def cosine_similarity(a: list[float], b: list[float]) -> float:
    """计算两个向量的余弦相似度。"""
    dot = sum(x * y for x, y in zip(a, b))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(x * x for x in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)


class VectorStore:
    def __init__(self, path: str = DEFAULT_STORE_PATH) -> None:
        self._path = Path(path)
        self._chunks: list[StoredChunk] = []
        if self._path.exists():
            self._load()

    def add(self, text: str, source: str, index: int, vector: list[float]) -> None:
        self._chunks.append(StoredChunk(text=text, source=source, index=index, vector=vector))

    def save(self) -> None:
        data = [asdict(c) for c in self._chunks]
        self._path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    def search(self, query_vector: list[float], top_k: int = 3) -> list[tuple[StoredChunk, float]]:
        """返回最相似的 top_k 个 chunk 及其相似度分数。"""
        scored = [
            (chunk, cosine_similarity(query_vector, chunk.vector))
            for chunk in self._chunks
        ]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:top_k]

    @property
    def size(self) -> int:
        return len(self._chunks)

    def _load(self) -> None:
        data = json.loads(self._path.read_text(encoding="utf-8"))
        self._chunks = [StoredChunk(**item) for item in data]
