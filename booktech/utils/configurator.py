import typing as t

import os
import yaml
from yaml.parser import ParserError


class ConfigError(Exception):
    """A Configuration error"""
    pass


def load_yaml_config(cfg: t.Optional[str] = None):
    """Loads configuration from a yaml file

    Args:
        cfg: Path to config file
    """

    # If no cfg file is provided then proceed to load
    # from environment variable.
    if not cfg:
        cfg = os.getenv("BOOKTECH_CONFIG_FILE")

    if not cfg:
        raise ConfigError("BOOKTECH_CONFIG_FILE env is not set")

    # Test if an absolute path has been given
    if not os.path.exists(cfg):
        raise ConfigError("Couldn't load config file")

    # Load config
    with open(cfg, "r") as f:
        try:
            config = yaml.safe_load(f)
        except ParserError as err:
            raise ConfigError(f"Couldn't load configuration - {err}")

    return config
