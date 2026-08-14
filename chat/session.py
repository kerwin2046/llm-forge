class ChatSession:
    def __init__(self, system_prompt: str = "You are a helpful assistant") -> None:
        self._system_prompt = system_prompt
        self._messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]

    @property
    def messages(self) -> list[dict[str, str]]:
        return list(self._messages)

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str) -> None:
        self._messages.append({"role": "assistant", "content": content})

    def clear(self) -> None:
        self._messages = [{"role": "system", "content": self._system_prompt}]
