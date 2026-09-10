#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for output_variables.py

Test data files:
/app/unittest/mock_data/original_recipe_radiation_budget.yml
    input for test_parse_variables_from_outer_key
/app/unittest/mock_data/original_recipe_zec.yml
    input for test_parse_variables_from_short_name_key
/app/unittest/kgo/radiation_budget_variables.txt
    kgo for test_write_variables
"""
from get_variables_from_recipe import parse_variables_from_recipe


def test_parse_variables_from_outer_key():
    radiation_budget_recipe = {
        "datasets": [
            {
                "activity": "ESMVal",
                "alias": "UKESM1.0 N96ORCA1",
                "dataset": "UKESM1-0-LL",
                "end_year": 1994,
                "ensemble": "r1i1p1f1",
                "exp": "historical-u-az513",
                "grid": "gn",
                "institute": "MOHC",
                "project": "ESMVal",
                "start_year": 1993,
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
        ],
        "diagnostics": {
            "seasonal_radiation_budget": {
                "description": "Seasonal radiation budget.",
                "scripts": {
                    "radiation_budget": {
                        "script": "seasonal_radiation_budget.py"
                    }
                },
                "variables": {
                    "hfls": {"mip": "Amon", "preprocessor": "seasonal"},
                    "hfss": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rlds": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rls": {"mip": "Emon", "preprocessor": "seasonal"},
                    "rlut": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rlutcs": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rsds": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rsdt": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rss": {"mip": "Emon", "preprocessor": "seasonal"},
                    "rsut": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rsutcs": {"mip": "Amon", "preprocessor": "seasonal"},
                },
            },
            "single_value_radiation_budget": {
                "description": "Radiation budget for HadGEM3 vs UKESM1.",
                "scripts": {
                    "radiation_budget": {
                        "script": "radiation_budget/radiation_budget.py"
                    }
                },
                "variables": {
                    "hfls": {"mip": "Amon", "preprocessor": "single_value"},
                    "hfss": {"mip": "Amon", "preprocessor": "single_value"},
                    "rlds": {"mip": "Amon", "preprocessor": "single_value"},
                    "rls": {"mip": "Emon", "preprocessor": "single_value"},
                    "rlut": {
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "end_year": 2010,
                                "level": "L3B",
                                "project": "obs4MIPs",
                                "start_year": 2000,
                                "tier": 1,
                            }
                        ],
                        "mip": "Amon",
                        "preprocessor": "single_value",
                    },
                    "rlutcs": {
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "end_year": 2010,
                                "level": "L3B",
                                "project": "obs4MIPs",
                                "start_year": 2000,
                                "tier": 1,
                            }
                        ],
                        "mip": "Amon",
                        "preprocessor": "single_value",
                    },
                    "rsds": {"mip": "Amon", "preprocessor": "single_value"},
                    "rsdt": {"mip": "Amon", "preprocessor": "single_value"},
                    "rss": {"mip": "Emon", "preprocessor": "single_value"},
                    "rsut": {
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "end_year": 2010,
                                "level": "L3B",
                                "project": "obs4MIPs",
                                "start_year": 2000,
                                "tier": 1,
                            }
                        ],
                        "mip": "Amon",
                        "preprocessor": "single_value",
                    },
                    "rsutcs": {
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "end_year": 2010,
                                "level": "L3B",
                                "project": "obs4MIPs",
                                "start_year": 2000,
                                "tier": 1,
                            }
                        ],
                        "mip": "Amon",
                        "preprocessor": "single_value",
                    },
                },
            },
        },
        "documentation": {
            "authors": ["lillis_jon", "hogan_emma"],
            "description": "Some summy text",
            "maintainer": ["lillis_jon", "hogan_emma"],
            "title": "Radiation Budget",
        },
        "preprocessors": {
            "seasonal": {
                "area_statistics": {"operator": "mean"},
                "climate_statistics": {
                    "operator": "mean",
                    "period": "seasonal",
                    "seasons": ["DJF", "MAM", "JJA", "SON"],
                },
            },
            "single_value": {
                "area_statistics": {"operator": "mean"},
                "climate_statistics": {"operator": "mean", "period": "full"},
            },
        },
    }
    actual = sorted(parse_variables_from_recipe(radiation_budget_recipe))
    expected = sorted(
        [
            "Emon/rss",
            "Amon/rsdt",
            "Amon/rsut",
            "Amon/rsutcs",
            "Amon/rsds",
            "Emon/rls",
            "Amon/rlut",
            "Amon/rlutcs",
            "Amon/rlds",
            "Amon/hfss",
            "Amon/hfls",
        ]
    )
    assert actual == expected


def test_parse_variables_from_short_name_key():
    mock_recipe = {
        "datasets": [
            {
                "activity": "ESMVal",
                "alias": "UKESM1.0 N96ORCA1",
                "dataset": "UKESM1-0-LL",
                "end_year": 1994,
                "ensemble": "r1i1p1f1",
                "exp": "historical-u-az513",
                "grid": "gn",
                "institute": "MOHC",
                "project": "ESMVal",
                "start_year": 1993,
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
        ],
        "diagnostics": {
            "zec": {
                "description": "Calculate ZEC for all available models.",
                "scripts": {
                    "zec": {"script": "climate_metrics/zec.py", "zec_year": 50}
                },
                "variables": {
                    "tas": {
                        "additional_datasets": [
                            {
                                "dataset": "ACCESS-ESM1-5",
                                "end_year": 267,
                                "start_year": 168,
                            },
                            {
                                "dataset": "CanESM5",
                                "end_year": 2010,
                                "ensemble": "r1i1p2f1",
                                "start_year": 1911,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 2015,
                                "ensemble": "r1i1p1f2",
                                "start_year": 1916,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 2015,
                                "ensemble": "r2i1p1f2",
                                "start_year": 1916,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 2015,
                                "ensemble": "r3i1p1f2",
                                "start_year": 1916,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 2015,
                                "ensemble": "r4i1p1f2",
                                "start_year": 1916,
                            },
                            {
                                "dataset": "MPI-ESM1-2-LR",
                                "end_year": 2014,
                                "start_year": 1915,
                            },
                            {
                                "dataset": "CESM2",
                                "end_year": 167,
                                "start_year": 68,
                            },
                        ],
                        "ensemble": "r1i1p1f1",
                        "exp": "esm-1pct-brch-1000PgC",
                        "grid": "gn",
                        "mip": "Amon",
                        "preprocessor": "spatial_mean",
                        "project": "CMIP6",
                        "short_name": "tas",
                    },
                    "tas_base": {
                        "additional_datasets": [
                            {
                                "dataset": "ACCESS-ESM1-5",
                                "end_year": 177,
                                "start_year": 158,
                            },
                            {
                                "dataset": "CanESM5",
                                "end_year": 1920,
                                "ensemble": "r1i1p2f1",
                                "start_year": 1901,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 1925,
                                "ensemble": "r1i1p1f2",
                                "start_year": 1906,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 1925,
                                "ensemble": "r2i1p1f2",
                                "start_year": 1906,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 1925,
                                "ensemble": "r3i1p1f2",
                                "start_year": 1906,
                            },
                            {
                                "dataset": "UKESM1-0-LL",
                                "end_year": 1925,
                                "ensemble": "r4i1p1f2",
                                "start_year": 1906,
                            },
                            {
                                "dataset": "MPI-ESM1-2-LR",
                                "end_year": 1924,
                                "start_year": 1905,
                            },
                            {
                                "dataset": "CESM2",
                                "end_year": 77,
                                "start_year": 58,
                            },
                        ],
                        "ensemble": "r1i1p1f1",
                        "exp": "1pctCO2",
                        "grid": "gn",
                        "mip": "Amon",
                        "preprocessor": "anomaly_base",
                        "project": "CMIP6",
                        "short_name": "tas",
                    },
                },
            }
        },
        "documentation": {
            "authors": ["gier_bettina"],
            "description": "Calculate ZEC temperature.\n",
            "domains": ["global"],
            "maintainer": ["gier_bettina"],
            "realms": ["atmos"],
            "references": ["macdougall20"],
            "title": "Zero Emission Commitment (ZEC)\n",
        },
        "preprocessors": {
            "anomaly_base": {
                "area_statistics": {"operator": "mean"},
                "climate_statistics": {"operator": "mean", "period": "full"},
            },
            "spatial_mean": {
                "annual_statistics": {"operator": "mean"},
                "area_statistics": {"operator": "mean"},
            },
        },
    }
    actual = parse_variables_from_recipe(mock_recipe)
    expected = ["Amon/tas"]
    assert actual == expected
