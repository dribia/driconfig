#!/usr/bin/env bash

set -e
set -x

mypy driconfig
flake8 driconfig tests
black driconfig tests --check
isort driconfig tests --check-only
pydocstyle driconfig
