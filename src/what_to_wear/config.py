"""Module for loading the configuration file."""

from pathlib import Path

import yaml


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
