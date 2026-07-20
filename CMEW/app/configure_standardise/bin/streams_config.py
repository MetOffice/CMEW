#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Information on which streams contain variables from different MIP tables.
"""
streams_dict = {
    "apm": [
        "Amon/hfls",
        "Amon/hfss",
        "Amon/rlds",
        "Amon/rlut",
        "Amon/rlutcs",
        "Amon/rsds",
        "Amon/rsdt",
        "Amon/rsut",
        "Amon/rsutcs",
        "Amon/tas",
        "Emon/rls",
        "Emon/rss",
    ],
    "inm": [
        "SImon/siconc",
    ],
    "onm/grid-T": [
        "Omon/tos",
    ],
}
