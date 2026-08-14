from collections.abc import Iterator

from openai import OpenAI


def create_chat_completion_stream(
    client: OpenAI,
    messages: list[dict[str, str]],
    **params,
):
    return client.chat.completions.create(messages=messages, stream=True, **params)


def iter_content(stream) -> Iterator[str]:
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta


def print_stream(stream) -> None:
    for text in iter_content(stream):
        print(text, end="", flush=True)
    print()
