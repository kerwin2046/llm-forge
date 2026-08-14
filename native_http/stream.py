import json
import os
import urllib.error
import urllib.request
from collections.abc import Iterator

from native_http.request import CHAT_COMPLETIONS_PATH, DEEPSEEK_BASE_URL, _build_payload


def _iter_sse_lines(response) -> Iterator[str]:
    for raw_line in response:
        line = raw_line.decode("utf-8").strip()
        if line:
            yield line


def _parse_sse_chunk(line: str) -> str | None:
    if not line.startswith("data: "):
        return None

    data = line[6:]
    if data == "[DONE]":
        return None

    chunk = json.loads(data)
    return chunk["choices"][0]["delta"].get("content")


def create_chat_completion_stream(
    messages: list[dict[str, str]],
    *,
    api_key: str | None = None,
    base_url: str = DEEPSEEK_BASE_URL,
    **params,
) -> Iterator[str]:
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is required")

    params = {**params, "stream": True}
    payload = _build_payload(messages, **params)
    url = f"{base_url.rstrip('/')}{CHAT_COMPLETIONS_PATH}"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Accept": "text/event-stream",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as response:
            for line in _iter_sse_lines(response):
                content = _parse_sse_chunk(line)
                if content:
                    yield content
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc


def print_stream(stream: Iterator[str]) -> None:
    for text in stream:
        print(text, end="", flush=True)
    print()
