"""Module for initializing the app."""
from datetime import date
from pathlib import Path
from typing import Any

from platformdirs import user_config_path, user_data_path

from what_to_wear.io import load_config, load_state
from what_to_wear.utils import get_today


def initialize(app_name: str) -> tuple[
    dict[str, list[dict[str, str]]],
    list[str],
    dict[str, Any],
    date,
    Path
]:
    """Initialize the app.

    Load the config and state files and get today's date.

    Args:
        app_name (str): The name of the app.

    """
    config_file, state_file = _get_config_and_state_files(app_name)

    closet, office_days = load_config(config_file)

    state = load_state(state_file)

    today = get_today()

    return closet, office_days, state, today, state_file


def _get_config_and_state_files(app_name: str) -> tuple[Path, Path]:
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
