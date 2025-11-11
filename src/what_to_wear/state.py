"""Module for loading and saving the state file."""

import json
from pathlib import Path


def load_state(state_file: Path) -> dict[str, int | str]:
    """Load the state file.

    Args:
        state_file (Path): Path to the state file.

    Returns:
        dict[str, int]: A dictionary describing state.

    """
    try:
        with state_file.open() as f:
            state = json.load(f)

            return state
    except FileNotFoundError:
        state = {
            'last-worn-casual-outfits': -1,
            'last-worn-work-outfits': -1,
            'date-last-updated': ''
        }

        return state


def save_state(state: dict[str, int | str], state_file: Path) -> None:
    """Save the current state.

    Args:
        state (dict[str, int]): The existing state.
        state_file (Path): The path to the state file.

    """
    with state_file.open('w') as f:
        json.dump(state, f)
