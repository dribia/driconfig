DriConfig mimics Pydantic's [Settings Management](https://pydantic-docs.helpmanual.io/usage/settings/)
functionality, working with YAML configurations instead of environment variables or `.env` files.

## The YAML language

YAML is a human-readable data-serialization language, commonly used for configuration files.
It natively encodes scalars (such as strings, integers, and floats), lists, and dictionaries.

```yaml
# config.yaml

parameter_a: "some string"
parameter_b: 1
parameter_c: 1.2
parameter_d: ["I'm", "a", "list"]
```

The above code block contains a sample configuration file written in the YAML language.

!!! info
    If you want to run the rest of the code blocks in this document, place the contents of the
    previous one into a file called `config.yaml` in your working directory.

!!! tip
    A YAML configuration file should always be a dictionary at its first level.
    The elements of this dictionary, then, could be of any type (scalars, lists or dictionaries).

The goal of DriConfig is to provide an interface between your Python code and such YAML confguration files.

## The DriConfig class
DriConfig provides a base configuration class called `DriConfig`. This base class should be sub-classed in order
to generate custom configuration classes that represent YAML configuration files.

```python
from driconfig import DriConfig

class AppConfig(DriConfig):  # Inherits the base DriConfig class.
    """Empty configuration class."""

    pass

app_config = AppConfig()

print(app_config.model_dump_json())
"""
{}
"""
```

### The DriConfig's DriConfigConfigDict dictionary
Now, we would want to read and parse the `config.yaml` file we created before.
We need to configure our `AppConfig` class in order to point at that file.

```python
from driconfig import DriConfig, DriConfigConfigDict

class AppConfig(DriConfig):
    """Empty configuration class."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

app_config = AppConfig()

print(app_config.model_dump_json())
"""
{}
"""
```

!!! warning
    In Pydantic V2, to specify config on a model, you should set
    a class attribute called model_config to be a dict with the
    key/value pairs you want to be used as the config.
    The Pydantic V1 behavior to create a
    [class called Config](https://pydantic-docs.helpmanual.io/usage/model_config/)
    in the namespace of the parent `BaseModel` subclass is now deprecated.

!!! note
    We have extended the use of
    [Pydantic `ConfigDict` dictionary](https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict)
    to host the YAML file information.
    In the [ConfigDict](configdict.md) section we detail which configurations have been
    added or modified.

### Parsing YAML configurations
Now we would want to parse the configurations we put on our `config.yaml` file.

```python
from typing import List

from driconfig import DriConfig, DriConfigConfigDict

class AppConfig(DriConfig):
    """Configuration class to parse the config.yaml file contents."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

    parameter_a: str
    parameter_b: int
    parameter_c: float
    parameter_d: List[str]

app_config = AppConfig()

print(app_config.model_dump_json(indent=4))
"""
{
    "parameter_a": "some string",
    "parameter_b": 1,
    "parameter_c": 1.2,
    "parameter_d": [
        "I'm",
        "a",
        "list"
    ]
}
"""
```

Note how we declared the configuration variable types following Pydantic's syntax.
In fact, while parsing the `config.yaml` file DriConfig is performing **type validation**,
so that if your configuration variable value is of an undesired type it will raise a validation error.

```python
from driconfig import DriConfig, DriConfigConfigDict
from pydantic import ValidationError

class AppConfig(DriConfig):
    """Configuration class to parse the config.yaml file contents."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

    parameter_a: int

try:
    app_config = AppConfig()
except ValidationError as e:
    print(e)
"""
1 validation error for AppConfig
parameter_a
  Input should be a valid integer, unable to parse string as an integer [type=int_parsing, input_value='some string', input_type=str]
    For further information visit https://errors.pydantic.dev/2.2/v/int_parsing
"""
```

As you can guess, all the benefits from Pydantic are hold by the `DriConfig` base class.
Then, apart from raising errors on incorrect types, values are casted to the correct
type when possible, and even [nested configurations](nested_models.md) can be expressed as nested Pydantic models.

In particular, also the default values behavior is preserved from Pydantic. This is, we could define
a default value for a given configuration, so that if the configuration is not present in the YAML
configuration file, it gets the default value from the configuration class definition.

```python hl_lines="18 33"
from typing import List

from driconfig import DriConfig, DriConfigConfigDict

class AppConfig(DriConfig):
    """Configuration class to parse the config.yaml file contents."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

    parameter_a: str
    parameter_b: int
    parameter_c: float
    parameter_d: List[str]
    parameter_e: str = "default value"

app_config = AppConfig()

print(app_config.model_dump_json(indent=4))
"""
{
    "parameter_a": "some string",
    "parameter_b": 1,
    "parameter_c": 1.2,
    "parameter_d": [
        "I'm",
        "a",
        "list"
    ],
    "parameter_e": "default_value
}
"""
```

Now, if we add `parameter_e` to our `config.yaml` file:
```yaml hl_lines="7"
# config.yaml

parameter_a: "some string"
parameter_b: 1
parameter_c: 1.2
parameter_d: ["I'm", "a", "list"]
parameter_e: "custom value"
```
We see how it prevails over the default value:
```python hl_lines="33"
from typing import List

from driconfig import DriConfig, DriConfigConfigDict

class AppConfig(DriConfig):
    """Configuration class to parse the config.yaml file contents."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

    parameter_a: str
    parameter_b: int
    parameter_c: float
    parameter_d: List[str]
    parameter_e: str = "default value"

app_config = AppConfig()

print(app_config.model_dump_json(indent=4))
"""
{
    "parameter_a": "some string",
    "parameter_b": 1,
    "parameter_c": 1.2,
    "parameter_d": [
        "I'm",
        "a",
        "list"
    ],
    "parameter_e": "custom value"
}
"""
```
