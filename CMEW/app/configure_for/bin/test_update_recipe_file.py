#!/usr/bin/env python
# (C) British Crown Copyright 2024, Met Office.
# Please see LICENSE for license details.
from update_recipe_file import update_recipe
from pathlib import Path


def test_create_recipe_file():
    # Arrange
    expected = {
        "documentation": {
            "title": "Radiation Budget",
            "description": "This diagnostic analyses the radiation budget by separating top-of-atmosphere fluxes into clear-sky and cloud forcing components, and surface fluxes into downwelling and upwelling components. Model predictions are compared against three observational estimates, one of which (Stephens et al. 2012) includes uncertainty estimates. When the black error bars overlap the zero line, the model is consistent with observations according to Stephens et al. (2012).",  # noqa: E501
            "authors": ["lillis_jon", "hogan_emma"],
            "maintainer": ["lillis_jon", "hogan_emma"],
        },
        "datasets": [
            {
                "dataset": "HadGEM3-GC31-LL",
                "project": "CMIP6",
                "exp": "historical",
                "ensemble": "r1i1p1f3",
                "grid": "gn",
                "start_year": 1993,
                "end_year": 1993,
            },
            {
                "dataset": "UKESM1-0-LL",
                "project": "ESMVal",
                "exp": "amip",
                "activity": "ESMVal",
                "ensemble": "r1i1p1f1",
                "grid": "gn",
                "start_year": 1993,
                "end_year": 1993,
            },
        ],
        "preprocessors": {
            "single_value": {
                "climate_statistics": {"operator": "mean", "period": "full"},
                "area_statistics": {"operator": "mean"},
            },
            "seasonal": {
                "climate_statistics": {
                    "operator": "mean",
                    "period": "seasonal",
                    "seasons": ["DJF", "MAM", "JJA", "SON"],
                },
                "area_statistics": {"operator": "mean"},
            },
        },
        "diagnostics": {
            "single_value_radiation_budget": {
                "description": "Radiation budget for HadGEM3 vs UKESM1.",
                "variables": {
                    "rss": {"mip": "Emon", "preprocessor": "single_value"},
                    "rsdt": {"mip": "Amon", "preprocessor": "single_value"},
                    "rsut": {
                        "mip": "Amon",
                        "preprocessor": "single_value",
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "project": "obs4mips",
                                "level": "L3B",
                                "version": "Ed2-7",
                                "start_year": 2000,
                                "end_year": 2010,
                                "tier": 1,
                            }
                        ],
                    },
                    "rsutcs": {
                        "mip": "Amon",
                        "preprocessor": "single_value",
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "project": "obs4mips",
                                "level": "L3B",
                                "version": "Ed2-7",
                                "start_year": 2000,
                                "end_year": 2010,
                                "tier": 1,
                            }
                        ],
                    },
                    "rsds": {"mip": "Amon", "preprocessor": "single_value"},
                    "rls": {"mip": "Emon", "preprocessor": "single_value"},
                    "rlut": {
                        "mip": "Amon",
                        "preprocessor": "single_value",
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "project": "obs4mips",
                                "level": "L3B",
                                "version": "Ed2-7",
                                "start_year": 2000,
                                "end_year": 2010,
                                "tier": 1,
                            }
                        ],
                    },
                    "rlutcs": {
                        "mip": "Amon",
                        "preprocessor": "single_value",
                        "additional_datasets": [
                            {
                                "dataset": "CERES-EBAF",
                                "project": "obs4mips",
                                "level": "L3B",
                                "version": "Ed2-7",
                                "start_year": 2000,
                                "end_year": 2010,
                                "tier": 1,
                            }
                        ],
                    },
                    "rlds": {"mip": "Amon", "preprocessor": "single_value"},
                    "hfss": {"mip": "Amon", "preprocessor": "single_value"},
                    "hfls": {"mip": "Amon", "preprocessor": "single_value"},
                },
                "scripts": {
                    "radiation_budget": {
                        "script": "radiation_budget/radiation_budget.py"
                    }
                },
            },
            "seasonal_radiation_budget": {
                "description": "Seasonal radiation budget for HadGEM3 vs UKESM1.",  # noqa: E501
                "variables": {
                    "rss": {"mip": "Emon", "preprocessor": "seasonal"},
                    "rsdt": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rsut": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rsutcs": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rsds": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rls": {"mip": "Emon", "preprocessor": "seasonal"},
                    "rlut": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rlutcs": {"mip": "Amon", "preprocessor": "seasonal"},
                    "rlds": {"mip": "Amon", "preprocessor": "seasonal"},
                    "hfss": {"mip": "Amon", "preprocessor": "seasonal"},
                    "hfls": {"mip": "Amon", "preprocessor": "seasonal"},
                },
                "scripts": {
                    "radiation_budget": {
                        "script": "radiation_budget/seasonal_radiation_budget.py"  # noqa: E501
                    }
                },
            },
        },
    }

    # Act
    # TODO: Copied from `configure_standardise/bin/test_create_variables.py`
    #       Need to update for the location of this file itself.
    recipe_path = (
        Path(__file__).parent.parent / "mock_data" / "test_recipe.yml"
    )
    actual = update_recipe(recipe_path)

    # Assert
    assert actual == expected
