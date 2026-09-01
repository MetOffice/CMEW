#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""Extract and persist one variable cube per NetCDF file.

The ESMValCore concatenation function which is used to combine NetCDF files
into a single file for each variable can fail if a file contains multiple
cubes, especially if these cubes have different time coordinates. This script
extracts the cube for a single variable, ensuring that ESMValTool can correctly
ingest the data."""

from __future__ import annotations

import logging
import os
import sys
from pathlib import Path
from typing import Any

import iris
import yaml
from iris.cube import Cube, CubeList
from iris.exceptions import CoordinateNotFoundError

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(Path(__file__).name)


def load_model_runs(path: Path) -> dict[str, dict[str, Any]]:
    """Load model run metadata from a YAML file."""
    with open(path, "r", encoding="utf-8") as handle:
        model_runs: dict[str, dict[str, Any]] = yaml.safe_load(handle)
    return model_runs


def retrieve_variable_list(path: Path) -> list[tuple[str, str]]:
    """Load ``(mip, variable)`` pairs from the CDDS variables file."""
    pairs: list[tuple[str, str]] = []
    with open(path, "r", encoding="utf-8") as handle:
        for raw_line in handle:
            line = raw_line.strip()
            if not line:
                continue
            variable_token = line.split(":", maxsplit=1)[0]
            if "/" not in variable_token:
                logger.warning("Skipping malformed variable token '%s'", line)
                continue
            mip, variable = variable_token.split("/", maxsplit=1)
            pairs.append((mip, variable))
    logger.info("Loaded %d variables from %s", len(pairs), path)
    return pairs


def find_files(
    root_dir: Path,
    dataset_config: dict[str, Any],
    mip: str,
    variable: str,
) -> list[Path]:
    """Return NetCDF files matching the dataset and variable location."""
    dataset_root = (
        root_dir
        / "GCModelDev"
        / str(dataset_config["activity"])
        / str(dataset_config["institute"])
        / str(dataset_config["model_id"])
        / str(dataset_config["experiment_id"])
        / str(dataset_config["variant_label"])
        / mip
        / variable
    )

    if not dataset_root.exists():
        logger.warning(
            "No directory for %s/%s at %s",
            mip,
            variable,
            dataset_root,
        )
        return []

    files = sorted(dataset_root.rglob("*.nc"))
    logger.info(
        "Found %d NetCDF files for %s/%s at %s",
        len(files),
        mip,
        variable,
        dataset_root,
    )
    return files


def cube_matches_variable(cube: Cube, variable: str) -> bool:
    """Check whether the cube identifier matches ``variable``."""
    return (
        cube.var_name == variable
        or cube.standard_name == variable
        or cube.long_name == variable
    )


def cube_has_time_coordinate(cube: Cube) -> bool:
    """Return ``True`` if ``cube`` has a single time coordinate."""
    try:
        cube.coord("time")
    except CoordinateNotFoundError:
        return False
    return True


def sanitize_cube_for_output(cube: Cube) -> Cube:
    """Return a cube safe for overwrite in variable-only NetCDF files.

    Some files include surface altitude as an auxiliary coordinate
    (``orog``). When written back, Iris may expose that variable as a
    separate cube on reload, which then breaks ESMValCore concatenation.
    """
    cleaned_cube = cube.copy()

    # Remove auxiliary factories first so dependent coords can be removed.
    for aux_factory in list(cleaned_cube.aux_factories):
        cleaned_cube.remove_aux_factory(aux_factory)

    coords_to_remove = []
    for coord in cleaned_cube.aux_coords:
        if (
            coord.var_name == "orog"
            or coord.standard_name == "surface_altitude"
            or coord.long_name == "Surface Altitude"
        ):
            coords_to_remove.append(coord)

    for coord in coords_to_remove:
        cleaned_cube.remove_coord(coord)

    return cleaned_cube


def pick_matching_cube(
    cubes: CubeList,
    variable: str,
    file_path: Path,
) -> Cube:
    """Pick the cube that matches a requested variable.

    Raises
    ------
    ValueError
        If a unique matching cube cannot be identified.
    """
    matching_cubes = [
        cube for cube in cubes if cube_matches_variable(cube, variable)
    ]

    timed_matching_cubes = [
        cube for cube in matching_cubes if cube_has_time_coordinate(cube)
    ]

    if len(timed_matching_cubes) == 1:
        return timed_matching_cubes[0]

    if len(timed_matching_cubes) > 1:
        var_name_matches = [
            cube for cube in timed_matching_cubes if cube.var_name == variable
        ]
        if len(var_name_matches) == 1:
            return var_name_matches[0]
        raise ValueError(
            "Found multiple timed cubes for variable "
            f"'{variable}' in {file_path}"
        )

    if len(matching_cubes) == 1:
        raise ValueError(
            "Matched cube for variable "
            f"'{variable}' has no time coordinate in {file_path}"
        )

    if len(matching_cubes) > 1:
        # Prefer an exact var_name match if one unique candidate exists.
        var_name_matches = [
            cube for cube in matching_cubes if cube.var_name == variable
        ]
        if len(var_name_matches) == 1:
            return var_name_matches[0]
        raise ValueError(
            f"Found multiple cubes for variable '{variable}' in {file_path}"
        )

    raise ValueError(
        "Could not find a unique timed cube for variable "
        f"'{variable}' in {file_path}"
    )


def overwrite_with_single_cube(file_path: Path, variable: str) -> None:
    """Load a NetCDF file and overwrite it with the target variable cube."""
    cubes = iris.load(str(file_path))
    try:
        selected_cube = pick_matching_cube(cubes, variable, file_path)
    except ValueError as exc:
        logger.warning("Skipping %s: %s", file_path, exc)
        return
    selected_cube = sanitize_cube_for_output(selected_cube)

    logger.info(
        "Found timed cube for variable '%s' in %s; overwriting file",
        variable,
        file_path,
    )
    logger.info("Cube details: %s", selected_cube)
    temp_path = file_path.with_suffix(".tmp.nc")
    if temp_path.exists():
        temp_path.unlink()

    # Touch the data to ensure it is loaded into memory before saving.
    selected_cube.data  # noqa: B018

    iris.save(selected_cube, str(temp_path))
    temp_path.replace(file_path)


def main() -> None:
    """Run variable cube extraction for all datasets and variables."""
    root_dir = Path(os.environ["ROOT_RESTRUCTURED_DIR"])
    model_runs_path = Path(os.environ["DATASETS_LIST_DIR"]) / "model_runs.yml"
    variables_dir = Path(os.environ["CYLC_WORKFLOW_SHARE_DIR"]) / "etc"

    logger.info("Loading model runs from %s", model_runs_path)
    model_runs = load_model_runs(model_runs_path)

    total_files = 0
    for dataset, dataset_config in model_runs.items():
        variables_path = variables_dir / f"variables_{dataset}.txt"
        if not variables_path.exists():
            logger.warning(
                "Variables file not found for dataset %s: %s",
                dataset,
                variables_path,
            )
            continue

        logger.info("Processing dataset %s", dataset)
        variables = retrieve_variable_list(variables_path)

        for mip, variable in variables:
            netcdf_files = find_files(root_dir, dataset_config, mip, variable)
            for file_path in netcdf_files:
                overwrite_with_single_cube(file_path, variable)
                total_files += 1

    logger.info("Completed variable extraction for %d files", total_files)


if __name__ == "__main__":
    main()
