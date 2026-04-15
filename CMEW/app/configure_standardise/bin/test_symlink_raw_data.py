#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Unit tests for symlink_raw_data.py
"""
from unittest.mock import patch
import pytest
import tempfile
from pathlib import Path
from symlink_raw_data import (
    determine_model_run_target_dir,
    symlink_pp_files,
    main,
)


def test_determine_model_run_target_dir(monkeypatch):
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
    actual = determine_model_run_target_dir(mock_dict)
    assert actual == expected


def test_symlink_pp_files(monkeypatch):
    # Make a mock source directory
    with tempfile.TemporaryDirectory() as mock_src_dir:
        mock_src_dir = Path(mock_src_dir)
        # Containing two subdirectories
        subdir_1 = mock_src_dir / "subdir_1"
        subdir_2 = mock_src_dir / "subdir_2"
        subdir_1.mkdir(parents=True)
        subdir_2.mkdir(parents=True)
        # Each containing two files, one both pp and one with one non-pp file
        (subdir_1 / "a_1.pp").write_text("Contents of a_1")
        (subdir_1 / "b_1.pp").write_text("Contents of b_1")
        (subdir_2 / "a_2.pp").write_text("Contents of a_2")
        (subdir_2 / "b_2.txt").write_text("This shouldn't copy")

        # Make a mock target parent directory
        with tempfile.TemporaryDirectory() as mock_target_dir:
            mock_target_dir = Path(mock_target_dir)

            # Run the symlink function:
            symlink_pp_files(str(mock_src_dir), str(mock_target_dir))

            # a_1 should copy:
            with open(mock_target_dir / "subdir_1" / "a_1.pp") as f:
                actual = f.read()
                expected = "Contents of a_1"
                assert actual == expected

            # b_1 should copy:
            with open(mock_target_dir / "subdir_1" / "b_1.pp") as f:
                actual = f.read()
                expected = "Contents of b_1"
                assert actual == expected

            # a_2 should copy:
            with open(mock_target_dir / "subdir_2" / "a_2.pp") as f:
                actual = f.read()
                expected = "Contents of a_2"
                assert actual == expected

            # b_2 should NOT copy:
            with pytest.raises(FileNotFoundError):
                with open(mock_target_dir / "subdir_2" / "b_2.pp") as f:
                    f.read()


class TestMain:
    # RAW_DATA_DIR is queried if RAW_DATA_ALREADY_EXTRACTED == True
    def test_already_extracted(self, monkeypatch):
        monkeypatch.setenv("RAW_DATA_ALREADY_EXTRACTED", "True")
        monkeypatch.setenv("RAW_DATA_DIR", "")
        # Should call symlink_raw_data if RAW_DATA_ALREADY_EXTRACTED
        with patch("symlink_raw_data.symlink_raw_data") as mock_symlink:
            main()
            mock_symlink.assert_called_once()
        pass

    def test_not_extracted(self, monkeypatch):
        monkeypatch.setenv("RAW_DATA_ALREADY_EXTRACTED", "False")
        # Otherwise should not call symlink_raw_data
        with patch("symlink_raw_data.symlink_raw_data") as mock_symlink:
            main()
            mock_symlink.assert_not_called()
        pass
