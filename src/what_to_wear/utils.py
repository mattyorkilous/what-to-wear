"""Module for utilities."""

import calendar
from datetime import date


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
