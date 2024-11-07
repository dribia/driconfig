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

|         |                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         |
|---------|-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| CI/CD   | [![Tests](https://github.com/dribia/driconfig/workflows/Test/badge.svg?query=branch%3Amain)](https://github.com/dribia/driconfig/actions?query=workflow%3ATest) [![Coverage Status](https://img.shields.io/codecov/c/github/dribia/driconfig?color=%2334D058)](https://codecov.io/gh/dribia/driconfig) [![Tests](https://github.com/dribia/driconfig/workflows/Lint/badge.svg?query=branch%3Amain)](https://github.com/dribia/driconfig/actions?query=workflow%3ALint) [![types - Mypy](https://img.shields.io/badge/types-Mypy-blue.svg)](https://github.com/python/mypy) [![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) |
| Package | [![PyPI](https://img.shields.io/pypi/v/driconfig)](https://pypi.org/project/driconfig) ![PyPI - Downloads](https://img.shields.io/pypi/dm/driconfig?color=blue&logo=pypi&logoColor=gold) ![PyPI - Python Version](https://img.shields.io/pypi/pyversions/driconfig?logo=python&logoColor=gold) [![GitHub](https://img.shields.io/github/license/dribia/driconfig?color=blue)](LICENSE)                                                                                                                                                                                                                                                                                                                                                  |
---

**Documentation**: <a href="https://dribia.github.io/driconfig" target="_blank">https://dribia.github.io/driconfig</a>

**Source Code**: <a href="https://github.com/dribia/driconfig" target="_blank">https://github.com/dribia/driconfig</a>

---

The usage of YAML files to store configurations and parameters is widely accepted in the Python
community, especially in Data Science environments. DriConfig provides a clean interface between your Python code and these YAML configuration files.

## Installation

This project resides in the Python Package Index (PyPI), so it can easily be installed with `pip`:

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

[Poetry](https://python-poetry.org) is the best way to interact with this project. To install it,
follow the official [Poetry installation guide](https://python-poetry.org/docs/#installation).

With `poetry` installed, one can install the project dependencies with:

```shell
poetry install
```

Then, to run the project unit tests:

```shell
make test
```

To run the linters (`ruff` and `mypy`):

```shell
make lint
```

## License

`driconfig` is distributed under the terms of the
[MIT](https://opensource.org/license/mit) license.
Check the [LICENSE](./LICENSE) file for further details.
