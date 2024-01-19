#!/usr/bin/env python
"""
Tests for configure_standardise
"""
from configure_standardise import extract_variables


def test_extract_variables():
    configure_standardise_path = "../mock_data/variables.txt"
    with open(configure_standardise_path) as file:
        test_variables = file.read()
    assert (
        extract_variables() == test_variables
    ), "ERROR: Incorrectly parsing recipe."
