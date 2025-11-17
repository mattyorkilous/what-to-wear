"""Execute the What to Wear app."""

import typer

from what_to_wear.closet import get_outfit_for, reset_state
from what_to_wear.display import display_outfit
from what_to_wear.initialize import initialize
from what_to_wear.io import save_state
from what_to_wear.utils import check_is_office_day, get_today, str_to_date

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
    closet, office_days, state, today, state_file = initialize(
        app_name='what-to-wear'
    )

    day = str_to_date(when) if when else today

    shirt, pants, is_office_day, state_updated = get_outfit_for(
        day,
        closet,
        office_days,
        state,
        today
    )

    display_outfit(day, today, shirt, pants, is_office_day=is_office_day)

    save_state(state_updated, state_file)


@app.command()
def reset(
    shirt: str = typer.Argument(...),
    when: str = typer.Argument(get_today().strftime('%Y-%m-%d'))
) -> None:
    """Reset the state file to the given shirt and pants.

    Args:
        when (str): The date to reset. Default is today.
        shirt (str): The shirt to reset to.

    """
    closet, office_days, state, today, state_file = initialize(
        app_name='what-to-wear'
    )

    day = str_to_date(when) if when else today

    state_updated = reset_state(day, shirt, closet, office_days, state, today)

    save_state(state_updated, state_file)


@app.command()
def stay_home() -> None:
    """Stay home and wear casual clothes even if it's an office day.

    This command gets the next casual outfit and resets the work outfit
    state to what it was before the main call that day.

    """
    closet, office_days, state, today, state_file = initialize(
        app_name='what-to-wear'
    )

    is_office_day = check_is_office_day(today, office_days)

    casual_outfits = closet.get('casual-outfits', [])

    last_worn_casual = int(state.get('last-worn-casual-outfits', -1))

    next_casual_index = (last_worn_casual + 1) % len(casual_outfits)

    shirt, pants = casual_outfits[next_casual_index].values()

    state['last-worn-casual-outfits'] = next_casual_index

    state['date-last-updated'] = today.isoformat()

    if is_office_day:
        last_worn_work = int(state.get('last-worn-work-outfits', -1))

        state['last-worn-work-outfits'] = last_worn_work - 1

    save_state(state, state_file)

    display_outfit(today, today, shirt, pants, is_office_day=False)


if __name__ == '__main__':
    app()
