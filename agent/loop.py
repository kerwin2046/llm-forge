"""Agent 主循环：模型 → 工具 → 模型 → ... → 最终回答。"""

from openai import OpenAI
from openai.types.chat import ChatCompletionMessage

from agent.prompts import AGENT_SYSTEM_PROMPT
from tools.runner import run_tool_calls
from tools.schema import TOOLS

MAX_STEPS = 10


def run_agent(client: OpenAI, user_input: str, params: dict) -> str:
    """
    执行 agent 循环，返回最终回答文本。

    循环逻辑：
      1. 调用模型
      2. 如果 finish_reason == "tool_calls" → 执行工具，把结果追加进 messages，继续
      3. 如果 finish_reason == "stop" → 返回最终回答
      4. 超过 MAX_STEPS → 强制终止
    """
    messages: list[dict] = [
        {"role": "system", "content": AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": user_input},
    ]

    # agent 循环不用流式，方便拿 tool_calls 结构
    call_params = {k: v for k, v in params.items() if k != "stream"}

    for step in range(1, MAX_STEPS + 1):
        print(f"\n[step {step}] 调用模型...")

        response = client.chat.completions.create(
            messages=messages,
            tools=TOOLS,
            **call_params,
        )

        choice = response.choices[0]
        message: ChatCompletionMessage = choice.message

        print(f"[step {step}] finish_reason: {choice.finish_reason}")

        if choice.finish_reason == "tool_calls":
            # 把模型的"要调工具"这条存入历史
            messages.append(message)

            # 执行所有工具调用
            for tc in message.tool_calls:
                print(f"[step {step}] 调用工具: {tc.function.name}({tc.function.arguments})")

            tool_results = run_tool_calls(message.tool_calls)
            for r in tool_results:
                print(f"[step {step}] 工具结果: {r['content']}")

            messages.extend(tool_results)
            continue

        # finish_reason == "stop"：模型给出最终回答
        final = message.content or ""
        return final

    return "[达到最大步数，agent 强制终止]"
