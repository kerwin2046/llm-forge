DEFAULT_MODEL = "deepseek-v4-flash"


def chat_params(
    model: str = DEFAULT_MODEL,
    stream: bool = False,
    reasoning_effort: str = "high",
) -> dict:
    return {
        "model": model,
        "stream": stream,
        "reasoning_effort": reasoning_effort,
        "extra_body": {"thinking": {"type": "enabled"}},
    }
