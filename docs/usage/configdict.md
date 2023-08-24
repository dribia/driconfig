# ConfigDict

## Pydantic's ConfigDict dictionary

A Pydantic model's internal `ConfigDict` dictionary controls many aspects of its functionality.
An exhaustive list can be found in [Pydantic's documentation](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict).

The `DriConfigConfigDict` dictionary, as it inherits from Pydantic's `BaseModel`, has all these configuration options available.

However, we have added some new configuration options, and modified some of its defaults.

## DriConfigConfigDict's dictionary.

### New configurations

| Field            | Type (default)         | Description                                      |
|------------------|---------------|--------------------------------------------------|
| `config_folder`  | `str` (`"config"`)     | Path to the folder where the YAML file is placed. |
| `config_file_name` | `str` (`"config.yaml"`)        | YAML file name. |
| `config_file_encoding` | `Optional[str]` (`None`) | YAML file encoding. If `None`, the `PyYAML` default is used. |
| `config_prefix`  | `str` (`""`)        | Prefix for configuration variable names. |
| `case_sensitive` | `bool` (`False`) | Whether to be case sensitive when reading variables from the YAML configuration file. |

!!! tip
    The `config_prefix` is useful when working with environments, so that configurations can be named e.g. after
    `DEV_`, `PRE_` or `PRO_` prefixes, but accessed with their root names within the code.

    Note that the prefix only affects first-level names in the YAML file. Names in nested configurations
    should not be prefixed.

    ```yaml
    # config.yaml

    PRE_PARENT_CONFIG:
        CHILD_CONFIG_A: 1
        CHILD_CONFIG_B: 1.2
    ```
    ```python
    # main.py

    from typing import Dict

    from driconfig import DriConfig, DriConfigConfigDict


    class AppConfig(DriConfig):
        """Configuration class to parse the config.yaml file contents."""

        """Configure AppConfig to point at the config.yaml file."""
        model_config = DriConfigConfigDict(
            config_folder=".",
            config_file_name="config.yaml",
            config_prefix = "PRE_",
        )

        PARENT_CONFIG: Dict[str, float]


    app_config = AppConfig()
    print(app_config.model_dump_json(indent=4))
    """
    {
        "PARENT_CONFIG": {
            "CHILD_CONFIG_A": 1.0,
            "CHILD_CONFIG_B": 1.2
        }
    }
    """
    ```

### Modified configurations

| Field            | Type (default)         | Description                                      |
|------------------|---------------|--------------------------------------------------|
| `validate_default` | `bool` (`True`) | Defaults to `True` so that validation is done in YAML file parsing. |
| `arbitrary_types_allowed` | `bool` (`True`) | Allow arbitrary types by default. |
| `extra` | `str` (`forbid`) | Forbid extra arguments on initialization by default. |
