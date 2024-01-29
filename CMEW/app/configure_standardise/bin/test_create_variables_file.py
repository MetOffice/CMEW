#!/usr/bin/env python
"""
Tests for configure_standardise
"""
from create_variables_file import parse_variables_from_recipe
from unittest import mock
from esmvalcore.experimental import get_recipe


def test_parse_radiation_budget_variables():
    with mock.patch(
        "create_variables_file.Recipe",
        return_value=get_recipe("recipe_radiation_budget"),
    ):
        actual = parse_variables_from_recipe("foo")
    expected = """Emon/rss
Amon/rsdt
Amon/rsut
Amon/rsutcs
Amon/rsds
Emon/rls
Amon/rlut
Amon/rlutcs
Amon/rlds
Amon/hfss
Amon/hfls"""
    assert actual == expected
