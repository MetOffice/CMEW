# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for 'update_recipe_file.py'.
"""
from update_recipe_file import (
    remove_datasets_contents,
    remove_additional_datasets,
    remove_extract_time,
    update_ocean_quadmap_model_selectors,
    construct_datasets_contents,
    add_datasets_contents,
)
from configure_for_conftest import (
    datasets,
    model_datasets,
    cmip6_datasets,
    recipe_with_datasets,
    recipe_without_datasets,
    recipe_without_additional_datasets,
)


def test_remove_datasets_contents():
    actual = remove_datasets_contents(recipe_with_datasets())
    expected = recipe_without_datasets()
    assert actual == expected


def test_remove_additional_datasets():
    actual = remove_additional_datasets(recipe_with_datasets())
    expected = recipe_without_additional_datasets()
    assert actual == expected


def test_remove_extract_time():
    recipe = {
        "preprocessors": {
            "prep_quad_map": {
                "climate_statistics": {"operator": "mean"},
                "extract_time": {
                    "start_year": 2000,
                    "end_year": 2003,
                },
                "regrid": {
                    "scheme": "nearest",
                    "target_grid": "WOA",
                },
            },
            "prep_quad_map_depth": {
                "extract_levels": {"levels": [100.0, 200.0]},
                "extract_time": {
                    "start_year": 2000,
                    "end_year": 2003,
                },
            },
        }
    }

    actual = remove_extract_time(recipe)

    expected = {
        "preprocessors": {
            "prep_quad_map": {
                "climate_statistics": {"operator": "mean"},
                "regrid": {
                    "scheme": "nearest",
                    "target_grid": "WOA",
                },
            },
            "prep_quad_map_depth": {
                "extract_levels": {"levels": [100.0, 200.0]},
            },
        }
    }

    assert actual == expected


def test_update_ocean_quadmap_model_selectors():
    recipe = {
        "diagnostics": {
            "sea_surface_salinity": {
                "scripts": {
                    "Global_Ocean_map": {
                        "control_model": {
                            "dataset": "HadGEM3-GC31-LL",
                            "ensemble": "r1i1p1f3",
                            "exp": "historical",
                            "mip": "Omon",
                            "project": "CMIP6",
                        },
                        "exper_model": {
                            "dataset": "UKESM1-0-LL",
                            "ensemble": "r1i1p1f2",
                            "exp": "historical",
                            "mip": "Omon",
                            "project": "CMIP6",
                        },
                        "script": "ocean/diagnostic_maps_quad.py",
                    }
                }
            }
        }
    }

    model_runs = {
        "u-eb014": {
            "benchmark_dataset": True,
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "test-u-eb014",
            "project": "ESMVal",
            "archive_stream": "ony",
        },
        "u-eb021": {
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "test-u-eb021",
            "project": "ESMVal",
            "archive_stream": "ony",
        },
    }

    actual = update_ocean_quadmap_model_selectors(recipe, model_runs)

    script = actual["diagnostics"]["sea_surface_salinity"]["scripts"][
        "Global_Ocean_map"
    ]

    assert script["control_model"] == {
        "dataset": "UKESM1-0-LL",
        "ensemble": "r1i1p1f1",
        "exp": "test-u-eb014",
        "mip": "Oyr",
        "project": "ESMVal",
    }
    assert script["exper_model"] == {
        "dataset": "UKESM1-0-LL",
        "ensemble": "r1i1p1f1",
        "exp": "test-u-eb021",
        "mip": "Oyr",
        "project": "ESMVal",
    }


def test_update_ocean_quadmap_model_selectors_mip_matches_monthly_route():
    # A non-annual control/experiment model must keep mip: Omon.
    recipe = {
        "diagnostics": {
            "sea_surface_salinity": {
                "scripts": {
                    "Global_Ocean_map": {
                        "control_model": {},
                        "exper_model": {},
                        "script": "ocean/diagnostic_maps_quad.py",
                    }
                }
            }
        }
    }

    model_runs = {
        "u-bv526": {
            "benchmark_dataset": True,
            "model_id": "HadGEM3-GC31-LL",
            "variant_label": "r5i1p1f3",
            "experiment_id": "historical-u-bv526",
            "project": "ESMVal",
        },
        "u-az513": {
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "historical-u-az513",
            "project": "ESMVal",
        },
    }

    actual = update_ocean_quadmap_model_selectors(recipe, model_runs)

    script = actual["diagnostics"]["sea_surface_salinity"]["scripts"][
        "Global_Ocean_map"
    ]
    assert script["control_model"]["mip"] == "Omon"
    assert script["exper_model"]["mip"] == "Omon"


def test_construct_datasets_contents():
    actual = construct_datasets_contents([model_datasets(), cmip6_datasets()])
    expected = datasets()
    assert actual == expected


def test_add_datasets_contents():
    actual = add_datasets_contents(recipe_without_datasets(), datasets())
    expected = recipe_with_datasets()
    assert actual == expected


def test_annual_source_dataset_gets_mip_oyr_override():
    model_runs = {
        "u-eb014": {
            "model_id": "UKESM1-0-LL",
            "experiment_id": "test-u-eb014",
            "project": "ESMVal",
            "start_year": 1850,
            "end_year": 1851,
            "variant_label": "r1i1p1f1",
            "archive_stream": "ony",
        },
    }

    actual = construct_datasets_contents([model_runs])

    assert actual[0]["mip"] == "Oyr"


def test_non_annual_source_dataset_has_no_mip_override():
    # Regression: existing monthly-route model runs (e.g. u-az513) must
    # not gain a "mip" key, so the recipe's default "mip: Omon" still
    # applies to them exactly as before.
    actual = construct_datasets_contents([model_datasets(), cmip6_datasets()])

    for dataset in actual:
        assert "mip" not in dataset


def test_access_cm2_cmip6_dataset_unaffected_by_annual_override():
    actual = construct_datasets_contents([cmip6_datasets()])

    assert len(actual) == 1
    assert actual[0]["dataset"] == "ACCESS-CM2"
    assert "mip" not in actual[0]


def test_annual_source_dataset_years_shifted_by_one():
    # The ony archive file for configured year N spans N-12-01 to
    # (N+1)-12-01 and is Oyr-labelled by year N+1, so the recipe period
    # for annual CMEW datasets must shift by one year.
    model_runs = {
        "u-eb014": {
            "model_id": "UKESM1-0-LL",
            "experiment_id": "test-u-eb014",
            "project": "ESMVal",
            "start_year": 1850,
            "end_year": 1859,
            "variant_label": "r1i1p1f1",
            "archive_stream": "ony",
        },
        "u-eb021": {
            "model_id": "UKESM1-0-LL",
            "experiment_id": "test-u-eb021",
            "project": "ESMVal",
            "start_year": 1850,
            "end_year": 1859,
            "variant_label": "r1i1p1f1",
            "archive_stream": "ony",
        },
    }

    actual = construct_datasets_contents([model_runs])

    for dataset_items in actual:
        assert dataset_items["start_year"] == 1851
        assert dataset_items["end_year"] == 1860
        assert dataset_items["mip"] == "Oyr"
        assert "archive_stream" not in dataset_items


def test_access_cm2_years_not_shifted():
    actual = construct_datasets_contents([cmip6_datasets()])

    assert actual[0]["dataset"] == "ACCESS-CM2"
    assert actual[0]["start_year"] == 1993
    assert actual[0]["end_year"] == 1994


def test_non_annual_cmew_dataset_years_not_shifted():
    actual = construct_datasets_contents([model_datasets()])

    for dataset_items in actual:
        assert dataset_items["start_year"] == 1993
        assert dataset_items["end_year"] == 1994
        assert "mip" not in dataset_items


def test_ocean_quadmap_model_selectors_keep_variable_level_mip():
    # The variable-level "mip: Omon" default (used by ACCESS-CM2/WOA) is
    # declared in the recipe's "variables" section, which
    # update_ocean_quadmap_model_selectors must not touch.
    recipe = {
        "diagnostics": {
            "sea_surface_salinity": {
                "variables": {
                    "sos": {"preprocessor": "prep_quad_map", "mip": "Omon"}
                },
                "scripts": {
                    "Global_Ocean_map": {
                        "control_model": {},
                        "exper_model": {},
                        "script": "ocean/diagnostic_maps_quad.py",
                    }
                },
            }
        }
    }
    model_runs = {
        "u-eb014": {
            "benchmark_dataset": True,
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "test-u-eb014",
            "project": "ESMVal",
            "archive_stream": "ony",
        },
        "u-eb021": {
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "test-u-eb021",
            "project": "ESMVal",
            "archive_stream": "ony",
        },
    }

    actual = update_ocean_quadmap_model_selectors(recipe, model_runs)

    assert (
        actual["diagnostics"]["sea_surface_salinity"]["variables"]["sos"][
            "mip"
        ]
        == "Omon"
    )
