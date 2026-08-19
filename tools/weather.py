import json

_FAKE_DATA = {
    "beijing":  {"city": "Beijing",  "temp_c": 28, "condition": "sunny"},
    "shanghai": {"city": "Shanghai", "temp_c": 32, "condition": "cloudy"},
    "london":   {"city": "London",   "temp_c": 15, "condition": "rainy"},
}


def get_weather(city: str) -> str:
    data = _FAKE_DATA.get(city.lower(), {"city": city, "temp_c": 20, "condition": "unknown"})
    return json.dumps(data)
