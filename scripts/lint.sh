#!/usr/bin/env bash

set -e
set -x

poetry run mypy driconfig
poetry run flake8 driconfig tests
poetry run black driconfig tests --check
poetry run isort driconfig tests --check-only
poetry run pydocstyle driconfig
