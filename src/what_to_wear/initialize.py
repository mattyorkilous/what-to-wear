"""Module for initializing the app."""
from datetime import date, datetime
from pathlib import Path

import pytz
import yaml
from platformdirs import user_config_path, user_data_path

from what_to_wear.state import load_state


def initialize(app_name: str) -> tuple[
    Path,
    dict[str, list[dict[str, str]]],
    list[str],
    dict[str, int | str],
    date
]:
    """Initialize the app.

    Load the config and state files and get today's date.

    Args:
        app_name (str): The name of the app.

    """
    config_file, state_file = _get_config_and_state_files(app_name)

    closet, office_days = _load_config(config_file)

    state = load_state(state_file)

    today = _get_today()

    return state_file, closet, office_days, state, today


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


def _get_today() -> date:
    """Get today as a date.

    Returns:
        date: Today's date.

    """
    today = datetime.now(pytz.timezone('America/New_York')).date()

    return today


def _load_config(config_file: Path) -> tuple[
    dict[str, list[dict[str, str]]],
    list[str]
]:
    """Load the configuration file.

    Args:
        config_file (Path): A path to the configuration file.

    Raises:
        FileNotFoundError: The configuration file is not found.

    Returns:
        tuple[ dict[str, list[dict[str, str]]], list[str] ]: The closet
            dictionary and the office days list.

    """
    try:
        with config_file.open() as f:
            config = yaml.safe_load(f)
    except FileNotFoundError as e:
        msg = f'Config file not found at {config_file}. Please create it.'

        raise FileNotFoundError(msg) from e

    return config['closet'], config['office_days']
