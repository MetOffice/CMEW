.. (C) Crown Copyright 2024-2025, Met Office.
.. The LICENSE.md file contains full licensing details.

*******
Testing
*******

.. include:: common.txt

Testing in |CMEW| can be done in one of two ways. Acceptance tests which run
in the ``compare`` task verify if the correct outputs are produced by the
workflow (ESMValTool tests, e.g. the Recipe Test Workflow, ensures
the contents of the output files are as expected). Unit tests which are run
inside the ``unittest`` task run ``pytest`` over existing python scripts in the
workflow.

The process to run the tests is as follows:

 * Navigate to the workflow directory,
   e.g. ``cd <desired_repository_location>/CMEW/CMEW``

 * Run either the workflow end-to-end (acceptance) tests or Python unit tests

   * Run the full |CMEW| workflow at the Met Office, with all tests enabled,
     using the command ``cylc vip -O metoffice -O test``

   * Run only the unit tests at the Met Office,
     using the command ``cylc vip -O metoffice -O unittest``

 * Ensure the tests pass. One way to do this is to check `Cylc Review`_
