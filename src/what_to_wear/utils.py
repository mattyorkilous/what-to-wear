"""Module for utilities."""

import calendar
from datetime import date, datetime

import pytz


def check_is_office_day(day: date, office_days: list[str]) -> bool:
    """Check if the given day is an office day.

    Args:
        day (date): The date to check.
        office_days (list[str]): A list of office day names.

    Returns:
        bool: True if it's an office day, False otherwise.

    """
    weekday = list(calendar.day_name)[day.weekday()]

    return weekday in office_days


def get_today() -> date:
    """Get today as a date.

    Returns:
        date: Today's date.

    """
    today = datetime.now(pytz.timezone('America/New_York')).date()

    return today


def str_to_date(date_string: str) -> date:
    """Convert a string to a date.

    Args:
        date_string (str): A date represented as a string.

    Returns:
        date: A date.

    """
    str_as_date = (
        datetime.strptime(date_string, '%Y-%m-%d')
            .astimezone(pytz.timezone('America/New_York'))
            .date()
    )

    return str_as_date
