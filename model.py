DEFAULT_MODEL = "deepseek-v4-flash"
AGENTS_MODEL = "agnes-2.0-flash"

def chat_params(
    model: str = AGENTS_MODEL,
    stream: bool = False,
    reasoning_effort: str = "high",
) -> dict:
    return {
        "model": model,
        "stream": stream,
        "reasoning_effort": reasoning_effort,
        "extra_body": {"thinking": {"type": "enabled"}},
    }
