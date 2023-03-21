#!/usr/bin/env bash

set -e
set -x

poetry run black driconfig tests --check
poetry run ruff driconfig tests
poetry run mypy driconfig
