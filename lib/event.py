import lib.date as date
from typing import Tuple


class Event:
    def __init__(self, start: date.Date, end: date.Date, name: str, desc: str):
        self.start = start
        self.end = end
        self.name = name
        self.desc = desc


def to_dict(event: Event) -> dict:
    return {
        "summary": event.name,
        "description": event.desc,
        "start": {"dateTime": date.to_timezone_string(event.start)},
        "end": {"dateTime": date.to_timezone_string(event.end)},
    }


def from_dict(message: dict) -> Tuple[str, Event]:
    start = date.from_timezone_string(message["start"]["dateTime"])
    end = date.from_timezone_string(message["end"]["dateTime"])
    name = message.get("summary", "")
    desc = message.get("description", "")
    return str(message["id"]), Event(start, end, name, desc)
