DriConfig
==========================

<p align="center">
    <a href="https://dribia.github.io/driconfig">
        <picture style="display: block; margin-left: auto; margin-right: auto; width: 40%;">
            <source
                media="(prefers-color-scheme: dark)"
                srcset="https://dribia.github.io/driconfig/img/logo_dribia_blanc_cropped.png"
            >
            <source
                media="(prefers-color-scheme: light)"
                srcset="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png"
            >
            <img
                alt="driconfig"
                src="https://dribia.github.io/driconfig/img/logo_dribia_blau_cropped.png"
            >
        </picture>
    </a>
</p>

<p align="center">
    <em>A Pydantic-ish way to manage your project's YAML configurations.</em>
</p>

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                     |
|---------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Lint](https://github.com/dribia/driconfig/workflows/Lint/badge.svg?query=branch%3Amain)](https://github.com/dribia/driconfig/actions?query=workflow%3ALint) [![Tests](https://github.com/dribia/driconfig/workflows/Test/badge.svg?query=branch%3Amain)](https://github.com/dribia/driconfig/actions?query=workflow%3ATest) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/driconfig?color=%2334D058)](https://codecov.io/gh/dribia/driconfig) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) |
| Package | [![PyPI](https://img.shields.io/pypi/v/driconfig)](https://pypi.org/project/driconfig) ![PyPI - Downloads](https://img.shields.io/pypi/dm/driconfig) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/driconfig) [![GitHub](https://img.shields.io/github/license/dribia/driconfig)](LICENSE)                                                                                                                                                                                                                                              |

---

**Documentation**: <a href="https://dribia.github.io/driconfig" target="_blank">https://dribia.github.io/driconfig</a>

**Source Code**: <a href="https://github.com/dribia/driconfig" target="_blank">https://github.com/dribia/driconfig</a>

---

The usage of YAML files to store configurations and parameters is widely accepted in the Python
community, especially in Data Science environments. DriConfig provides a clean interface between your
Python code and these YAML configuration files.

It is heavily based on [Pydantic](https://pydantic-docs.helpmanual.io)'s
[Settings Management](https://pydantic-docs.helpmanual.io/usage/settings/),
preserving its core functionalities and advantages.

## Key features

* Subclassing the `DriConfig` class we create an **interface to any YAML configuration file**.
* Our project's **configurations are** then **attributes** of this class.
* They are **automatically filled** with the values in the YAML configuration file.
* We can define **complex configuration structures** using Pydantic models.
* We preserve Pydantic's **type casting and validation**!

## Installation

This project resides in the Python Package Index (PyPI), so it can easily be installed with `uv` or `pip`.

### Using uv (recommended)

[uv](https://docs.astral.sh/uv/) is a fast Python package installer and resolver.

```console
uv pip install driconfig
```

Or add it to your project:

```console
uv add driconfig
```

### Using pip

```console
pip install driconfig
```

## Usage

You can import the `DriConfig` class from the `driconfig` package and create your own configuration classes.

```python
from driconfig import DriConfig
```

### Examples

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

## Contributing

Check the [CONTRIBUTING](./CONTRIBUTING.md) site for guidelines on how to contribute to this project.

## License

DriConfig is distributed under the terms of the [MIT](https://opensource.org/license/mit) license.
Check the [LICENSE](./LICENSE) file for further details.
