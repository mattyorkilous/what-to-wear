"""Execute the What to Wear app."""

from datetime import datetime

import pytz
import typer

from what_to_wear.closet import get_outfit_for
from what_to_wear.config import load_config
from what_to_wear.display import display_outfit
from what_to_wear.state import load_state, save_state
from what_to_wear.utils import (
    check_is_office_day,
    get_config_and_state_files,
    get_today,
)

app = typer.Typer()

@app.command()
def show(when: str = typer.Argument(default=None)) -> None:
    """Execute the What to Wear app.

    Args:
        when (Optional[str]): The data for which to get the outfit. If
            None, use today.

    """
    config_file, state_file = get_config_and_state_files(
        app_name='what-to-wear'
    )

    closet, office_days = load_config(config_file)

    state = load_state(state_file)

    today = get_today()

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
    config_file, state_file = get_config_and_state_files(
        app_name='what-to-wear'
    )

    closet, office_days = load_config(config_file)

    state = load_state(state_file)

    today = get_today()

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
