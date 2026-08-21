"""多轮 Agent：同一 session 里追问，流式输出，工具失败回灌给模型。"""

from openai import OpenAI

from agent.prompts import AGENT_SYSTEM_PROMPT
from chat.session import ChatSession
from tools.runner import run_tool_calls
from tools.schema import TOOLS
from utils.retry import with_retry

MAX_STEPS = 10


def run_agent_turn(client: OpenAI, session: ChatSession, params: dict) -> str:
    """
    在已有 session 上跑一轮：可能多次调工具，最后流式打出回答。
    返回最终文本（空字符串表示被步数上限打断）。
    """
    call_params = {k: v for k, v in params.items() if k != "stream"}

    for step in range(1, MAX_STEPS + 1):
        print(f"\n[step {step}] 调用模型...")
        content, tool_calls, finish_reason = _stream_step(
            client, session.messages, call_params
        )
        print(f"[step {step}] finish_reason: {finish_reason}")

        if tool_calls:
            session.append(_assistant_message(content, tool_calls))
            for tc in tool_calls:
                print(
                    f"[step {step}] 调用工具: "
                    f"{tc['function']['name']}({tc['function']['arguments']})"
                )
            results = run_tool_calls(tool_calls)
            for row in results:
                print(f"[step {step}] 工具结果: {row['content']}")
            session.extend(results)
            continue

        final = content or ""
        session.add_assistant(final)
        return final

    fallback = "[达到最大步数，agent 强制终止]"
    session.add_assistant(fallback)
    return fallback


def run_agent(client: OpenAI, user_input: str, params: dict) -> str:
    """单次独立运行（无跨问记忆），留给脚本一次性调用。"""
    session = ChatSession(system_prompt=AGENT_SYSTEM_PROMPT)
    session.add_user(user_input)
    return run_agent_turn(client, session, params)


def _stream_step(
    client: OpenAI,
    messages: list[dict],
    params: dict,
) -> tuple[str, list[dict], str]:
    stream = with_retry(
        lambda: client.chat.completions.create(
            messages=messages,
            tools=TOOLS,
            stream=True,
            **params,
        )
    )

    content_parts: list[str] = []
    tool_acc: dict[int, dict] = {}
    finish_reason = "stop"
    printed_prefix = False

    for chunk in stream:
        if not chunk.choices:
            continue
        choice = chunk.choices[0]
        if choice.finish_reason:
            finish_reason = choice.finish_reason
        delta = choice.delta
        if delta is None:
            continue

        if delta.content:
            if not printed_prefix:
                print("Agent: ", end="", flush=True)
                printed_prefix = True
            print(delta.content, end="", flush=True)
            content_parts.append(delta.content)

        for piece in delta.tool_calls or []:
            _merge_tool_delta(tool_acc, piece)

    if printed_prefix:
        print()

    tool_calls = [tool_acc[i] for i in sorted(tool_acc)] if tool_acc else []
    if tool_calls:
        finish_reason = "tool_calls"
    return "".join(content_parts), tool_calls, finish_reason


def _merge_tool_delta(acc: dict[int, dict], piece) -> None:
    idx = 0 if piece.index is None else piece.index
    slot = acc.setdefault(
        idx,
        {
            "id": "",
            "type": "function",
            "function": {"name": "", "arguments": ""},
        },
    )
    if piece.id:
        slot["id"] = piece.id
    if piece.type:
        slot["type"] = piece.type
    fn = piece.function
    if fn is None:
        return
    if fn.name:
        slot["function"]["name"] += fn.name
    if fn.arguments:
        slot["function"]["arguments"] += fn.arguments


def _assistant_message(content: str, tool_calls: list[dict]) -> dict:
    return {
        "role": "assistant",
        "content": content or None,
        "tool_calls": tool_calls,
    }
