.. (C) Crown Copyright 2025-2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Prerequisites for running CMEW at the Met Office
================================================

.. include:: ../common.txt

Multiple tools are required to run |CMEW|.

If you have a standard Linux account at the Met Office, these tools are typically already available, and the commands in the table below should work without additional setup.

Software prerequisites
----------------------

.. list-table::
   :header-rows: 1
   :widths: 20 25 25 30

   * - Tool
     - Command-line tool
     - Available by default?
     - Installation check
   * - Git
     - ``git``
     - Yes
     - ``which git``
       ``git --version``
   * - |Rose|
     - ``rose``
     - Yes
     - ``which rose``
       ``rose --version``
   * - |Cylc|
     - ``cylc``
     - Yes
     - ``which cylc``
       ``cylc --version``
   * - |CDDS|
     - ``cdds_convert``
     - No, run
       ``source ~cdds/bin/setup_env_for_cdds 3.2.0``
     - ``which cdds_convert``
       ``cdds_convert --help``
   * - MOOSE
     - ``moo``
     - Yes
     - ``which moo``
   * - |ESMValTool|
     - ``esmvaltool``
     - No, run
       ``module load scitools/community/esmvaltool/2.12.0``
     - ``which esmvaltool``
       ``esmvaltool --version``

Account and access requirements
--------------------------------

In addition to the software listed above, user accounts must be correctly configured for the following services.

.. list-table::
   :header-rows: 1
   :widths: 20 35 35

   * - Tool / service
     - Access check
     - Request account
   * - GitHub
     - https://github.com/login
     - https://github.com/signup
   * - MOOSE
     - ``moo --help``
     - ServiceNow

You must also be able to submit Slurm jobs under a valid Met Office account and project. A quick check is:

::

   sinfo
   squeue -u $USER
