import json

from tools.search_docs import search_docs
from tools.weather import get_weather

_REGISTRY = {
    "get_weather": get_weather,
    "search_docs": search_docs,
}


def run_tool_calls(tool_calls) -> list[dict]:
    """执行模型给出的 tool_calls；任何失败都写成 tool 消息回给模型。"""
    results = []
    for tc in tool_calls:
        call_id, name, raw_args = _unpack(tc)
        results.append({
            "role": "tool",
            "tool_call_id": call_id,
            "content": _run_one(name, raw_args),
        })
    return results


def _unpack(tc) -> tuple[str, str, str]:
    if isinstance(tc, dict):
        fn = tc.get("function") or {}
        return str(tc.get("id", "")), str(fn.get("name", "")), str(fn.get("arguments") or "{}")
    return tc.id, tc.function.name, tc.function.arguments or "{}"


def _run_one(name: str, raw_args: str) -> str:
    fn = _REGISTRY.get(name)
    if fn is None:
        return json.dumps({"error": f"unknown tool: {name}"})

    try:
        args = json.loads(raw_args or "{}")
        if not isinstance(args, dict):
            return json.dumps({"error": "tool arguments must be a JSON object"})
        return fn(**args)
    except json.JSONDecodeError as exc:
        return json.dumps({"error": f"invalid JSON arguments: {exc}"})
    except TypeError as exc:
        return json.dumps({"error": f"bad arguments for {name}: {exc}"})
    except Exception as exc:
        return json.dumps({"error": f"{name} failed: {exc}"})
