"""文档切片：把长文本切成固定大小的小块，带重叠。"""

from dataclasses import dataclass

DEFAULT_CHUNK_SIZE = 500
DEFAULT_OVERLAP = 100  # 相邻块之间重叠的字符数（防止在句子中间断裂丢信息）


@dataclass
class Chunk:
    text: str
    source: str
    index: int


def chunk_text(
    text: str,
    source: str = "unknown",
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    overlap: int = DEFAULT_OVERLAP,
) -> list[Chunk]:
    """
    按字符数切片。

    chunk_size: 每块最大字符数
    overlap: 相邻块之间重叠的字符数（防止在句子中间断裂丢信息）
    """
    chunks = []
    start = 0
    idx = 0

    while start < len(text):
        end = start + chunk_size
        chunk_text_slice = text[start:end]

        if chunk_text_slice.strip():
            chunks.append(Chunk(text=chunk_text_slice, source=source, index=idx))
            idx += 1

        start += chunk_size - overlap

    return chunks


def chunk_file(path: str, **kwargs) -> list[Chunk]:
    """读取文件并切片。"""
    with open(path, encoding="utf-8") as f:
        content = f.read()
    return chunk_text(content, source=path, **kwargs)
