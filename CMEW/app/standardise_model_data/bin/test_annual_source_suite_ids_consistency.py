#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Checks that annual/monthly routing is driven by the
"standardisation_frequency" facet in rose-suite.conf, rather than a
hard-coded suite-id list duplicated across CMEW apps.
"""
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]


def test_annual_source_suite_ids_constant_removed():
    # The old duplicated constant must no longer exist anywhere.
    for relative_path in (
        "app/configure_standardise/bin/config_configure_standardise.py",
        "app/configure_for/bin/update_recipe_file.py",
        "flow.cylc",
    ):
        contents = (REPO_ROOT / relative_path).read_text()
        assert "ANNUAL_SOURCE_SUITE_IDS" not in contents


def test_rose_suite_conf_marks_annual_model_runs_with_frequency():
    contents = (REPO_ROOT / "rose-suite.conf").read_text()

    for suite_id in ("u-eb014", "u-eb021"):
        section_start = contents.index('suite_id="{}"'.format(suite_id))
        section_text = contents[
            max(0, section_start - 300) : section_start  # noqa: E203
        ]
        assert 'archive_stream="onm"' in section_text
        assert 'standardisation_frequency="annual"' in section_text


def test_update_recipe_file_uses_standardisation_frequency_facet():
    contents = (
        REPO_ROOT / "app" / "configure_for" / "bin" / "update_recipe_file.py"
    ).read_text()

    assert "standardisation_frequency" in contents
    assert "is_annual_source" in contents


def test_flow_cylc_uses_facet_per_dataset_not_hardcoded_ids():
    contents = (REPO_ROOT / "flow.cylc").read_text()

    assert "facet_per_dataset" in contents
    assert "standardisation_frequency" in contents
