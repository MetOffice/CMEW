# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for 'update_recipe_file.py'.
"""
from cmewpy.update_esmvaltool_recipe.update_recipe_file import (
    remove_datasets_contents,
    remove_additional_datasets,
    update_ocean_quadmap_model_selectors,
    construct_datasets_contents,
    add_datasets_contents,
)


def test_remove_datasets_contents(
    recipe_with_datasets, recipe_without_datasets
):
    actual = remove_datasets_contents(recipe_with_datasets)
    expected = recipe_without_datasets
    assert actual == expected


def test_remove_additional_datasets(
    recipe_with_datasets, recipe_without_additional_datasets
):
    actual = remove_additional_datasets(recipe_with_datasets)
    expected = recipe_without_additional_datasets
    assert actual == expected


def test_construct_datasets_contents(model_datasets, cmip6_datasets, datasets):
    actual = construct_datasets_contents([model_datasets, cmip6_datasets])
    expected = datasets
    assert actual == expected


def test_add_datasets_contents(
    recipe_without_datasets, datasets, recipe_with_datasets
):
    actual = add_datasets_contents(recipe_without_datasets, datasets)
    expected = recipe_with_datasets
    assert actual == expected



def test_update_ocean_quadmap_model_selectors():
    recipe = {
        "diagnostics": {
            "sea_surface_temperature": {
                "scripts": {
                    "Global_Ocean_map": {
                        "script": "ocean/diagnostic_maps_quad.py",
                        "control_model": {
                            "dataset": "HadGEM3-GC31-LL",
                            "project": "CMIP6",
                        },
                        "exper_model": {
                            "dataset": "UKESM1-0-LL",
                            "project": "CMIP6",
                        },
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
            "experiment_id": "development-u-eb014",
            "project": "ESMVal",
        },
        "u-eb021": {
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "development-u-eb021",
            "project": "ESMVal",
        },
    }

    actual = update_ocean_quadmap_model_selectors(recipe, model_runs)

    script = actual["diagnostics"]["sea_surface_temperature"]["scripts"][
        "Global_Ocean_map"
    ]

    assert script["control_model"] == {
        "dataset": "UKESM1-0-LL",
        "ensemble": "r1i1p1f1",
        "exp": "development-u-eb014",
        "mip": "Omon",
        "project": "ESMVal",
    }

    assert script["exper_model"] == {
        "dataset": "UKESM1-0-LL",
        "ensemble": "r1i1p1f1",
        "exp": "development-u-eb021",
        "mip": "Omon",
        "project": "ESMVal",
    }


def test_update_ocean_quadmap_model_selectors_ignores_other_scripts():
    recipe = {
        "diagnostics": {
            "other_diagnostic": {
                "scripts": {
                    "other_script": {
                        "script": "some/other_diagnostic.py",
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
            "experiment_id": "development-u-eb014",
            "project": "ESMVal",
        },
        "u-eb021": {
            "model_id": "UKESM1-0-LL",
            "variant_label": "r1i1p1f1",
            "experiment_id": "development-u-eb021",
            "project": "ESMVal",
        },
    }

    expected = {
        "diagnostics": {
            "other_diagnostic": {
                "scripts": {
                    "other_script": {
                        "script": "some/other_diagnostic.py",
                    }
                }
            }
        }
    }

    actual = update_ocean_quadmap_model_selectors(recipe, model_runs)

    assert actual == expected
