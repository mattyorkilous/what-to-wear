"""Module for utilities."""

import calendar
from datetime import date, datetime
from pathlib import Path

import pytz
from platformdirs import user_config_path, user_data_path


def get_config_and_state_files(app_name: str) -> tuple[Path, Path]:
    """Get the config and state files for the app.

    Args:
        app_name (str): The name of the app.

    Returns:
        tuple[Path, Path]: The config file and state file paths.

    """
    config_dir, data_dir = _make_platform_dirs(app_name)

    config_file = config_dir / 'config.yaml'

    state_file = data_dir / 'rotation_state.json'

    return config_file, state_file


def _make_platform_dirs(app_name: str) -> tuple[Path, Path]:
    """Make platform-specific directories for the app.

    Args:
        app_name (str): The name of the app.

    """
    config_dir = user_config_path(app_name)

    data_dir = user_data_path(app_name)

    for directory in (config_dir, data_dir):
        directory.mkdir(exist_ok=True)

    return config_dir, data_dir


def get_today() -> date:
    """Get today as a date.

    Returns:
        date: Today's date.

    """
    today = datetime.now(pytz.timezone('America/New_York')).date()

    return today


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
