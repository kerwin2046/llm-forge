import sys

from agent.loop import run_agent_turn
from agent.prompts import AGENT_SYSTEM_PROMPT
from chat.session import ChatSession
from model import chat_params
from provider import custom_client

EXIT_COMMANDS = frozenset({"exit", "quit", "/exit", "/quit"})


def main() -> None:
    client = custom_client()
    params = chat_params()
    session = ChatSession(system_prompt=AGENT_SYSTEM_PROMPT)

    if "--demo" in sys.argv:
        _run_demo(client, session, params)
        return

    print("Agent chat. Type 'exit' to leave, '/clear' to reset. History is kept across turns.")
    print("Try: weather in Beijing and London → then: which city is warmer?")
    print("Or: what model does this project use? (needs: python main_rag.py index docs/example.md)")

    while True:
        try:
            user_input = input("\nYou: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        lowered = user_input.lower()
        if lowered in EXIT_COMMANDS:
            print("Bye.")
            break
        if lowered == "/clear":
            session.clear()
            print("History cleared.")
            continue

        session.add_user(user_input)
        run_agent_turn(client, session, params)


def _run_demo(client, session: ChatSession, params: dict) -> None:
    questions = [
        "What's the weather like in Beijing and London?",
        "Which city is warmer?",
        "What model does llm-forge use?",
    ]
    for q in questions:
        print(f"\n{'=' * 50}")
        print(f"用户: {q}")
        session.add_user(q)
        run_agent_turn(client, session, params)


if __name__ == "__main__":
    main()
