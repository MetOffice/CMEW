#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Regression checks on the annual standardisation Cylc task wiring, to
ensure the opt-in annual route stays workflow-local and consistent with
the monthly route's dataset selection.
"""
import os
import re

import jinja2

REPO_ROOT = os.path.dirname(
    os.path.dirname(
        os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    )
)

ANNUAL_ROSE_APP_CONF = os.path.join(
    REPO_ROOT, "app", "standardise_model_data_annual", "rose-app.conf"
)
FLOW_CYLC = os.path.join(REPO_ROOT, "flow.cylc")


def _env_var_value(contents, var_name):
    match = re.search(
        r"--{}\s+\"?(\S+?)\"?\s*(\\\n|$)".format(re.escape(var_name)),
        contents,
    )
    assert match, "Could not find --{} in rose-app.conf".format(var_name)
    return match.group(1)


def _render_dataset_partitioning(datasets_string, archive_streams):
    """
    Render flow.cylc's dataset-partitioning Jinja loop standalone
    (extracted by marker comments), given fake list_datasets()/
    facet_per_dataset() values, and return (monthly_datasets,
    annual_datasets) as lists.
    """
    with open(FLOW_CYLC) as file_handle:
        contents = file_handle.read()

    start_marker = (
        "{# list_datasets() returns a comma-separated string, "
        "not a list. #}"
    )
    end_marker = "{%- endfor %}"
    start = contents.index(start_marker)
    end = contents.index(end_marker, start) + len(end_marker)
    snippet = contents[start:end]
    snippet += (
        "\n{{ monthly_datasets | join(',') }}|"
        "{{ annual_datasets | join(',') }}"
    )

    rendered = jinja2.Template(snippet).render(
        datasets=datasets_string, archive_streams=archive_streams
    )
    monthly_part, annual_part = rendered.strip().split("|")
    monthly = [d for d in monthly_part.split(",") if d]
    annual = [d for d in annual_part.split(",") if d]
    return monthly, annual


def test_annual_rose_app_conf_uses_workflow_local_paths_not_tmp():
    with open(ANNUAL_ROSE_APP_CONF) as file_handle:
        contents = file_handle.read()

    assert "/tmp" not in contents
    for required_var in (
        "${ROOT_DATA_DIR}",
        "${CYLC_WORKFLOW_SHARE_DIR}",
        "${CYLC_WORKFLOW_RUN_DIR}",
    ):
        assert required_var in contents


def test_annual_rose_app_conf_does_not_invoke_cdds_entry_points():
    with open(ANNUAL_ROSE_APP_CONF) as file_handle:
        lines = file_handle.readlines()

    # Only check non-comment lines: the file's header comment explains,
    # in prose, what this app deliberately does NOT invoke.
    command_lines = "\n".join(
        line for line in lines if not line.strip().startswith("#")
    )

    assert "cdds_extract" not in command_lines
    assert "cdds_convert" not in command_lines
    assert "run_mip_convert" not in command_lines
    assert "standardise_ony_annual.py" in command_lines


def test_annual_retrieval_dir_matches_model_output_dir_relationship():
    # Proves mip_convert's required <model_output_dir>/<suite_id>/ony/
    # layout cannot regress: retrieval-dir must equal
    # model-output-dir/${CYLC_TASK_PARAM_annual_dataset}/ony.
    with open(ANNUAL_ROSE_APP_CONF) as file_handle:
        contents = file_handle.read()

    retrieval_dir = _env_var_value(contents, "retrieval-dir")
    model_output_dir = _env_var_value(contents, "model-output-dir")

    assert (
        retrieval_dir
        == model_output_dir + "/${CYLC_TASK_PARAM_annual_dataset}/ony"
    )


def test_flow_cylc_annual_dataset_param_only_for_opt_in_graph_block():
    with open(FLOW_CYLC) as file_handle:
        contents = file_handle.read()

    # The annual task must only appear inside the existing conditional
    # block that also guards the monthly cdds_convert route, so it is
    # never added for UNITTEST or SKIP_CDDS runs.
    match = re.search(
        r"\{%-?\s*if annual_datasets\s*%\}(.*?)\{%-?\s*endif\s*%\}",
        contents,
        re.DOTALL,
    )
    assert match, "Could not find the annual_datasets conditional block"
    assert "standardise_model_data_annual" in contents


def test_u_eb014_is_annual_only():
    monthly, annual = _render_dataset_partitioning(
        "u-eb014", {"u-eb014": "ony"}
    )
    assert monthly == []
    assert annual == ["u-eb014"]


def test_u_eb021_is_annual_only():
    monthly, annual = _render_dataset_partitioning(
        "u-eb021", {"u-eb021": "ony"}
    )
    assert monthly == []
    assert annual == ["u-eb021"]


def test_non_annual_dataset_remains_monthly_only():
    monthly, annual = _render_dataset_partitioning(
        "u-az513", {"u-az513": "onm"}
    )
    assert monthly == ["u-az513"]
    assert annual == []


def test_monthly_and_annual_datasets_are_disjoint():
    monthly, annual = _render_dataset_partitioning(
        "u-az513, u-eb014, u-eb021, u-bv526",
        {
            "u-az513": "onm",
            "u-eb014": "ony",
            "u-eb021": "ony",
            "u-bv526": "onm",
        },
    )
    assert set(monthly) == {"u-az513", "u-bv526"}
    assert set(annual) == {"u-eb014", "u-eb021"}
    assert set(monthly).isdisjoint(set(annual))
    # No dataset should be standardised by both routes.
    assert set(monthly) | set(annual) == {
        "u-az513",
        "u-eb014",
        "u-eb021",
        "u-bv526",
    }


def test_dataset_missing_archive_stream_facet_defaults_to_monthly():
    # A dataset with no archive_stream facet at all (the common case for
    # non-annual runs) must default to the monthly route.
    monthly, annual = _render_dataset_partitioning("u-az513", {})
    assert monthly == ["u-az513"]
    assert annual == []


def test_restructure_dirs_depends_on_both_selected_standardisation_paths():
    with open(FLOW_CYLC) as file_handle:
        contents = file_handle.read()

    # restructure_dirs must be triggered by the monthly chain (when
    # monthly_datasets is non-empty) and by the annual chain (when
    # annual_datasets is non-empty), so it waits for whichever paths are
    # actually selected before running.
    assert "=> standardise_model_data<dataset> => restructure_dirs" in contents
    assert (
        "standardise_model_data_annual<annual_dataset>\n"
        "                => restructure_dirs" in contents
    )
