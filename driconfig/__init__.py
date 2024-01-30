"""Pydantic-ish way to manage YAML configurations.

This module is heavily inspired in Pydantic's Settings management.

Dribia Data Research 2021
"""

from __future__ import annotations as _annotations

import os
from collections.abc import Mapping
from importlib.metadata import version
from pathlib import Path
from typing import (
    Any,
    ClassVar,
    Type,
)

import yaml
from pydantic import BaseModel, ConfigDict
from pydantic.fields import FieldInfo
from pydantic.v1.utils import deep_update
from pydantic_settings import BaseSettings
from pydantic_settings.sources import (
    EnvSettingsSource,
    InitSettingsSource,
    PydanticBaseSettingsSource,
)
from yaml import YAMLError

__version__ = version(__name__)


class DriConfigConfigDict(ConfigDict, total=False):
    """DriConfig configuration dictionary."""

    case_sensitive: bool
    config_file_name: str | None
    config_folder: Path | None
    config_file_encoding: str | None
    config_prefix: str | None


class YAMLConfigError(YAMLError):
    """Error in YAML configuration file."""

    pass


class DriConfig(BaseModel):
    """Base class with for project configurations.

    All of its values can be overridden by values found in a YAML
    configuration file.

    """

    def __init__(
        __pydantic_self__,
        _case_sensitive: bool | None = None,
        _config_file_name: str | None = None,
        _config_folder: Path | str | None = None,
        _config_file_encoding: str | None = None,
        _config_prefix: str | None = None,
        **values: Any,
    ) -> None:
        """Initialization parameters.

        It allows to define on initialization the YAML config file name
        and folder, and its encoding. However, those parameters should
        be configured by overriding them in the internal Config class.

        It also allows to provide any configuration value defined as a
        class attribute. However, it would defeat the purpose, since
        they should be defined in a YAML configuration file.

        Args:
            _config_file_name: YAML configuration file name.
            _config_folder: YAML configuration folder.
            _config_file_encoding: YAML configuration file encoding.
            _config_prefix: YAML configuration prefix.
            **values: Any config value.
        """
        # Uses something other than `self` the first arg
        # to allow "self" as a settable attribute
        super().__init__(
            **__pydantic_self__._config_build_values(
                values,
                _case_sensitive=_case_sensitive,
                _config_file_name=_config_file_name,
                _config_folder=_config_folder,
                _config_file_encoding=_config_file_encoding,
                _config_prefix=_config_prefix,
            )
        )

    @classmethod
    def config_customise_sources(
        cls,
        settings_cls: Type[DriConfig],
        init_config: PydanticBaseSettingsSource,
        yaml_config: PydanticBaseSettingsSource,
    ) -> tuple[PydanticBaseSettingsSource, ...]:
        """Define the sources and their order for loading the settings values.

        Args:
            settings_cls: The Settings class.
            init_config: The `InitConfigSource` instance.
            yaml_config: The `YamlConfigSource` instance.

        Returns:
            A tuple containing the sources and their order for loading the settings values.
        """
        return init_config, yaml_config

    def _config_build_values(
        self,
        init_kwargs: dict[str, Any],
        _case_sensitive: bool | None = None,
        _config_file_name: str | None = None,
        _config_folder: Path | str | None = None,
        _config_file_encoding: str | None = None,
        _config_prefix: str | None = None,
    ) -> dict[str, Any]:
        """Build the configuration values based on init and YAML.

        We prioritize initialization values over configured values
        in the YAML file. However, the purpose of this class is to
        define the configuration values via a YAML configuration
        file!

        Args:
            init_kwargs: Initialization arguments.
            _config_file_name: YAML configuration file name.
            _config_folder: YAML configuration folder.
            _config_file_encoding: YAML configuration file encoding.
            _config_prefix: YAML configuration prefix.

        Returns: The value dictionary.

        """
        case_sensitive = (
            _case_sensitive
            if _case_sensitive is not None
            else self.model_config.get("case_sensitive")
        )
        config_file_name = (
            _config_file_name
            if _config_file_name is not None
            else self.model_config.get("config_file_name")
        )
        config_folder = (
            _config_folder
            if _config_folder is not None
            else self.model_config.get("config_folder")
        )
        config_file_encoding = (
            _config_file_encoding
            if _config_file_encoding is not None
            else self.model_config.get("config_file_encoding")
        )
        config_prefix = (
            _config_prefix
            if _config_prefix is not None
            else self.model_config.get("config_prefix")
        )
        init_config = InitSettingsSource(
            self.__class__,  # type: ignore
            init_kwargs=init_kwargs,
        )
        yaml_config = YamlConfigSource(
            self.__class__,  # type: ignore
            config_file_name=config_file_name,
            config_folder=config_folder,
            config_file_encoding=config_file_encoding,
            config_prefix=config_prefix,
            case_sensitive=case_sensitive,
        )
        sources = self.config_customise_sources(
            self.__class__,
            init_config=init_config,
            yaml_config=yaml_config,
        )
        if sources:
            return deep_update(*reversed([source() for source in sources]))
        else:
            return {}

    model_config: ClassVar[DriConfigConfigDict] = DriConfigConfigDict(
        extra="forbid",
        arbitrary_types_allowed=True,
        validate_default=True,
        case_sensitive=False,
        protected_namespaces=("model_", "config_"),
        config_prefix=None,
        config_folder=None,
        config_file_name=None,
    )


