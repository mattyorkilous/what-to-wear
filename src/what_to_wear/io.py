"""Module for loading and saving files."""

import json
from pathlib import Path
from typing import Any

import yaml

from what_to_wear.utils import get_today, str_to_date


def load_state(state_file: Path) -> dict[str, Any]:
    """Load the state file.

    Args:
        state_file (Path): Path to the state file.

    Returns:
        dict[str, int]: A dictionary describing state.

    """
    try:
        with state_file.open() as f:
            state = json.load(f)

            state['date-last-queried'] = str_to_date(
                state['date-last-queried']
            )

            return state
    except FileNotFoundError:
        state = {
            'current-casual-outfits': 0,
            'current-work-outfits': 0,
            'date-last-queried': get_today()
        }

        return state


def load_config(config_file: Path) -> tuple[
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


def save_state(state: dict[str, Any], state_file: Path) -> None:
    """Save the current state.

    Args:
        state (dict[str, int]): The existing state.
        state_file (Path): The path to the state file.

    """
    state_to_save = state.copy()

    state_to_save['date-last-queried'] = (
        state_to_save['date-last-queried'].strftime('%Y-%m-%d')
    )

    with state_file.open('w') as f:
        json.dump(state_to_save, f)
