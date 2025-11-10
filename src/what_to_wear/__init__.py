"""Execute the What to Wear app."""
from __future__ import annotations

import json
from datetime import date, datetime
from typing import TYPE_CHECKING

import pytz
from platformdirs import user_data_path

if TYPE_CHECKING:
    from pathlib import Path


def main() -> None:
    """Execute the What to Wear app."""
    app_name = 'what_to_wear'

    state_file = user_data_path(app_name) / 'rotation_state.json'

    state_file.parent.mkdir(parents=True, exist_ok=True)

    closet = {
        'non_office_shirts': (
            'white', 'brown', 'dark green', 'black', 'pink',
            'dark blue', 'beige', 'light blue', 'light green'
        ),
        'non_office_pants': ('dark blue', 'black', 'tan'),
        'office_outfits': (
            ('white', 'dark blue'),
            ('black', 'tan'),
            ('light blue', 'black'),
            ('stripes', 'dark blue'),
            ('dark blue', 'tan'),
        )
    }

    office_days = (1, 2, 3)

    try:
        state = load_state(state_file)
    except FileNotFoundError:
        state = {'non_office_index': 0, 'office_index': 0}

    state = load_state(state_file)

    today = datetime.now(pytz.timezone('America/New_York')).date()

    category, shirt, pants = get_today_outfit(
        state, today, office_days, closet
    )

    save_state(state, state_file)

    today_name = today.strftime('%A')

    print(f'Today is {today_name}.')

    print(f'{category}: {shirt.capitalize()} shirt with {pants} pants.')


def load_state(state_file: Path) -> dict[str, int]:
    """Load the state file.

    Args:
        state_file (Path): Path to the state file.

    Returns:
        dict[str, int]: A dictionary describing state.

    """
    with state_file.open() as f:
        state = json.load(f)

        return state


def save_state(state: dict[str, int], state_file: Path) -> None:
    """Save the current state.

    Args:
        state (dict[str, int]): The existing state.
        state_file (Path): The path to the state file.

    """
    with state_file.open('w') as f:
        json.dump(state, f)


def get_today_outfit(
        state: dict[str, int],
        today: date,
        office_days: tuple[int, ...],
        closet: dict[str, tuple[str, ...]]
) -> tuple[str, str, str]:
    """Get today's outfit.

    Args:
        state (dict[str, int]): The current state.
        today (date): Today.
        office_days (tuple[int, ...]): A tuple of office day indices.
        closet (dict[str, tuple[str, ...]]): A dictionary describing
            clothes in the closet.

    Returns:
        tuple[str, str, str]: The category, the shirt, and the pants.

    """
    state = state.copy()

    office_outfits, non_office_shirts, non_office_pants = (
        closet[key] for key in (
            'office_outfits', 'non_office_shirts', 'non_office_pants'
        )
    )

    weekday = today.weekday()

    is_office_day = weekday in office_days

    if is_office_day:
        state['office_index'] = (
            (state['office_index'] + 1) % len(office_outfits)
        )

        shirt, pants = office_outfits[state['office_index']]

        category = 'Office day outfit'

    else:
        state['non_office_index'] = (
            (state['non_office_index'] + 1) % len(non_office_shirts)
        )

        shirt = non_office_shirts[state['non_office_index']]

        if shirt == 'black':
            pants = 'light blue'
        else:
            pants = non_office_pants[
                state['non_office_index'] % len(non_office_pants)
            ]

        category = 'Non-office outfit'

    return category, shirt, pants


if __name__ == '__main__':
    main()