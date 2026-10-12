# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""Tests for the CMEW preflight command."""

import runpy
from pathlib import Path

import pytest


SCRIPT_PATH = Path(__file__).with_name("cmew-preflight")
PREFLIGHT = runpy.run_path(str(SCRIPT_PATH))

build_preflight = PREFLIGHT["build_preflight"]


def write_config(
    tmp_path,
    *,
    archive_stream=None,
    start_year=1850,
    number_of_years=10,
):
    """Write a minimal Rose configuration for preflight testing."""
    archive_line = ""
    if archive_stream is not None:
        archive_line = f'archive_stream="{archive_stream}"\n'

    config = tmp_path / "rose-suite.conf"
    config.write_text(
        "[namelist:model_runs(1)]\n"
        f"{archive_line}"
        'calendar="gregorian"\n'
        'experiment_id="test"\n'
        'label_for_plots="experiment"\n'
        'model_id="UKESM1-0-LL"\n'
        'suite_id="u-test001"\n'
        'variant_label="r1i1p1f1"\n'
        "\n"
        "[template variables]\n"
        f"NUMBER_OF_YEARS={number_of_years}\n"
        f"START_YEAR={start_year}\n"
    )
    return config


def test_annual_ony_uses_oyr_and_shifts_effective_years(tmp_path):
    """Annual ony data should follow the Oyr route with a +1 year shift."""
    config = write_config(tmp_path, archive_stream="ony")

    plan = build_preflight(config)

    assert plan["requested_start"] == 1850
    assert plan["requested_end"] == 1859

    dataset = plan["datasets"][0]

    assert dataset["suite_id"] == "u-test001"
    assert dataset["archive_stream"] == "ony"
    assert dataset["frequency"] == "annual"
    assert dataset["route"] == "annual standardisation"
    assert dataset["mip"] == "Oyr"
    assert dataset["effective_start"] == 1851
    assert dataset["effective_end"] == 1860


def test_missing_archive_stream_defaults_to_monthly_without_year_shift(
    tmp_path,
):
    """Missing archive_stream should preserve the existing onm default."""
    config = write_config(tmp_path)

    plan = build_preflight(config)

    assert plan["requested_start"] == 1850
    assert plan["requested_end"] == 1859

    dataset = plan["datasets"][0]

    assert dataset["suite_id"] == "u-test001"
    assert dataset["archive_stream"] == "onm"
    assert dataset["frequency"] == "monthly"
    assert dataset["route"] == "monthly standardisation"
    assert dataset["mip"] == "Omon"
    assert dataset["effective_start"] == 1850
    assert dataset["effective_end"] == 1859


@pytest.mark.parametrize("number_of_years", [0, -1])
def test_number_of_years_must_be_positive(tmp_path, number_of_years):
    """Preflight should reject zero or negative assessment lengths."""
    config = write_config(
        tmp_path,
        number_of_years=number_of_years,
    )

    with pytest.raises(ValueError, match="NUMBER_OF_YEARS must be at least 1"):
        build_preflight(config)


def test_mixed_streams_are_routed_independently(tmp_path):
    """Each model run should use its own archive-stream route."""
    config = tmp_path / "rose-suite.conf"
    config.write_text(
        "[namelist:model_runs(1)]\n"
        'archive_stream="ony"\n'
        'label_for_plots="annual-model"\n'
        'model_id="UKESM1-0-LL"\n'
        'suite_id="u-annual"\n'
        "\n"
        "[namelist:model_runs(reference)]\n"
        'archive_stream="onm"\n'
        'label_for_plots="monthly-model"\n'
        'model_id="UKESM1-0-LL"\n'
        'suite_id="u-monthly"\n'
        "\n"
        "[template variables]\n"
        "NUMBER_OF_YEARS=10\n"
        "START_YEAR=1850\n"
    )

    plan = build_preflight(config)

    datasets = {dataset["suite_id"]: dataset for dataset in plan["datasets"]}

    annual = datasets["u-annual"]
    assert annual["archive_stream"] == "ony"
    assert annual["route"] == "annual standardisation"
    assert annual["mip"] == "Oyr"
    assert annual["effective_start"] == 1851
    assert annual["effective_end"] == 1860

    monthly = datasets["u-monthly"]
    assert monthly["archive_stream"] == "onm"
    assert monthly["route"] == "monthly standardisation"
    assert monthly["mip"] == "Omon"
    assert monthly["effective_start"] == 1850
    assert monthly["effective_end"] == 1859


def test_dataset_roles_are_identified_from_model_run_sections(tmp_path):
    """Preflight should label experiment and reference datasets correctly."""
    config = tmp_path / "rose-suite.conf"
    config.write_text(
        "[namelist:model_runs(1)]\n"
        'archive_stream="ony"\n'
        'label_for_plots="experiment-model"\n'
        'model_id="UKESM1-0-LL"\n'
        'suite_id="u-experiment"\n'
        "\n"
        "[namelist:model_runs(reference)]\n"
        'archive_stream="ony"\n'
        'label_for_plots="reference-model"\n'
        'model_id="UKESM1-0-LL"\n'
        'suite_id="u-reference"\n'
        "\n"
        "[template variables]\n"
        "NUMBER_OF_YEARS=2\n"
        "START_YEAR=1850\n"
    )

    plan = build_preflight(config)

    datasets = {dataset["suite_id"]: dataset for dataset in plan["datasets"]}

    assert datasets["u-experiment"]["role"] == "experiment"
    assert datasets["u-reference"]["role"] == "reference"


def test_recipe_variables_returns_unique_short_names_and_mips():
    """Recipe requirements should expose unique short-name/MIP pairs."""
    recipe_content = {
        "diagnostics": {
            "surface_temperature": {
                "variables": {
                    "tos": {
                        "mip": "Omon",
                    }
                }
            },
            "surface_salinity": {
                "variables": {
                    "salinity": {
                        "short_name": "sos",
                        "mip": "Omon",
                    }
                }
            },
            "duplicate_temperature": {
                "variables": {
                    "tos": {
                        "mip": "Omon",
                    }
                }
            },
        }
    }

    variables = PREFLIGHT["recipe_variables"](recipe_content)

    assert variables == [
        {
            "short_name": "tos",
            "mip": "Omon",
        },
        {
            "short_name": "sos",
            "mip": "Omon",
        },
    ]


def test_preflight_plan_can_include_recipe_information(tmp_path):
    """Recipe metadata should be carried into the preflight plan."""
    config = write_config(tmp_path, archive_stream="ony")

    variables = [
        {
            "short_name": "tos",
            "mip": "Omon",
        },
        {
            "short_name": "sos",
            "mip": "Omon",
        },
    ]

    plan = build_preflight(
        config,
        recipe="ocean_quadmap",
        recipe_variables=variables,
    )

    assert plan["recipe"] == "ocean_quadmap"
    assert plan["recipe_variables"] == variables


def test_preflight_output_shows_recipe_variables(tmp_path, capsys):
    """Human-readable output should show recipe requirements."""
    config = write_config(tmp_path, archive_stream="ony")

    plan = build_preflight(
        config,
        recipe="ocean_quadmap",
        recipe_variables=[
            {
                "short_name": "tos",
                "mip": "Omon",
            },
            {
                "short_name": "sos",
                "mip": "Omon",
            },
        ],
    )

    PREFLIGHT["print_preflight"](plan)

    output = capsys.readouterr().out

    assert "Recipe: ocean_quadmap" in output
    assert "Required recipe variables:" in output
    assert "tos (Omon)" in output
    assert "sos (Omon)" in output
    assert "output MIP table: Oyr" in output
