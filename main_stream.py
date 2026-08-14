from api.stream import create_chat_completion_stream, print_stream
from messages import default_messages
from model import chat_params
from provider import get_client


def main() -> None:
    client = get_client()
    messages = default_messages()
    params = chat_params(stream=True)
    stream = create_chat_completion_stream(client, messages, **params)
    print_stream(stream)


if __name__ == "__main__":
    main()
