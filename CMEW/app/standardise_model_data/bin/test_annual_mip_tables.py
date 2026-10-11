#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import json
import os

ANNUAL_VARIABLES = ["tos", "sos", "thetao", "so"]

GCMODELDEV_TABLE_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "mip_tables",
    "GCModelDev",
)

# Support files, in addition to the Oyr table itself, that standalone
# mip_convert's cmor.setup() requires to be present alongside any table.
REQUIRED_GCMODELDEV_FILES = [
    "GCModelDev_CV.json",
    "GCModelDev_coordinate.json",
    "GCModelDev_grids.json",
    "GCModelDev_formula_terms.json",
    "GCModelDev_Oyr.json",
]


def test_gcmodeldev_table_dir_has_required_support_files():
    for required_file in REQUIRED_GCMODELDEV_FILES:
        assert os.path.isfile(
            os.path.join(GCMODELDEV_TABLE_DIR, required_file)
        ), "Missing required file: {}".format(required_file)


def test_gcmodeldev_oyr_table_has_annual_ocean_variables():
    with open(
        os.path.join(GCMODELDEV_TABLE_DIR, "GCModelDev_Oyr.json")
    ) as file_handle:
        oyr = json.load(file_handle)

    for var_name in ANNUAL_VARIABLES:
        assert var_name in oyr["variable_entry"]
        assert oyr["variable_entry"][var_name]["frequency"] == "yr"


def test_gcmodeldev_oyr_entries_match_omon_except_frequency():
    with open(
        os.path.join(GCMODELDEV_TABLE_DIR, "GCModelDev_Oyr.json")
    ) as file_handle:
        oyr = json.load(file_handle)

    omon_path = "/home/users/cdds/etc/mip_tables/GCModelDev/0.0.25/GCModelDev_Omon.json"
    if not os.path.isfile(omon_path):
        return  # Shared CDDS install not available in this environment.

    with open(omon_path) as file_handle:
        omon = json.load(file_handle)

    for var_name in ANNUAL_VARIABLES:
        oyr_entry = dict(oyr["variable_entry"][var_name])
        omon_entry = dict(omon["variable_entry"][var_name])
        oyr_entry.pop("frequency")
        omon_entry.pop("frequency")
        assert oyr_entry == omon_entry
