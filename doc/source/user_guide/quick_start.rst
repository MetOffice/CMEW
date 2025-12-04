.. (C) Crown Copyright 2022-2025, Met Office.
.. The LICENSE.md file contains full licensing details.

Quick Start
===========

.. include:: ../common.txt

* Checkout |CMEW|::

    git clone git@github.com:MetOffice/CMEW.git

* Configure |CMEW|::

    cd CMEW/CMEW
    rose edit

* Run |CMEW| at the Met Office with the current configuration,
  either without specifiying a run name::

    cylc vip -O metoffice

  or by supplying a unique run name relevant to the current configuration
  (e.g. for identifying your run later on)::

    cylc vip --run-name=<run-name> -O metoffice

* Browse the logs using `Cylc Review`_, a web service for browsing logs via an
  HTTP interface.
