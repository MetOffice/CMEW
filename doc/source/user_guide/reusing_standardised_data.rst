.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Reusing pre-standardised data files from CMEW
=============================================

.. include:: ../common.txt

In rare circumstances, a user may wish to re-use standardised data
from one |CMEW| run in a future |CMEW| run.
This is mostly likely to be the case when only the recipe step has failed,
so that the exact combination of model runs, variables and time period are required.

In the case of a failed recipe run, the ``housekeeping`` task will not have run.
This means the standardised data will still exist in the workflow directory,
and this may be copied elsewhere for future use.

Steps for reusing standardised data at the Met Office:
------------------------------------------------------

First copy the standardised data files and file structure exactly.
The directory to copy is named ``GCModelDev`` and is found in the ``share/work`` directory
of the failed run.
e.g.::

    mkdir -p $SCRATCH/cmew_data/
    cp -r $HOME/cylc-run/CMEW/runN/share/work/GCModelDev $SCRATCH/cmew_data/


Next add the following two variables to the ``rose-suite.conf`` file::

    SKIP_CDDS=true
    STANDARDISED_DATA_DIR="$SCRATCH/cmew_data"


Following |CMEW| runs will skip the |CDDS| steps and symlink the pre-standardised data.

.. note::
   It is possible to save standardised data ahead of a failed run,
   by manually removing the ``housekeeping`` task from the workflow.
   However, this is not envisaged to be a common user requirement
   and familiarity with |Cylc| run manipulation is required.
