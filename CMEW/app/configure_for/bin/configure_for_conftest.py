#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
from pathlib import Path


def datasets():
    return [
        {
            "activity": "ESMVal",
            "end_year": 1994,
            "exp": "historical-u-az513",
            "grid": "gn",
            "institute": "MOHC",
            "alias": "UKESM1.0 N96ORCA1",
            "dataset": "UKESM1-0-LL",
            "project": "ESMVal",
            "start_year": 1993,
            "ensemble": "r1i1p1f1",
        },
        {
            "activity": "ESMVal",
            "alias": "HadGEM3-GC3.1 N96ORCA1",
            "benchmark_dataset": True,
            "dataset": "HadGEM3-GC31-LL",
            "end_year": 1994,
            "ensemble": "r5i1p1f3",
            "exp": "historical-u-bv526",
            "grid": "gn",
            "institute": "MOHC",
            "project": "ESMVal",
            "start_year": 1993,
        },
        {
            "activity": "ESMVal",
            "alias": "HadGEM3-GC5E-LL N96ORCA1",
            "dataset": "HadGEM3-GC5E-LL",
            "end_year": 1994,
            "ensemble": "r1i1p1f1",
            "exp": "amip-u-cw673",
            "grid": "gn",
            "institute": "MOHC",
            "project": "ESMVal",
            "start_year": 1993,
        },
        {
            "alias": "CMIP6_ACCESS-CM2",
            "dataset": "ACCESS-CM2",
            "end_year": 1994,
            "ensemble": "r1i1p1f1",
            "exp": "historical",
            "grid": "gn",
            "institute": "CSIRO-ARCCSS",
            "project": "CMIP6",
            "start_year": 1993,
        },
    ]


def model_datasets():
    return {
        "u-az513": {
            "activity": "ESMVal",
            "calendar": "360_day",
            "end_year": 1994,
            "experiment_id": "historical-u-az513",
            "grid": "gn",
            "institute": "MOHC",
            "label_for_plots": "UKESM1.0 N96ORCA1",
            "model_id": "UKESM1-0-LL",
            "project": "ESMVal",
            "start_year": 1993,
            "suite_id": "u-az513",
            "variant_label": "r1i1p1f1",
        },
        "u-bv526": {
            "activity": "ESMVal",
            "benchmark_dataset": True,
            "calendar": "360_day",
            "end_year": 1994,
            "experiment_id": "historical-u-bv526",
            "grid": "gn",
            "institute": "MOHC",
            "label_for_plots": "HadGEM3-GC3.1 N96ORCA1",
            "model_id": "HadGEM3-GC31-LL",
            "project": "ESMVal",
            "start_year": 1993,
            "suite_id": "u-bv526",
            "variant_label": "r5i1p1f3",
        },
        "u-cw673": {
            "activity": "ESMVal",
            "calendar": "gregorian",
            "end_year": 1994,
            "experiment_id": "amip-u-cw673",
            "grid": "gn",
            "institute": "MOHC",
            "label_for_plots": "HadGEM3-GC5E-LL N96ORCA1",
            "model_id": "HadGEM3-GC5E-LL",
            "project": "ESMVal",
            "start_year": 1993,
            "suite_id": "u-cw673",
            "variant_label": "r1i1p1f1",
        },
    }


def cmip6_datasets():
    return {
        "ACCESS-CM2": {
            "end_year": 1994,
            "experiment_id": "historical",
            "grid": "gn",
            "institute": "CSIRO-ARCCSS",
            "label_for_plots": "CMIP6_ACCESS-CM2",
            "model_id": "ACCESS-CM2",
            "project": "CMIP6",
            "start_year": 1993,
            "variant_label": "r1i1p1f1",
        },
    }


def recipe_with_datasets():
    return {
        "documentation": {"key1": "value1", "key2": "value2"},
        "datasets": datasets(),
        "preprocessors": {"key3": "value3"},
        "diagnostics": {
            "my_diagnostic_name": {
                "variables": {
                    "my_variable": {"additional_datasets": ["value4"]},
                },
            },
        },
    }


def recipe_without_datasets():
    return {
        "documentation": {"key1": "value1", "key2": "value2"},
        "datasets": [],
        "preprocessors": {"key3": "value3"},
        "diagnostics": {
            "my_diagnostic_name": {
                "variables": {
                    "my_variable": {"additional_datasets": ["value4"]},
                },
            },
        },
    }


def recipe_without_additional_datasets():
    return {
        "documentation": {"key1": "value1", "key2": "value2"},
        "datasets": datasets(),
        "preprocessors": {"key3": "value3"},
        "diagnostics": {
            "my_diagnostic_name": {
                "variables": {
                    "my_variable": {},
                },
            },
        },
    }


def mock_data_dir():
    return Path(__file__).parent.parent.parent / "unittest" / "mock_data"


def model_runs_yml_fp():
    return mock_data_dir() / "model_runs.yml"


def original_recipe_radiation_budget_fp():
    return mock_data_dir() / "original_recipe_radiation_budget.yml"
