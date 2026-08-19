from provider import custom_client
from messages import default_messages
from model import chat_params
from tools.schema import TOOLS
from tools.runner import run_tool_calls
from api.response import get_content


def main() -> None:
    client = custom_client()
    messages = default_messages("What's the weather in Beijing?")
    params = chat_params()

    # 第一次调用：模型决定要不要用工具
    response = client.chat.completions.create(
        messages=messages,
        tools=TOOLS,
        **{k: v for k, v in params.items() if k != "stream"},
    )

    choice = response.choices[0]
    print(f"finish_reason: {choice.finish_reason}")

    if choice.finish_reason == "tool_calls":
        # 把模型的"我要调工具"这条消息存入历史
        messages.append(choice.message)

        # 执行工具，把结果存入历史
        tool_results = run_tool_calls(choice.message.tool_calls)
        messages.extend(tool_results)

        print(f"工具返回: {tool_results[0]['content']}")

        # 第二次调用：模型看到工具结果，生成最终回答
        final = client.chat.completions.create(
            messages=messages,
            **{k: v for k, v in params.items() if k != "stream"},
        )
        print(f"\n最终回答: {get_content(final)}")
    else:
        # 模型直接回答，不需要工具
        print(f"\n直接回答: {get_content(response)}")


if __name__ == "__main__":
    main()
