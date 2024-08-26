#!/usr/bin/env bash

set -e
set -x

mypy app tests
ruff check app tests
ruff format app tests --check