Being able to use Pydantic models to parse nested configurations on our YAML files is maybe the
strongest point of DriConfig.

Let's say we have a YAML `config.yaml` file looking like this:

```yaml
# config.yaml

timeout: 1000
min_date: 2021-04-17
model_parameters:
  alpha: 2
  beta: 0.1
  gamma: 30
```

In this case, `model_parameters` is what we call a *nested configuration*, being a *dictionary of dictionaries*.

Then, we would have two options:

* Parse `model_parameters` as a `dict` type.
* Parse it as a Pydantic model, and performing specific type validation for each of its values.

## Arbitrary types
Let's parse the `model_parameters` configuration as an arbitrary dictionary.
```python
from datetime import date
from typing import Any, Dict

from driconfig import DriConfig, DriConfigConfigDict


class AppConfig(DriConfig):
    """Configuration class to parse the config.yaml file contents."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

    timeout: int
    min_date: date
    model_parameters: Dict[str, Any]

app_config = AppConfig()
print(app_config.model_dump_json(indent=4))
"""
{
    "timeout": 1000,
    "min_date": "2021-04-17",
    "model_parameters": {
        "alpha": 2,
        "beta": 0.1,
        "gamma": 30
    }
}
"""
print(type(app_config.model_parameters))
"""
<class 'dict'>
"""
```

Note that no type validation is performed on the values of `model_paramters`. Instead, it is stored
as an arbitrary dictionary.

## Nested model

Now, let's properly parse `model_parameters` as a Pydantic model.
```python
from datetime import date

from pydantic import BaseModel

from driconfig import DriConfig, DriConfigConfigDict


class ModelParameters(BaseModel):
    """Pydantic model for `model_parameters`."""

    alpha: int
    beta: float
    gamma: int


class AppConfig(DriConfig):
    """Configuration class to parse the config.yaml file contents."""

    """Configure AppConfig to point at the config.yaml file."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )

    timeout: int
    min_date: date
    model_parameters: ModelParameters

app_config = AppConfig()
print(app_config.model_dump_json(indent=4))
"""
{
    "timeout": 1000,
    "min_date": "2021-04-17",
    "model_parameters": {
        "alpha": 2,
        "beta": 0.1,
        "gamma": 30
    }
}
"""
print(type(app_config.model_parameters))
"""
<class '__main__.ModelParameters'>
"""
```

Note how, in this case, type validation *is* performed for `alpha`, `beta` and `gamma`.

We could mimic this pattern to build even deeper nested configuration parsers,
holding all of Pydantic's validation power.
