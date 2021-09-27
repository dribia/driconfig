"""Test configurations and fixtures.

Dribia 2021/08/04, irene <irene@dribia.com>
"""

from pathlib import Path

import pytest


@pytest.fixture
def config_path() -> Path:
    """Get the config file path within the tests folder."""
    return Path(__file__).parent.resolve() / "config"
