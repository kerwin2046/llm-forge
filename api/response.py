from openai.types.chat import ChatCompletion


def get_content(response: ChatCompletion) -> str:
    return response.choices[0].message.content or ""


def print_response(response: ChatCompletion) -> None:
    print(get_content(response))
    print(response)
