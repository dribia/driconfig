# DriConfig

<p style="text-align: center; padding-bottom: 1rem;">
    <a href="/driconfig">
        <img
            src="./img/logo_dribia_blau_cropped.png"
            alt="Dribia"
            style="display: block; margin-left: auto; margin-right: auto; width: 40%;"
        >
    </a>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             |
|---------|---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Tests](https://github.com/dribia/driconfig/actions/workflows/test.yml/badge.svg)](https://github.com/dribia/driconfig/actions/workflows/test.yml) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/driconfig)](https://codecov.io/gh/dribia/driconfig) [![Tests](https://github.com/dribia/driconfig/actions/workflows/lint.yml/badge.svg)](https://github.com/dribia/driconfig/actions/workflows/lint.yml) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/driconfig)](https://pypi.org/project/driconfig/) ![PyPI - Downloads](https://img.shields.io/pypi/dm/driconfig?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/driconfig?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/dribia/driconfig?color=blue)](https://github.com/dribia/driconfig/blob/main/LICENSE)                                                                                                                                                                                                                                                             |

<p style="text-align: center;">
    <em>A Pydantic-ish way to manage your project's YAML configurations.</em>
</p>

---

**Documentation**: <a href="https://dribia.github.io/driconfig" target="_blank">https://dribia.github.io/driconfig</a>

**Source Code**: <a href="https://github.com/dribia/driconfig" target="_blank">https://github.com/dribia/driconfig</a>

---

The usage of YAML files to store configurations and parameters is widely accepted in the Python
community, especially in Data Science environments.

DriConfig provides a clean interface between your Python code and these YAML configuration files.

It is heavily based on [Pydantic](https://pydantic-docs.helpmanual.io)'s [Settings Management](https://pydantic-docs.helpmanual.io/usage/settings/),
preserving its core functionalities and advantages.

## Key features

* Subclassing the `DriConfig` class we create an **interface to any YAML configuration file**.
* Our project's **configurations are** then **attributes** of this class.
* They are **automatically filled** with the values in the YAML configuration file.
* We can define **complex configuration structures** using Pydantic models.
* We preserve Pydantic's **type casting and validation**!

## Example
Let's say we have a YAML configuration file `config.yaml` with the following data:
```yaml
# config.yaml
model_parameters:
  eta: 0.2
  gamma: 2
  lambda: 1

date_interval:
  start: 2021-01-01
  end: 2021-12-31
```
Then we can configparse with `driconfig` as follows:
```python
from datetime import date
from typing import Dict

from driconfig import DriConfig, DriConfigConfigDict
from pydantic import BaseModel


class DateInterval(BaseModel):
  """Model for the `date_interval` configuration."""
  start: date
  end: date


class AppConfig(DriConfig):
   """Interface for the config/config.yaml file."""

    """Configure the YAML file location."""
    model_config = DriConfigConfigDict(
        config_folder=".",
        config_file_name="config.yaml",
    )
   model_parameters: Dict[str, float]
   date_interval: DateInterval

config = AppConfig()
print(config.model_dump_json(indent=4))
"""
{
    "model_parameters": {
        "eta": 0.2,
        "gamma": 2.0,
        "lambda": 1.0
    },
    "date_interval": {
        "start": "2021-01-01",
        "end": "2021-12-31"
    }
}
"""
```
