.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Troubleshooting
===============

The ``extract_data`` tasks fail
-------------------------------

At the Met Office, this could be due to being logged out of MASS.

**Confirm diagnosis:**
``~/cylc-run/CMEW/<run-name>/log/job/1/extract_data_<assessment_area>_<dataset>/runN/job.err``
will contain the line
``select, command-id=<command_id>, (NOT_LOGGED_IN) run 'moo login' to continue.``

**Solution:**
Type ``moo login`` on the command line to be prompted to log in.


The cdds_CMEW workflows fail
----------------------------

At the Met Office, this could be due to being logged out of MASS.

**Confirm diagnosis:**
The ``run_extract_<stream>`` tasks will have failed, with
``~/cylc-run/cdds_CMEW/<run-name>_<dataset>/log/job/<start_year>0101T0000Z/run_extract_<stream>/NN/job.out``
containing the line
``test, command-id=<command_id>, (NOT_LOGGED_IN) run 'moo login' to continue.``

**Solution:**
Type ``moo login`` on the command line to be prompted to log in.
