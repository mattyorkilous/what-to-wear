"""Module for getting outfits from the closet."""

from datetime import date

from .utils import check_is_office_day


def get_outfit_for(
        day: date,
        closet: dict[str, list[dict[str, str]]],
        office_days: list[str],
        state: dict[str, int | str],
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
        tuple[str, str, bool, dict[str, int | str]]]: The shirt, pants,
        whether it's an office day, and the updated state.

    """
    state_updated = state.copy()

    is_office_day = check_is_office_day(day, office_days)

    closet_section = 'work-outfits' if is_office_day else 'casual-outfits'

    key = f'last-worn-{closet_section}'

    last_worn = int(state.get(key, -1))

    outfits = closet.get(closet_section, [])

    next_index = (last_worn + 1) % len(outfits)

    stored_date = state.get('date-last-updated', '')

    today_iso = (today.isoformat())

    if stored_date == '':
        shirt, pants = outfits[next_index].values()

        return shirt, pants, is_office_day, state_updated

    if stored_date != today_iso:
        state_updated[key] = next_index

        state_updated['date-last-updated'] = today_iso

        shirt, pants = outfits[next_index].values()

        return shirt, pants, is_office_day, state_updated

    current_index = int(state.get(key, next_index)) % len(outfits)

    shirt, pants = outfits[current_index].values()

    return shirt, pants, is_office_day, state_updated
