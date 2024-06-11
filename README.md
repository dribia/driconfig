# DriConfig

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

<p style="text-align: center">
<a href="https://github.com/dribia/driconfig/actions?query=workflow%3ATest" target="_blank">
    <img src="https://github.com/dribia/driconfig/workflows/Test/badge.svg?query=branch%3Amain" alt="Test">
</a>
<a href="https://github.com/dribia/driconfig/actions?query=workflow%3ALint" target="_blank">
    <img src="https://github.com/dribia/driconfig/workflows/Lint/badge.svg?query=branch%3Amain" alt="Lint">
</a>
<a href="https://github.com/dribia/driconfig/actions?query=workflow%3APublish" target="_blank">
    <img src="https://github.com/dribia/driconfig/workflows/Publish/badge.svg?query=branch%3Amain" alt="Publish">
</a>
<a href="https://github.com/dribia/driconfig/actions?query=workflow%3ADocs" target="_blank">
    <img src="https://github.com/dribia/driconfig/workflows/Docs/badge.svg?query=branch%3Amain" alt="Docs">
</a>
<a href="https://codecov.io/gh/dribia/driconfig" target="_blank">
    <img src="https://img.shields.io/codecov/c/github/dribia/driconfig?color=%2334D058" alt="Coverage">
</a>
<a href="https://pypi.org/project/driconfig" target="_blank">
    <img src="https://img.shields.io/pypi/v/driconfig?color=%2334D058&label=pypi%20package" alt="PyPI version">
</a>
<a href="https://pypistats.org/packages/driconfig" target="_blank">
    <img src="https://img.shields.io/pypi/dm/driconfig?color=%2334D058" alt="PyPI downloads">
</a>
</p>

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
