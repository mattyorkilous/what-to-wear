"""Execute the What to Wear app."""

from datetime import datetime

import pytz
import typer

from what_to_wear.closet import get_outfit_for
from what_to_wear.display import display_outfit
from what_to_wear.initialize import initialize
from what_to_wear.state import save_state
from what_to_wear.utils import check_is_office_day

app = typer.Typer()

@app.callback(invoke_without_command=True)
def show(
    when: str = typer.Option(None, '--when', '-w', help='Date (YYYY-MM-DD)')
) -> None:
    """Display the outfit for the given date.

    Args:
        when (Optional[str]): The data for which to get the outfit. If
            None, use today.

    """
    state_file, closet, office_days, state, today = initialize(
        app_name='what-to-wear'
    )

    day = (
        datetime
            .strptime(when, '%Y-%m-%d')
            .astimezone(pytz.timezone('America/New_York'))
            .date()
        if when else today
    )

    shirt, pants, is_office_day, state_updated = get_outfit_for(
        day=day,
        closet=closet,
        office_days=office_days,
        state=state,
        today=today
    )

    save_state(state_updated, state_file)

    display_outfit(today, shirt, pants, is_office_day=is_office_day)


@app.command()
def reset(shirt: str = typer.Argument(...)) -> None:
    """Reset the state file to the given shirt and pants.

    Args:
        shirt (str): The shirt to reset to.

    """
    state_file, closet, office_days, state, today = initialize(
        app_name='what-to-wear'
    )

    is_office_day = check_is_office_day(today, office_days)

    closet_section = 'work-outfits' if is_office_day else 'casual-outfits'

    outfits = closet.get(closet_section, [])

    for index, outfit in enumerate(outfits):
        if outfit['shirt'] == shirt:
            state[f'last-worn-{closet_section}'] = index - 1

            break

    save_state(state, state_file)


if __name__ == '__main__':
    app()
