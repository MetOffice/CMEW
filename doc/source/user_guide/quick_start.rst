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

* Run |CMEW| at the Met Office, where ``<run-name>`` is a unique run name
  relevant to the current configuration::

    cylc vip --run-name=<run-name> -O metoffice

* Browse the logs using `Cylc Review`_, a web service for browsing logs via an
  HTTP interface.
