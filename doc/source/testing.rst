.. (C) Crown Copyright 2024, the Met Office.

*******
Testing
*******

.. include:: common.txt

Testing in |CMEW| can be done in one of two ways. Acceptance tests which run
in the ``compare`` task verify if the correct outputs are produced by the workflow.
Unit tests which are run inside the ``unittest`` task run ``pytest`` over
existing python scripts in the workflow.

To run the full |CMEW| workflow at the Met Office, with all tests enabled, use the command
    ``cylc vip -O metoffice -O test``

To only run the unit tests at the Met Office, use the command
    ``cylc vip -O metoffice -O unittest``
