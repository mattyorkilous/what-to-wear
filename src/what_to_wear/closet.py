"""Module for getting outfits from the closet."""

from datetime import date
from typing import Any

from what_to_wear.utils import check_is_office_day


def get_outfit_for(
        day: date,
        closet: dict[str, list[dict[str, str]]],
        office_days: list[str],
        state: dict[str, Any],
        today: date
) -> tuple[str, str, bool, dict[str, int | str]]:
    """Get the outfit for `when`.

    Args:
        day (date): The date for which to get the outfit.
        closet (dict[str, list[dict[str, str]]]): A dictionary
            describing clothes in the closet.
        office_days (list[str]): A tuple of office day indices.
        state (dict[str, int]): The current state.
        today (date): Today's date.

    Returns:
        tuple[str, str, bool, dict[str, Any]]]: The shirt, pants,
        whether it's an office day, and the updated state.

    """
    is_office_day, closet_section, outfits = _process_closet(
        closet,
        day,
        office_days
    )

    current_key = f'current-{closet_section}'

    current_index = state[current_key]

    date_last_queried = state['date-last-queried']

    reference_day = today if day > today else date_last_queried

    delta = (day - reference_day).days

    next_index = current_index+delta % len(outfits)

    if day > today:
        shirt, pants = _get_outfit_from_index(next_index, outfits)

        return shirt, pants, is_office_day, state

    if day > date_last_queried:
        shirt, pants = _get_outfit_from_index(next_index, outfits)

        state_updated = _update_state(state, current_key, next_index, today)

        return shirt, pants, is_office_day, state_updated

    if day == date_last_queried:
        shirt, pants = _get_outfit_from_index(current_index, outfits)

        return shirt, pants, is_office_day, state

    msg = '`when` must be in the present or future.'

    raise ValueError(msg)


def reset_state(
        day: date,
        shirt: str,
        closet: dict[str, list[dict[str, str]]],
        office_days: list[str],
        state: dict[str, Any],
        today: date
) -> dict[str, Any]:
    """Reset the state to wear `shirt` on `day`.

    Args:
        day (date): The day to reset.
        shirt (str): The shirt to which to reset.
        closet (dict[str, list[dict[str, str]]]): The closet.
        office_days (list[str]): The office days.
        state (dict[str, Any]): The current state.
        today (date): Today.

    Returns:
        dict[str, Any]: The updated state.

    """
    _, closet_section, outfits = _process_closet(
        closet,
        day,
        office_days
    )

    current_key = f'current-{closet_section}'

    shirts = [outfit['shirt'] for outfit in outfits]

    new_index = shirts.index(shirt)

    state_updated = _update_state(state, current_key, new_index, today)

    return state_updated


def _process_closet(
        closet: dict[str, list[dict[str, str]]],
        day: date,
        office_days: list[str]
) -> tuple[bool, str, list[dict[str, str]]]:
    is_office_day = check_is_office_day(day, office_days)

    closet_section = 'work-outfits' if is_office_day else 'casual-outfits'

    outfits = closet[closet_section]

    return is_office_day, closet_section, outfits


def _get_outfit_from_index(
        index: int,
        outfits: list[dict[str, str]]
) -> tuple[str, str]:
    shirt, pants = outfits[index].values()

    return shirt, pants


def _update_state(
        state: dict[str, Any],
        current_key: str,
        index: int,
        today: date
) -> dict[str, Any]:
    state_updated = state.copy()

    state_updated[current_key] = index

    state_updated['date-last-queried'] = today

    return state_updated
