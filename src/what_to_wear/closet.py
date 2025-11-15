"""Module for getting outfits from the closet."""

from collections import Counter
from datetime import date, timedelta
from itertools import accumulate
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
    is_office_day, closet_section, outfits, current_key = _process_closet(
        closet,
        day,
        office_days
    )

    current_index, date_last_queried, reference_day, delta = _process_state(
        state,
        current_key,
        day,
        today
    )

    next_index = _calculate_next_index(
        current_index,
        reference_day,
        delta,
        len(outfits),
        closet_section,
        office_days
    )

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
    _, closet_section, outfits, current_key = _process_closet(
        closet,
        day,
        office_days
    )

    current_index, _, reference_day, delta = _process_state(
        state,
        current_key,
        day,
        today
    )

    n_outfits = len(outfits)

    current_next_index = _calculate_next_index(
        current_index,
        reference_day,
        delta,
        n_outfits,
        closet_section,
        office_days
    )

    shirts = [outfit['shirt'] for outfit in outfits]

    shirt_index = shirts.index(shirt)

    new_index = (shirt_index - current_next_index) % n_outfits

    state_updated = _update_state(state, current_key, new_index, today)

    return state_updated


def _process_closet(
        closet: dict[str, list[dict[str, str]]],
        day: date,
        office_days: list[str]
) -> tuple[bool, str, list[dict[str, str]], str]:
    is_office_day = check_is_office_day(day, office_days)

    closet_section = 'work' if is_office_day else 'casual'

    outfits = closet[closet_section]

    current_key = f'current-{closet_section}'

    return is_office_day, closet_section, outfits, current_key


def _process_state(
        state: dict[str, Any],
        current_key: str,
        day: date,
        today: date
) -> tuple[int, date, date, int]:
    current_index = state[current_key]

    date_last_queried = state['date-last-queried']

    reference_day = today if day > today else date_last_queried

    delta = (day - reference_day).days

    return current_index, date_last_queried, reference_day, delta


def _calculate_next_index(
        current_index: int,
        reference_day: date,
        delta: int,
        n_outfits: int,
        closet_section: str,
        office_days: list[str]
) -> int:
    if delta == 0:
        return current_index

    days = list(accumulate(
        range(delta),
        lambda last_day, _: last_day + timedelta(days=1),
        initial=reference_day
    ))

    day_types = [
        'work' if check_is_office_day(day_, office_days) else 'casual'
        for day_ in days
    ]

    day_type_counts = Counter(day_types)

    closet_section_delta = day_type_counts[closet_section] - 1

    next_index = closet_section_delta % n_outfits

    return next_index


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
