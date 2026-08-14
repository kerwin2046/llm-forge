def get_content(response: dict) -> str:
    return response["choices"][0]["message"]["content"] or ""


def print_response(response: dict) -> None:
    print(get_content(response))
    print(response)
