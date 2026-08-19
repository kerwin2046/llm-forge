from chat.loop import run_chat_loop
from chat.session import ChatSession
from model import chat_params
from provider import custom_client


def main() -> None:
    client = custom_client()
    session = ChatSession()
    params = chat_params(stream=True)
    run_chat_loop(client, session, params)


if __name__ == "__main__":
    main()
