import os

from openai import OpenAI

DEEPSEEK_BASE_URL = "https://api.deepseek.com"


def get_client(
    api_key: str | None = None,
    base_url: str = DEEPSEEK_BASE_URL,
) -> OpenAI:
    return OpenAI(
        api_key=api_key or os.environ.get("DEEPSEEK_API_KEY"),
        base_url=base_url,
    )
