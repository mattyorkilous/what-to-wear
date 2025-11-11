"""Module for displaying information to the user."""

from datetime import date

from rich import print as rprint


def display_outfit(
        today: date,
        shirt: str,
        pants: str,
        *,
        is_office_day: bool
) -> None:
    """Display the outfit for today.

    Args:
        today (date): Today.
        shirt (str): The shirt to wear.
        is_office_day (bool): Whether it's an office day.
        pants (str): The pants to wear.

    """
    today_name = today.strftime('%A')

    rprint(f'Today is {today_name}.')

    outfit_type = 'work' if is_office_day else 'casual'

    rprint(
        f'{outfit_type.capitalize()} outfit: '
        f'{shirt} shirt with {pants} pants.'
    )
