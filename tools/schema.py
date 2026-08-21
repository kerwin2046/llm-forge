TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather for a given city.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {
                        "type": "string",
                        "description": "The city name, e.g. Beijing, London",
                    }
                },
                "required": ["city"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_docs",
            "description": (
                "Search the local knowledge base (indexed project docs) "
                "for facts about llm-forge, its phases, models, or how to run it."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query in the user's language",
                    },
                    "top_k": {
                        "type": "integer",
                        "description": "Number of chunks to return (default 3)",
                    },
                },
                "required": ["query"],
            },
        },
    },
]
