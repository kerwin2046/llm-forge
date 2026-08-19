from api.request import create_chat_completion
from api.response import print_response
from messages import default_messages
from model import chat_params
from provider import custom_client


def main() -> None:
    client = custom_client()
    messages = default_messages()
    params = chat_params()
    response = create_chat_completion(client, messages, **params)
    print_response(response)


if __name__ == "__main__":
    main()
