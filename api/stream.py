from collections.abc import Iterator

from openai import OpenAI

from utils.retry import with_retry


def create_chat_completion_stream(
    client: OpenAI,
    messages: list[dict[str, str]],
    **params,
):
    params = {**params, "stream": True}
    return with_retry(lambda: client.chat.completions.create(messages=messages, **params))


def iter_content(stream) -> Iterator[str]:
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def print_stream(stream) -> None:
    for text in iter_content(stream):
        print(text, end="", flush=True)
    print()
