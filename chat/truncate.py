DEFAULT_MAX_TURNS = 20


def truncate_messages(
    messages: list[dict[str, str]],
    max_turns: int = DEFAULT_MAX_TURNS,
) -> list[dict[str, str]]:
    """
    保留 system prompt + 最近 max_turns 轮对话。
    一轮 = 一条 user + 一条 assistant，所以最多保留 max_turns * 2 条非 system 消息。
    """
    system = [m for m in messages if m["role"] == "system"]
    history = [m for m in messages if m["role"] != "system"]

    max_messages = max_turns * 2
    if len(history) > max_messages:
        history = history[-max_messages:]

    return system + history
