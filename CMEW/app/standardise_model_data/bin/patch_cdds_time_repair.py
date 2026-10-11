#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Patch the generated per-request CDDS conversion workflow so the NEMO
time metadata repair runs immediately after extraction.
"""
import argparse
import configparser
import os
import shlex
import sys
import logging

logging.basicConfig(level=logging.INFO, stream=sys.stdout)
filename = os.path.basename(__file__)
logger = logging.getLogger(filename)

SUPPORTED_STREAM = "onm"
ORIGINAL_COMMAND = (
    ". $setup; /usr/bin/time cdds_extract ${REQUEST_CONFIG_PATH} "
    "--streams ${STREAM}"
)


def read_request(request_path):
    """
    Parse a CDDS request configuration file.

    Parameters
    ----------
    request_path : str
        The full path to the CDDS request configuration file.

    Returns
    -------
    :class:`configparser.ConfigParser`
        The parsed request configuration.
    """
    config = configparser.ConfigParser()
    with open(request_path, "r") as file_handle:
        config.read_file(file_handle)
    return config


def derive_workflow_dir(config):
    """
    Derive the generated per-request CDDS conversion workflow directory.

    Parameters
    ----------
    config : :class:`configparser.ConfigParser`
        The parsed CDDS request configuration.

    Returns
    -------
    str
        The full path to the generated conversion workflow directory.
    """
    metadata = config["metadata"]
    common = config["common"]
    run_dir_name = "{}_{}_{}".format(
        metadata["model_id"],
        metadata["experiment_id"],
        metadata["variant_label"],
    )
    return os.path.join(
        common["root_proc_dir"],
        metadata["mip_era"],
        metadata["mip"],
        run_dir_name,
        common["package"],
        "convert",
        "cdds_{}".format(common["workflow_basename"]),
    )


def derive_input_dir(config):
    """
    Derive the extracted-input directory for the ``onm`` stream.

    Parameters
    ----------
    config : :class:`configparser.ConfigParser`
        The parsed CDDS request configuration.

    Returns
    -------
    str
        The full path to the extracted ``onm`` stream input directory.

    Raises
    ------
    ValueError
        If ``[data] streams`` is not exactly ``onm``.
    """
    metadata = config["metadata"]
    common = config["common"]
    streams = config["data"]["streams"].split()
    if streams != [SUPPORTED_STREAM]:
        raise ValueError(
            "Unsupported streams {!r}: this workaround currently only "
            "supports a request with exactly stream '{}'.".format(
                streams, SUPPORTED_STREAM
            )
        )

    run_dir_name = "{}_{}_{}".format(
        metadata["model_id"],
        metadata["experiment_id"],
        metadata["variant_label"],
    )
    return os.path.join(
        common["root_data_dir"],
        metadata["mip_era"],
        metadata["mip"],
        run_dir_name,
        common["package"],
        "input",
        # CDDS extracts archive data beneath the model workflow ID, not the
        # Cylc workflow basename.  The basename may be parent-run-specific
        # to avoid nested Cylc name collisions, while model_workflow_id
        # remains the actual MASS suite identifier.
        config["data"]["model_workflow_id"],
        SUPPORTED_STREAM,
    )


def build_repair_command(repair_script, input_dir):
    """
    Build the shell snippet that repairs NEMO time metadata.

    Parameters
    ----------
    repair_script : str
        The full path to ``repair_nemo_time_metadata.py``.
    input_dir : str
        The full path to the extracted ``onm`` stream input directory.

    Returns
    -------
    str
        The ``&&``-chained repair command, with the input directory
        shell-quoted and the extracted-file glob left outside the quotes
        so the shell can still expand it at run time.
    """
    return "python {} {}/nemo_*_1m_*_grid-T.nc".format(
        shlex.quote(repair_script), shlex.quote(input_dir)
    )


def patch_run_extract_app(workflow_dir, repair_script, input_dir):
    """
    Patch the generated ``run_extract`` Rose app to run the repair.

    Parameters
    ----------
    workflow_dir : str
        The full path to the generated conversion workflow directory.
    repair_script : str
        The full path to ``repair_nemo_time_metadata.py``.
    input_dir : str
        The full path to the extracted ``onm`` stream input directory.

    Raises
    ------
    FileNotFoundError
        If the workflow directory or the ``run_extract`` Rose app are
        missing.
    ValueError
        If the original ``cdds_extract`` command cannot be found.
    """
    if not os.path.isdir(workflow_dir):
        raise FileNotFoundError(
            "Generated CDDS workflow directory not found: {}".format(
                workflow_dir
            )
        )

    rose_app_path = os.path.join(
        workflow_dir, "app", "run_extract", "rose-app.conf"
    )
    if not os.path.isfile(rose_app_path):
        raise FileNotFoundError(
            "Generated run_extract Rose app not found: {}".format(
                rose_app_path
            )
        )

    with open(rose_app_path, "r") as file_handle:
        contents = file_handle.read()

    repair_command = build_repair_command(repair_script, input_dir)

    # CDDS 4.0.0 runs extraction and MIP conversion in one nested workflow
    # and provides no post-extraction hook. Patch only the request-scoped
    # generated workflow so NEMO time metadata is repaired before CDDS
    # validates and converts the extracted files.
    if repair_command in contents:
        logger.info(
            "Repair command already injected into %s; skipping.",
            rose_app_path,
        )
        return

    if ORIGINAL_COMMAND not in contents:
        raise ValueError(
            "Expected original cdds_extract command not found in "
            "{}".format(rose_app_path)
        )

    patched_contents = contents.replace(
        ORIGINAL_COMMAND,
        "{} && {}".format(ORIGINAL_COMMAND, repair_command),
    )

    with open(rose_app_path, "w") as file_handle:
        file_handle.write(patched_contents)

    logger.info("Injected repair command into %s", rose_app_path)


def parse_args(arguments):
    """
    Return the names and values of the command line arguments for
    the patching script.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.

    Returns
    -------
    :class:`argparse.Namespace`
        The names and values of the command line arguments.
    """
    parser = argparse.ArgumentParser(
        description=(
            "Patch the generated per-request CDDS conversion workflow so "
            "the NEMO time metadata repair runs after extraction."
        ),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--request-path",
        required=True,
        help="The full path to the CDDS request configuration file.",
    )
    parser.add_argument(
        "--repair-script",
        required=True,
        help="The full path to repair_nemo_time_metadata.py.",
    )
    return parser.parse_args(arguments)


def main(arguments=None):
    """
    Patch the generated CDDS conversion workflow for a given request.

    Parameters
    ----------
    arguments : :obj:`list` of :obj:`str`
        The command line arguments to be parsed.
    """
    args = parse_args(arguments)
    config = read_request(args.request_path)
    workflow_dir = derive_workflow_dir(config)
    input_dir = derive_input_dir(config)
    patch_run_extract_app(workflow_dir, args.repair_script, input_dir)


if __name__ == "__main__":
    main()
