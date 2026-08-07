#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path


def mock_data_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "mock_data"


def recipe_paths_yml_fp():
    return mock_data_dir() / "recipe_paths.yml"
