DEFAULT_MAX_TURNS = 20


def truncate_messages(
    messages: list[dict],
    max_turns: int = DEFAULT_MAX_TURNS,
) -> list[dict]:
    """
    保留 system + 最近 max_turns 个以 user 开头的回合。

    一个回合 = 一条 user，以及其后所有 assistant / tool 消息。
    这样不会把 tool_calls 和对应的 tool 结果拆开。
    """
    system = [m for m in messages if m.get("role") == "system"]
    history = [m for m in messages if m.get("role") != "system"]

    turns: list[list[dict]] = []
    current: list[dict] = []
    for msg in history:
        if msg.get("role") == "user":
            if current:
                turns.append(current)
            current = [msg]
        else:
            if not current:
                current = [msg]
            else:
                current.append(msg)
    if current:
        turns.append(current)

    kept = turns[-max_turns:] if len(turns) > max_turns else turns
    flattened = [msg for turn in kept for msg in turn]
    return system + flattened
