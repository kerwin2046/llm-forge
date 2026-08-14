def default_messages(user_content: str = "hello,Good Day!") -> list[dict[str, str]]:
    return [
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": user_content},
    ]
