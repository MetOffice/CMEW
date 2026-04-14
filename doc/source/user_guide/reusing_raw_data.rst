.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Reusing pre-extracted pp files from MASS
========================================

.. include:: ../common.txt

It is possible to save non-standardised model output data (pp files) with |CMEW|,
to avoid having to extract them from MASS again in future.

This functionality is controlled by two variables in the `rose-suite.conf` file::

    RAW_DATA_ALREADY_EXTRACTED
    RAW_DATA_DIR

To copy the data, the user must run |CMEW| specifying the location to which to save the files,
e.g.::

    RAW_DATA_ALREADY_EXTRACTED="False"
    RAW_DATA_DIR="$SCRATCH/raw_data"

The pp files will be stored in subdirectories according to their stream (e.g. "apm"),
as this is the structure expected for later standardising the data.

.. warning::
   If the specified directory is not empty, |CMEW| will deliberately fail to copy the data.

In future runs, to avoid extracting the same data,
specify the same location when skipping the extract from MASS step,
e.g.::

    RAW_DATA_ALREADY_EXTRACTED="True"
    RAW_DATA_DIR="$SCRATCH/raw_data"

.. note::
   If only some of the necessary pp files have already been extracted,
   for example one model run but not another,
   it is **not currently possible** to reuse pp files with |CMEW|.
