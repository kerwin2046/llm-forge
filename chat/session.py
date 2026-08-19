from chat.truncate import DEFAULT_MAX_TURNS, truncate_messages


class ChatSession:
    def __init__(
        self,
        system_prompt: str = "You are a helpful assistant",
        max_turns: int = DEFAULT_MAX_TURNS,
    ) -> None:
        self._system_prompt = system_prompt
        self._max_turns = max_turns
        self._messages: list[dict[str, str]] = [
            {"role": "system", "content": system_prompt},
        ]

    @property
    def messages(self) -> list[dict[str, str]]:
        return truncate_messages(self._messages, self._max_turns)

    def add_user(self, content: str) -> None:
        self._messages.append({"role": "user", "content": content})

    def add_assistant(self, content: str) -> None:
        self._messages.append({"role": "assistant", "content": content})

    def clear(self) -> None:
        self._messages = [{"role": "system", "content": self._system_prompt}]
