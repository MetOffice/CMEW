# (C) Crown Copyright 2024-2026, Met Office.
# The LICENSE.md file contains full licensing details.

import os
from pathlib import Path

from create_request_file import create_request, load_request_defaults


def test_create_request(monkeypatch):
    request_defaults_path = (
        Path(__file__).parent.parent / "etc" / "request_defaults.cfg"
    )
    start_year = 1993
    number_of_years = 1
    calendar = "standard"
    experiment_id = "amip"
    institution_id = "MOHC"
    model_id = "HadGEM3-GC31-HH"
    root_proc_dir = "/path/to/proc/dir/"
    root_data_dir = "/path/to/data/dir/"
    suite_id = "u-az513"
    variables_path = "/path/to/variables.txt"
    variant_label = "r1i1p1f1"
    mip_table_dir = "~cdds/etc/mip_tables/GCModelDev/0.0.25"
    stream_id = "apm"

    monkeypatch.setenv("REQUEST_DEFAULTS_PATH", str(request_defaults_path))
    monkeypatch.setenv("START_YEAR", str(start_year))
    monkeypatch.setenv("NUMBER_OF_YEARS", str(number_of_years))
    monkeypatch.setenv("CALENDAR", calendar)
    monkeypatch.setenv("EXPERIMENT_ID", experiment_id)
    monkeypatch.setenv("INSTITUTION_ID", institution_id)
    monkeypatch.setenv("MODEL_ID", model_id)
    monkeypatch.setenv("ROOT_PROC_DIR", root_proc_dir)
    monkeypatch.setenv("ROOT_DATA_DIR", root_data_dir)
    monkeypatch.setenv("SUITE_ID", suite_id)
    monkeypatch.setenv("VARIABLES_PATH", variables_path)
    monkeypatch.setenv("VARIANT_LABEL", variant_label)
    monkeypatch.setenv("MIP_TABLE_DIR", mip_table_dir)
    monkeypatch.setenv("STREAM_ID", stream_id)

    config = create_request()
    actual = {
        section: dict(config.items(section)) for section in config.sections()
    }

    request_defaults = load_request_defaults()
    expected = {}
    for section in request_defaults.sections():
        expected[section] = dict(request_defaults.items(section))

    expected["metadata"] = {
        **request_defaults["metadata"],
        "calendar": calendar,
        "experiment_id": experiment_id,
        "institution_id": institution_id,
        "model_id": model_id,
        "sub_experiment_id": suite_id.replace("-", ""),
        "variant_label": variant_label,
    }
    expected["common"] = {
        **request_defaults["common"],
        "mip_table_dir": os.path.expanduser(mip_table_dir),
        "root_proc_dir": root_proc_dir,
        "root_data_dir": root_data_dir,
        "workflow_basename": suite_id,
    }
    expected["data"] = {
        **request_defaults["data"],
        "end_date": str(start_year + number_of_years) + "-01-01T00:00:00",
        "model_workflow_id": suite_id,
        "start_date": str(start_year) + "-01-01T00:00:00",
        "streams": stream_id,
        "variable_list_file": variables_path,
    }

    assert actual == expected
