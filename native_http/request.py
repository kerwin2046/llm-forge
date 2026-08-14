import json
import os
import urllib.error
import urllib.request

DEEPSEEK_BASE_URL = "https://api.deepseek.com"
CHAT_COMPLETIONS_PATH = "/chat/completions"


def _build_payload(messages: list[dict[str, str]], **params) -> dict:
    payload: dict = {"messages": messages}
    extra_body = params.pop("extra_body", None)
    payload.update(params)
    if extra_body:
        payload.update(extra_body)
    return payload


def create_chat_completion(
    messages: list[dict[str, str]],
    *,
    api_key: str | None = None,
    base_url: str = DEEPSEEK_BASE_URL,
    **params,
) -> dict:
    api_key = api_key or os.environ.get("DEEPSEEK_API_KEY")
    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY is required")

    payload = _build_payload(messages, **params)
    url = f"{base_url.rstrip('/')}{CHAT_COMPLETIONS_PATH}"
    data = json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )

    try:
        with urllib.request.urlopen(request) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"HTTP {exc.code}: {body}") from exc
