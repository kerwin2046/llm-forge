from openai import OpenAI
from openai.types.chat import ChatCompletion

from utils.retry import with_retry


def create_chat_completion(
    client: OpenAI,
    messages: list[dict[str, str]],
    **params,
) -> ChatCompletion:
    return with_retry(lambda: client.chat.completions.create(messages=messages, **params))
