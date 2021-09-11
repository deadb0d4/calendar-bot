import lib.event as ev
import lib.date as dt


def test_to_dict():
    start = dt.from_timezone_string("2021-09-11T20:13:00+03:00")
    end = dt.from_timezone_string("2021-09-11T21:16:00+03:00")
    event = ev.Event(start, end, "Event", "Testing")
    assert ev.to_dict(event) == {
        "description": "Testing",
        "end": {"dateTime": "2021-09-11T21:16:00+03:00"},
        "start": {"dateTime": "2021-09-11T20:13:00+03:00"},
        "summary": "Event",
    }


def test_from_dict():
    message = {
        "description": "Testing",
        "end": {"dateTime": "2021-09-11T21:16:00+03:00"},
        "start": {"dateTime": "2021-09-11T20:13:00+03:00"},
        "summary": "Event",
        "id": "TestId",
    }
    test_id, event = ev.from_dict(message)
    assert test_id == message.pop("id")
    assert ev.to_dict(event) == message