class InitConfigSource(InitSettingsSource):
    """Configuration source from the __init__ arguments."""

    def __repr__(self) -> str:
        """Class representation."""
        return f"InitConfigSource(init_kwargs={self.init_kwargs!r})"


class YamlConfigSource(EnvSettingsSource):
    """Configuration source from the YAML configuration file."""

    def __init__(
        self,
        settings_cls: Type[BaseSettings],
        config_file_name: str | None = None,
        config_folder: Path | str | None = None,
        config_file_encoding: str | None = None,
        case_sensitive: bool | None = None,
        config_prefix: str | None = None,
    ):
        """Initialize the YAML configurations source.

        Args:
            settings_cls: The DriConfig class.
            config_file_name: YAML configuration file name.
            config_folder: YAML configuration folder.
            config_file_encoding: YAML configuration encoding.
            case_sensitive: Whether to use case-sensitive keys.
            config_prefix: YAML configuration prefix.
        """
        super().__init__(
            settings_cls,
            case_sensitive=case_sensitive,
            env_prefix=None,
            env_nested_delimiter=None,
        )
        self.config_file: Path | None = None
        self.case_sensitive: bool = case_sensitive
        self.config_prefix: str = config_prefix
        if config_file_name is not None and config_folder is not None:
            self.config_file = Path(config_folder) / config_file_name
        self.config_file_encoding: str | None = config_file_encoding
        self.env_vars = self._load_config_vars()

    def _load_config_vars(self) -> dict[str, Any]:
        """Load configuration variables from the YAML file."""
        return self._read_config_files(self.case_sensitive, self.config_prefix)

    def _read_config_files(self, case_sensitive: bool, config_prefix: str):
        if self.config_file is None:
            return {}
        if isinstance(self.config_file, (str, os.PathLike)):
            config_file = self.config_file

        config_vars: dict[str, str | None] = {}

        config_path = Path(config_file).expanduser()
        if config_path.is_file():
            yaml_file = read_yaml_file(
                config_path,
                encoding=self.config_file_encoding,
                case_sensitive=case_sensitive,
                config_prefix=config_prefix,
            )
            if not isinstance(yaml_file, Mapping):
                raise YAMLConfigError(
                    f"The YAML configuration file must be a "
                    f"mapping and not a '{type(yaml_file).__name__}'."
                )
            config_vars.update(yaml_file)

        return config_vars

    def prepare_field_value(
        self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool
    ) -> Any:
        """Prepare the field value."""
        if isinstance(value, dict):
            deep_update(value, self.explode_env_vars(field_name, field, self.env_vars))
        return value

    def __repr__(self) -> str:
        """Class representation."""
        return (
            f"YamlConfigSource(config_file={str(self.config_file)!r}, "
            f"config_file_encoding={self.config_file_encoding!r})"
        )


def read_yaml_file(
    file_path: Path,
    *,
    encoding: str = None,
    case_sensitive: bool = False,
    config_prefix: str = None,
) -> dict[str, str | None]:
    """Parse a YAML configuration file.

    Args:
        file_path: YAML configuration file path.
        encoding: YAML configuration file encoding.
        case_sensitive: Whether read variables case-sensitively.
        config_prefix: YAML configuration prefix.
    Returns: Parsed YAML configuration file.

    """
    with open(file_path, "r", encoding=encoding or "utf8") as f:
        file_vars: dict[str, Any] = yaml.load(f, Loader=yaml.SafeLoader)
    if config_prefix is not None:
        file_vars = {k.replace(config_prefix, ""): v for k, v in file_vars.items()}
    if not case_sensitive:
        try:
            return {k.lower(): v for k, v in file_vars.items()}
        except AttributeError:
            return file_vars
    else:
        return file_vars
