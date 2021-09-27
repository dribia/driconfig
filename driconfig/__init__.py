"""Pydantic-ish way to manage YAML configurations.

This module is heavily inspired in Pydantic's Settings management.

Dribia Data Research 2021
"""

from collections.abc import Mapping
from pathlib import Path
from typing import AbstractSet, Any, Callable, Dict, List, Optional, Tuple, Union

import yaml
from pydantic import BaseConfig, BaseModel, Extra
from pydantic.fields import ModelField
from pydantic.utils import deep_update
from yaml import YAMLError

try:
    from importlib.metadata import version  # type: ignore
except ModuleNotFoundError:
    from importlib_metadata import version  # type: ignore

__version__ = version(__name__)

config_file_sentinel = str(object())
config_folder_sentinel = str(object())

ConfigsSourceCallable = Callable[["DriConfig"], Dict[str, Any]]


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
        _config_file_name: Union[str, None] = config_file_sentinel,
        _config_folder: Union[Path, str, None] = config_folder_sentinel,
        _config_file_encoding: Optional[str] = None,
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
            **values: Any config value.
        """
        # Uses something other than `self` the first arg
        # to allow "self" as a settable attribute
        super().__init__(
            **__pydantic_self__._build_values(
                values,
                _config_file_name=(
                    _config_file_name
                    if _config_file_name != config_file_sentinel
                    else __pydantic_self__.__config__.config_file_name
                ),
                _config_folder=(
                    _config_folder
                    if _config_folder != config_folder_sentinel
                    else __pydantic_self__.__config__.config_folder
                ),
                _config_file_encoding=(
                    _config_file_encoding
                    if _config_file_encoding is not None
                    else __pydantic_self__.__config__.config_file_encoding
                ),
            )
        )

    def _build_values(
        self,
        init_kwargs: Dict[str, Any],
        _config_file_name: Union[str, None] = None,
        _config_folder: Union[Path, str, None] = None,
        _config_file_encoding: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Build the configuration values based on init and YAML.

        We prioritize initialization values over configured values
        in the YAML file. However, the purpose of this class is to
        defined the configuration values via a YAML configuration
        file!

        Args:
            init_kwargs: Initialization arguments.
            _config_file_name: YAML configuration file name.
            _config_folder: YAML configuration folder.
            _config_file_encoding: YAML configuration file encoding.

        Returns: The value dictionary.

        """
        init_config = InitConfigSource(init_kwargs=init_kwargs)
        yaml_config = YamlConfigSource(
            config_file_name=_config_file_name,
            config_folder=_config_folder,
            config_file_encoding=_config_file_encoding,
        )
        sources = self.__config__.customise_sources(
            init_config=init_config, yaml_config=yaml_config
        )
        if sources:
            return deep_update(*reversed([source(self) for source in sources]))
        else:
            return {}

    class Config(BaseConfig):
        """Base internal Config class.

        This class and its attributes can (should) be overridden
        when creating a YAML configuration class.

        """

        config_prefix = ""  # Only load YAML entries with given prefix.
        config_folder = "."  # Folder where the YAML file is located.
        config_file_name = None  # File name of the YAML file.
        config_file_encoding = None  # Encoding of the YAML file.
        validate_all = True
        extra = Extra.forbid
        arbitrary_types_allowed = True
        case_sensitive = False

        @classmethod
        def prepare_field(cls, field: ModelField) -> None:
            """Prepare field for being loaded w/ the configured prefix.

            Args:
                field: Model field.

            Returns: Prepared model field.

            """
            config_names: Union[List[str], AbstractSet[str]]
            config_names = {cls.config_prefix + field.name}
            if not cls.case_sensitive:
                config_names = config_names.__class__(n.lower() for n in config_names)
            field.field_info.extra["config_names"] = config_names

        @classmethod
        def customise_sources(
            cls,
            init_config: ConfigsSourceCallable,
            yaml_config: ConfigsSourceCallable,
        ) -> Tuple[ConfigsSourceCallable, ...]:
            """Join configurations from different sources.

            Here we define the prioritization of initialization values
            over YAML-configured values.

            Args:
                init_config: Initialization values.
                yaml_config: Configured values in YAML.

            Returns: Sorted configuration value sources.

            """
            return init_config, yaml_config

    __config__: Config  # type: ignore


class InitConfigSource:
    """Configuration source from the __init__ arguments."""

    __slots__ = ("init_kwargs",)

    def __init__(self, init_kwargs: Dict[str, Any]):
        """Configurations passed."""
        self.init_kwargs = init_kwargs

    def __call__(self, configs: DriConfig) -> Dict[str, Any]:
        """Obtain configurations."""
        return self.init_kwargs

    def __repr__(self) -> str:
        """Class representation."""
        return f"InitConfigSource(init_kwargs={self.init_kwargs!r})"


class YamlConfigSource:
    """Configuration source from the a YAML configuration file."""

    __slots__ = ("config_file", "config_file_encoding")

    def __init__(
        self,
        config_file_name: Union[str, None],
        config_folder: Union[Path, str, None],
        config_file_encoding: Optional[str],
    ):
        """Initialize the YAML configurations source.

        Args:
            config_file_name: YAML configuration file name.
            config_folder: YAML configuration folder.
            config_file_encoding: YAML configuration encoding.

        """
        self.config_file: Union[Path, None] = None
        if config_file_name is not None and config_folder is not None:
            self.config_file = Path(config_folder) / config_file_name
        self.config_file_encoding: Optional[str] = config_file_encoding

    def __call__(self, configs: DriConfig) -> Dict[str, Any]:
        """Build variables from the YAML configuration file."""
        d: Dict[str, Optional[str]] = {}
        config_vars: Dict[str, Any] = {}
        if self.config_file is not None:
            config_path = Path(self.config_file).expanduser()
            if config_path.is_file():
                yaml_file = read_yaml_file(
                    config_path,
                    encoding=self.config_file_encoding,
                    case_sensitive=configs.__config__.case_sensitive,
                )
                if not isinstance(yaml_file, Mapping):
                    raise YAMLConfigError(
                        f"The YAML configuration file must be a "
                        f"mapping and not a '{type(yaml_file).__name__}'."
                    )
                config_vars = {**yaml_file}

        for field in configs.__fields__.values():
            config_val: Optional[str] = None
            for config_name in field.field_info.extra["config_names"]:
                config_val = config_vars.get(config_name)
                if config_val is not None:
                    break

            if config_val is None:
                continue

            d[field.alias] = config_val
        return d

    def __repr__(self) -> str:
        """Class representation."""
        return (
            f"YamlConfigSource(config_file={str(self.config_file)!r}, "
            f"config_file_encoding={self.config_file_encoding!r})"
        )


def read_yaml_file(
    file_path: Path, *, encoding: str = None, case_sensitive: bool = False
) -> Dict[str, Optional[str]]:
    """Parse a YAML configuration file.

    Args:
        file_path: YAML configuration file path.
        encoding: YAML configuration file encoding.
        case_sensitive: Whether read variables case-sensitively.

    Returns: Parsed YAML configuration file.

    """
    with open(file_path, "r", encoding=encoding or "utf8") as f:
        file_vars: Dict[str, Any] = yaml.load(f, Loader=yaml.SafeLoader)
    if not case_sensitive:
        try:
            return {k.lower(): v for k, v in file_vars.items()}
        except AttributeError:
            return file_vars
    else:
        return file_vars
