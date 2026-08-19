from openai import OpenAI

from api.stream import create_chat_completion_stream, iter_content
from chat.session import ChatSession

EXIT_COMMANDS = frozenset({"exit", "quit", "/exit", "/quit"})


def _read_user_input() -> str | None:
    try:
        return input("\nYou: ").strip()
    except (EOFError, KeyboardInterrupt):
        return None


def _stream_reply(client: OpenAI, session: ChatSession, params: dict) -> str:
    stream = create_chat_completion_stream(client, session.messages, **params)
    print("🥰:", end="", flush=True)

    parts: list[str] = [] # to store the parts of the reply
    for text in iter_content(stream): # iterate over the stream
        print(text, end="", flush=True) # print the text
        parts.append(text) # add the text to the parts
    print() # print a new line

    return "".join(parts) # join the parts and return the reply


def run_chat_loop(client: OpenAI, session: ChatSession, params: dict) -> None:
    print("Chat started. Type 'exit' or 'quit' to leave, '/clear' to reset history.")

    while True:
        user_input = _read_user_input()
        if user_input is None:
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
        reply = _stream_reply(client, session, params)
        session.add_assistant(reply)
