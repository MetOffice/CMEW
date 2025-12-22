# (C) Crown Copyright 2025, Met Office.
# The LICENSE.md file contains full licensing details.

Prerequisites for Cloning and Running CMEW at the Met Office
============================================================

.. include:: ../common.txt

This page lists the prerequisites for the metoffice site:
  * Cloning the Climate Model Evaluation Workflow (|CMEW|) repository
  * Running |CMEW| on Met Office systems

|CMEW| users at the Met Office will need access to:
  * Git
  * Cylc
  * MASS
  * The ESMValTool community environment
  * |CDDS|

1 Cloning the CMEW repository
-----------------------------

1.1. Access and Network
^^^^^^^^^^^^^^^^^^^^^^^

* A valid user account.
* Internet access to the |CMEW| GitHub repository (via SSH or HTTPS).

1.2. Git Installed
^^^^^^^^^^^^^^^^^^

**git** must be available on your login node.

* Check::

    git --version

1.3. GitHub Authentication
^^^^^^^^^^^^^^^^^^^^^^^^^^

You need either **SSH** or **HTTPS** authentication.

1.4 Access and Platform for Running CMEW
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

You must be able to submit Slurm jobs under a valid account/project.

Quick checks::

    sinfo
    squeue -u $USER

2 Cylc and Rose
---------------

On the Met Office system, Cylc and Rose are normally provided centrally. These versions are known to work with the CMEW prototype:

  * Cylc Flow 8.x (e.g. 8.6.1)
  * Rose 2.x (e.g. 2.6.2)

Verify you are using the system stack::

    which cylc
    cylc --version
    which rose
    rose --version

Expected examples::

    /usr/local/bin/cylc with Cylc 8.6.1
    /usr/local/bin/rose with Rose 2.6.2

2.1 Diagnostics Environment (ESMValTool)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|CMEW| runs ESMValTool recipes for diagnostics. You need:

  * a working ESMValTool installation available on your Linux system

Sanity check after loading the esmvaltool module::

  module load scitools/community/esmvaltool/2.10.0
  esmvaltool --version

2.2 Met Office MOOSE account is required
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check that a valid MOOSE account exists.
Verify that the credentials file is installed correctly and that MASS access is possible::

  moo si -v

Contact ServiceNow for a MOOSE account on your Linux system if there is no access to MASS.

2.3 Standardisation Environment (CDDS / CMORisation)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

|CMEW| standardises model data prior to diagnostics using CDDS.
You need:

* CDDS installed on the Met Office system (confirmed)
