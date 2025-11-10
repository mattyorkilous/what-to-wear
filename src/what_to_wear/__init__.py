"""Execute the What to Wear app."""
from __future__ import annotations

import calendar
import json
from datetime import date, datetime
from typing import TYPE_CHECKING

import pytz
import yaml
from platformdirs import user_config_path, user_data_path
from rich import print as rprint

if TYPE_CHECKING:
    from pathlib import Path


def main() -> None:
    """Execute the What to Wear app."""
    app_name = 'what-to-wear'

    config_dir, data_dir = make_platform_dirs(app_name)

    config_file = config_dir / 'config.yaml'

    state_file = data_dir / 'rotation_state.json'

    closet, office_days = load_config(config_file)

    state = load_state(state_file)

    today = datetime.now(pytz.timezone('America/New_York')).date()

    shirt, pants, state_updated = get_outfit_for(
        when=today,
        closet=closet,
        office_days=office_days,
        state=state,
    )

    save_state(state_updated, state_file)

    display_outfit(today, shirt, pants)


def make_platform_dirs(app_name: str) -> tuple[Path, Path]:
    """Make platform-specific directories for the app.

    Args:
        app_name (str): The name of the app.

    """
    config_dir = user_config_path(app_name)

    data_dir = user_data_path(app_name)

    for directory in (config_dir, data_dir):
        directory.mkdir(exist_ok=True)

    return config_dir, data_dir


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
            'last-worn-casual-outfits': 7,
            'last-worn-work-outfits': 2,
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


def get_outfit_for(
        when: date,
        closet: dict[str, list[dict[str, str]]],
        office_days: list[str],
        state: dict[str, int | str]
) -> tuple[str, str, dict[str, int | str]]:
    """Get the outfit for `when`.

    Args:
        when (date): The date for which to get the outfit.
        closet (dict[str, list[dict[str, str]]]): A dictionary
            describing clothes in the closet.
        office_days (list[str]): A tuple of office day indices.
        state (dict[str, int]): The current state.

    Returns:
        tuple[str, str]: The shirt and the pants.

    """
    state_updated = state.copy()

    weekday = list(calendar.day_name)[when.weekday()]

    is_office_day = weekday in office_days

    closet_section = 'work-outfits' if is_office_day else 'casual-outfits'

    key = f'last-worn-{closet_section}'

    last_worn = int(state.get(key, -1))

    next_index = (last_worn + 1) % len(closet[closet_section])

    stored_date = state.get('date-last-updated', '')

    today_iso = (
        datetime.now(pytz.timezone('America/New_York')).date().isoformat()
    )

    if stored_date == -1:
        shirt, pants = closet[closet_section][next_index].values()

        return shirt, pants, state_updated

    if stored_date != today_iso:
        state_updated[key] = next_index

        state_updated['date-last-updated'] = today_iso

        shirt, pants = closet[closet_section][next_index].values()

        return shirt, pants, state_updated

    current_index = int(
        state.get(key, next_index)) % len(closet[closet_section]
    )

    shirt, pants = closet[closet_section][current_index].values()

    return shirt, pants, state_updated


def display_outfit(today: date, shirt: str, pants: str) -> None:
    """Display the outfit for today.

    Args:
        today (date): Today.
        shirt (str): The shirt to wear.
        pants (str): The pants to wear.

    """
    today_name = today.strftime('%A')

    rprint(f'Today is {today_name}.')

    rprint(f'{shirt.capitalize()} shirt with {pants} pants.')


if __name__ == '__main__':
    main()
