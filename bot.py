import telebot

import googleapiclient
from google.oauth2 import service_account
from googleapiclient.discovery import build

import lib.event as ev
import lib.date as dt
from lib.config import Config

from typing import List, Tuple


def _parse_watch(w):
    return tuple(map(int, w.split(":")))


class Calendar:
    def __init__(self, config: Config):
        credentials = service_account.Credentials.from_service_account_file(
            config.calendar["credentials_filepath"], scopes=config.calendar["scopes"]
        )
        self.service = googleapiclient.discovery.build(
            "calendar", "v3", credentials=credentials
        )
        self.config = config

    def create_event(self, event: ev.Event) -> str:
        e = (
            self.service.events()
            .insert(calendarId=self.config.basic["email"], body=ev.to_dict(event))
            .execute()
        )
        return e["htmlLink"]

    def busy_time(self, start: dt.Date, end: dt.Date) -> List[Tuple[dt.Date, dt.Date]]:
        #  body = {
        #      "timeMin": dt.to_utc_string(start),
        #      "timeMax": dt.to_utc_string(end),
        #      "items": [{"id": self.config.basic["email"]}],
        #  }
        #  res = self.service.freebusy().query(body=body).execute()
        pass  # TODO: use it


config = Config("./secret")
cal = Calendar(config)
bot = telebot.TeleBot(config.bot["token"])


def _parse_date(s: str) -> Tuple[int, int, int]:
    s = s.replace(" ", "").lower()

    # watch for special values
    now = dt.now(config.basic["gmt"])
    if s == "today" or s == "t":
        return now.day, now.month, now.year
    elif s == "tomorrow" or s == "tt":
        d = dt.after(now, 24 * 60)
        return d.day, d.month, d.year

    # substitute by defaults
    items = list(map(int, s.split(".")))
    if len(items) == 1:
        items += [now.month, now.year]
    elif len(items) == 2:
        items += [now.year]
    start_day, start_month, start_year = items

    # basic check
    if not (0 < start_day < 32):
        raise RuntimeError(f"Invalid start day: {start_day}")
    if not (0 < start_month < 13):
        raise RuntimeError(f"Invalid start month: {start_month}")
    return start_day, start_month, start_year


def _parse_time(s: str) -> Tuple[int, int]:
    s = s.replace(" ", "")
    h = int(s[:2])
    if not (0 <= h < 24):
        raise RuntimeError(f"Invalid hour: {h}")
    m = int(s[2:4])
    if not (0 <= m < 60):
        raise RuntimeError(f"Invalid minutes: {m}")
    return h, m


@bot.message_handler(commands=["start", "help"])
def get_text_messages(message):
    if message.from_user.username != config.bot["owner"]:
        text = "I am a teapot"
    else:
        options = config.bot["options"]
        text = (
            config.bot["greet"]
            + "\n\n"
            + "\n\n".join([e["name"].title() + ": " + e["desc"] for e in options])
        )
    bot.reply_to(message, text)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    try:
        items = message.text.split(",")
        # try to parse first item as a start date
        start_day, start_month, start_year = _parse_date(items[0])
        start_hour, start_minutes = _parse_time(items[1])
        if len(items) == 5:
            # end day is not the start one...
            end_day, end_month, end_year = _parse_date(items[2])
        else:
            end_day, end_month, end_year = start_day, start_month, start_year
        end_hour, end_minutes = _parse_time(items[-2])
        if ":" in items[-1]:
            name, desc = items[-1].split(":")
            name = name.strip()
            desc = desc.strip()
        else:
            name = items[-1].strip()
            desc = ""
        start = dt.Date(
            start_year,
            start_month,
            start_day,
            start_hour,
            start_minutes,
            config.basic["gmt"],
        )
        end = dt.Date(
            end_year,
            end_month,
            end_day,
            end_hour,
            end_minutes,
            config.basic["gmt"],
        )
        link = cal.create_event(ev.Event(start, end, name.title(), desc))
        bot.reply_to(message, link)
    except Exception as e:
        bot.reply_to(message, f"Failed to create: {e}")


# TODO: add correct app loop
while True:
    try:
        bot.polling(none_stop=True)
    except:
        # TODO: add persistent logging
        continue
