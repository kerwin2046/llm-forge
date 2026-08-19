import json

from tools.weather import get_weather

_REGISTRY = {
    "get_weather": get_weather,
}


def run_tool_calls(tool_calls) -> list[dict]:
    """
    接收模型返回的 tool_calls，执行对应函数，返回 tool 消息列表。
    """
    results = []
    for tc in tool_calls:
        name = tc.function.name
        args = json.loads(tc.function.arguments)

        fn = _REGISTRY.get(name)
        if fn is None:
            output = json.dumps({"error": f"unknown tool: {name}"})
        else:
            output = fn(**args)

        results.append({
            "role": "tool",
            "tool_call_id": tc.id,
            "content": output,
        })

    return results
