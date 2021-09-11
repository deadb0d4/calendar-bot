import lib.date as my_date


def test_from_utc_string():
    gmt = 3
    date = my_date.from_utc_string(gmt, "2021-08-31T23:12:33.000Z")
    assert date.year == 2021
    assert date.month == 9
    assert date.day == 1
    assert date.minutes == 12
    assert date.hour == 2
    assert date.gmt == 3


def test_to_utc_string():
    date = my_date.from_utc_string(3, "2021-08-31T11:12:33.000Z")
    assert my_date.to_utc_string(date) == '2021-08-31T11:12:00.000Z'


def test_to_timezone_string():
    date = my_date.from_utc_string(3, "2021-08-31T11:12:33.000Z")
    assert my_date.to_timezone_string(date) == '2021-08-31T14:12:00+03:00'


def test_from_timezone_string():
    date = my_date.from_timezone_string('2021-09-01T02:13:31+03:00')
    assert my_date.to_utc_string(date) == '2021-08-31T23:13:00.000Z'
