#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.

# Information on which streams contain variables from different MIP tables.
streams_dict = {
    "apm": [
        "Amon/tas",
        "Amon/pr",
        "Amon/ps",
        "Amon/rtmt",
        "Amon/rsut",
        "Amon/rlut",
        "Amon/vas",
        "Amon/evspsbl",
        "Amon/psl",
        "AERmon/od550aer",
        "AERmon/cdnc",
        "AERmon/ch4",
        "Amon/clw",
        "Amon/clt",
        "Amon/hfls",
        "Amon/hfss",
        "Amon/rlds",
        "Emon/rls",
        "Amon/rlutcs",
        "Amon/rsutcs",
        "Amon/rsds",
        "Amon/rsdt",
        "Emon/rss",
        "AERmon/co2",
        "Lmon/nbp",
        "Omon/fgco2",
        "Amon/ua",
        "Amon/zg",
        "3hr/pr",
        "CF3hr/pr",
    ],
    "inm": [
        "SImon/siconc",
    ],
    "onm/grid-T": [
        "Omon/tos",
        "Omon/zos",
        "Omon/sos",
        "Omon/mlotst",
    ],
}

# Default information to write into the CDDS request file.
request_defaults = {
    "metadata": {
        "base_date": "1850-01-01T00:00:00",
        "branch_method": "no parent",
        "license": (
            "GCModelDev model data is licensed under the "
            "Open Government License v3 "
            "(https://www.nationalarchives.gov.uk/"
            "doc/open-government-licence/version/3/)"
        ),
        "mip": "ESMVal",
        "mip_era": "GCModelDev",
        "model_type": "AGCM AER",
    },
    "common": {
        "mode": "relaxed",
        "package": "round-1",
        "mip_table_dir": "/data/scratch/jonathan.lillis/mip_tables/0.0.25/",
    },
    "data": {
        "mass_data_class": "crum",
        "model_workflow_branch": "trunk",
        "model_workflow_revision": "not used except with data request",
    },
    "misc": {
        "atmos_timestep": 1200,
    },
    "conversion": {
        "mip_convert_plugin": "UKESM1",
        "mip_convert_external_plugin": "cmew_ukesm1_plugin",
        "skip_archive": True,
        "skip_qc": True,
        "cylc_args": "--no-detach -v",
        "model_params_dir": "$HOME/model_configs/",
    },
    "netcdf_global_attributes": {
        "further_info_url": "dummy_url",
    },
}
