#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for symlink_raw_data.py
"""
from unittest.mock import patch
import tempfile
from pathlib import Path
from symlink_raw_data import determine_target_dir, symlink_pp_files, main


def test_determine_target_dir(monkeypatch):
    monkeypatch.setenv("ROOT_DATA_DIR", "/path/to/cdds_data")
    mock_dict = {
        "activity": "ESMVal",
        "calendar": "360_day",
        "end_year": "2002",
        "experiment_id": "historical",
        "grid": "gn",
        "institute": "MOHC",
        "label_for_plots": "Ref Test Label",
        "model_id": "HadGEM3-GC31-LL",
        "project": "ESMVal",
        "start_year": "1993",
        "sub_experiment": "ubv526",
        "suite_id": "u-bv526",
        "variant_label": "r5i1p1f3",
    }
    expected = (
        "/path/to/cdds_data/"
        "GCModelDev/"
        "ESMVal/"
        "HadGEM3-GC31-LL/"
        "historical/"
        "r5i1p1f3/"
        "round-1/"
        "input/"
        "u-bv526"
    )
    actual = determine_target_dir(mock_dict)
    assert actual == expected


def test_symlink_pp_files():
    pass


class TestMain:
    def test_already_extracted(self, monkeypatch):
        monkeypatch.setenv("RAW_DATA_ALREADY_EXTRACTED", "True")
        # Should call symlink_pp_dirs if RAW_DATA_ALREADY_EXTRACTED
        with patch("symlink_raw_data.symlink_pp_files") as mock_symlink:
            main()
            mock_symlink.assert_called_once()
        pass
    def test_not_extracted(self, monkeypatch):
        monkeypatch.setenv("RAW_DATA_ALREADY_EXTRACTED", "False")
        # Otherwise should not call symlink_pp_dirs
        with patch("symlink_raw_data.symlink_pp_files") as mock_symlink:
            main()
            mock_symlink.assert_not_called()
        pass
