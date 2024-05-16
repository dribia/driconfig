#!/usr/bin/env bash

set -e
set -x

poetry run ruff format driconfig tests --check
poetry run ruff check driconfig tests
poetry run mypy driconfig
