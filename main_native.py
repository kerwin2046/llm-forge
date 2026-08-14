from messages import default_messages
from model import chat_params
from native_http.request import create_chat_completion
from native_http.response import print_response


def main() -> None:
    messages = default_messages()
    params = chat_params()
    response = create_chat_completion(messages, **params)
    print_response(response)


if __name__ == "__main__":
    main()
