"""Module for displaying information to the user."""

from datetime import date

from rich import print as rprint


def display_outfit(
        day: date,
        today: date,
        shirt: str,
        pants: str,
        *,
        is_office_day: bool
) -> None:
    """Display the outfit for today.

    Args:
        day (date): The day to display the outfit for.
        today (date): Today.
        shirt (str): The shirt to wear.
        is_office_day (bool): Whether it's an office day.
        pants (str): The pants to wear.

    """
    prefix = 'Today is' if day == today else 'That day will be'

    day_name = day.strftime('%A')

    rprint(f'{prefix} {day_name}.')

    outfit_type = 'work' if is_office_day else 'casual'

    rprint(
        f'{outfit_type.capitalize()} outfit: '
        f'{shirt} shirt with {pants} pants.'
    )
