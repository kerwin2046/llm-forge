from openai import OpenAI
from openai.types.chat import ChatCompletion


def create_chat_completion(
    client: OpenAI,
    messages: list[dict[str, str]],
    **params,
) -> ChatCompletion:
    return client.chat.completions.create(messages=messages, **params)
