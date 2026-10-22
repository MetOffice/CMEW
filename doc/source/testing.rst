.. (C) Crown Copyright 2024-2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Testing
=======

.. include:: common.txt

|CMEW| contains two types of tests:

* **End-to-end tests**.
  |CMEW| end-to-end tests verify whether the evaluation tools
  produce the expected output files.
  These checks are performed via the ``compare`` task.
  They do not check the contents of those files;
  this is covered by the Recipe Test Workflow.
* **Unit tests**.
  |CMEW| unit tests ensure key functions
  in the ``cmewpy`` Python package behave as expected.
  These tests are run using ``pytest``.

How to run tests in |CMEW|
--------------------------

Run the end-to-end tests
~~~~~~~~~~~~~~~~~~~~~~~~

* Navigate to the workflow directory::

    cd <desired_repository_location>/CMEW/CMEW

* Run |CMEW| at the Met Office, with all tests enabled::

    cylc vip -O metoffice -O test

* Ensure the tests pass. One way to do this is to check `Cylc Review`_.

Run the unit tests via |CMEW|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Navigate to the workflow directory::

    cd <desired_repository_location>/CMEW/CMEW

* Run the unit tests at the Met Office::

    cylc vip -O metoffice -O unittest

* Ensure the tests pass. One way to do this is to check `Cylc Review`_.

Run the unit tests from the command line
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

* Navigate to the ``cmewpy`` directory::

    cd <desired_repository_location>/CMEW/cmewpy

* Run the unit tests::

    pytest
