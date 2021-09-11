import datetime
from typing import Optional


class Date:
    def __init__(
        self, year: int, month: int, day: int, hour: int, minutes: int, gmt: int
    ):
        self.year: int = year
        self.month: int = month
        self.day: int = day
        self.hour: int = hour
        self.minutes: int = minutes
        self.gmt: int = gmt


def from_utc_datetime(gmt: int, date: datetime.datetime) -> Date:
    date += datetime.timedelta(hours=gmt)
    return Date(date.year, date.month, date.day, date.hour, date.minute, gmt)


def to_utc_datetime(date: Date) -> datetime.datetime:
    res = datetime.datetime(date.year, date.month, date.day, date.hour, date.minutes)
    res -= datetime.timedelta(hours=date.gmt)
    return res


def now(gmt: int) -> Date:
    return from_utc_datetime(gmt, datetime.datetime.now(datetime.timezone.utc))


def to_timezone_string(date: Date) -> str:
    day = f"{date.year}-{str(date.month).zfill(2)}-{str(date.day).zfill(2)}"
    time = f"{str(date.hour).zfill(2)}:{str(date.minutes).zfill(2)}:00"
    gmt = f"{str(date.gmt).zfill(2)}:00"
    return f"{day}T{time}+{gmt}"


def from_timezone_string(s: str) -> Date:
    date, time = s.split("T")
    time, gmt = time.split("+")
    gmt = int(gmt.split(":")[0])
    hour, minutes, _ = map(int, time.split(":"))
    year, month, day = map(int, date.split("-"))
    return Date(year, month, day, hour, minutes, gmt)


def from_utc_string(gmt: int, s: str) -> Date:
    assert s[-1] == "Z"
    return from_utc_datetime(
        gmt, datetime.datetime.strptime(s[:-1], "%Y-%m-%dT%H:%M:%S.%f")
    )


def to_utc_string(date: Date) -> str:
    return to_utc_datetime(date).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"
