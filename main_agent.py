from agent.loop import run_agent
from model import chat_params
from provider import custom_client


def main() -> None:
    client = custom_client()
    params = chat_params()

    questions = [
        "What's the weather like in Beijing and London?",
        "Which city is warmer?",
    ]

    for q in questions:
        print(f"\n{'='*50}")
        print(f"用户: {q}")
        answer = run_agent(client, q, params)
        print(f"\n最终回答: {answer}")


if __name__ == "__main__":
    main()
