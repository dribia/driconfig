"""driconfig package test module.

Dribia 2021/01/11, Albert Iribarne <iribarne@dribia.com>
"""

import re

import pytest
from pydantic import ValidationError

import driconfig
from driconfig import DriConfig, InitConfigSource, YAMLConfigError, YamlConfigSource


def test_version():
    """Assert that `__version__` exists and is valid."""
    assert re.match(r"\d.\d.\d", driconfig.__version__)


def test_driconfig(config_path):
    """Test DriConfig."""

    class AppConfig(DriConfig):
        """Test configuration."""

        class Config:
            config_folder = config_path
            config_file_name = "config.yaml"
            case_sensitive = False

        foo: str
        case_sensitive: str = "is_case_sensitive"

    app_config = AppConfig()
    assert isinstance(app_config.foo, str)
    assert app_config.case_sensitive == "is_not_case_sensitive"


def test_driconfig_insensitive(config_path):
    """Test DriConfig."""

    class AppConfig(DriConfig):
        """Test configuration."""

        class Config:
            config_folder = config_path
            config_file_name = "config.yaml"
            case_sensitive = True

        foo: str
        case_sensitive: str = "is_case_sensitive"

    app_config = AppConfig()
    assert isinstance(app_config.foo, str)
    assert app_config.case_sensitive == "is_case_sensitive"


def test_driconfig_fail():
    """Test DriConfig."""

    class AppConfig(DriConfig):
        """Test DriConfig."""

        foo: str

    with pytest.raises(ValidationError):
        AppConfig()


def test_builtins_settings_source_repr():
    """Test representation methods."""
    assert (
        repr(InitConfigSource(init_kwargs={"apple": "value 0", "banana": "value 1"}))
        == "InitConfigSource(init_kwargs={'apple': 'value 0', 'banana': 'value 1'})"
    )
    assert (
        repr(
            YamlConfigSource(
                config_folder="foo",
                config_file_name="bar",
                config_file_encoding="utf-8",
            )
        )
        == "YamlConfigSource(config_file='foo/bar', config_file_encoding='utf-8')"
    )


def test_customise_sources_empty():
    """Test empty customize sources method."""

    class AppConfig(DriConfig):
        apple: str = "default"
        banana: str = "default"

        class Config:
            @classmethod
            def customise_sources(cls, *args, **kwargs):
                return ()

    assert AppConfig().dict() == {"apple": "default", "banana": "default"}
    assert AppConfig(apple="xxx").dict() == {"apple": "default", "banana": "default"}


def test_catch_on_non_str_key(config_path):
    """Test catch of the non-string key yaml case."""

    class AppConfig(DriConfig):
        class Config:
            config_folder = config_path
            config_file_name = "config_non_str.yaml"
            case_sensitive = False

    app_config = AppConfig()
    assert isinstance(app_config, AppConfig)


def test_yaml_config_error(config_path):
    """Test the YAMLConfigError exception raising."""

    class AppConfig(DriConfig):
        class Config:
            config_folder = config_path
            config_file_name = "config_non_mapping.yaml"

    with pytest.raises(YAMLConfigError):
        _ = AppConfig()
