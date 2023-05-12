.. (C) Crown Copyright 2022-2023, the Met Office.

Quick Start
===========

.. include:: ../common.txt

* Checkout the |CAW|::

    git clone git@github.com:MetOffice/CMEW.git

* Configure the |CAW|::

    cd CMEW/CMEW
    rose edit

* Run the |CAW| at the Met Office, where ``<run-name>`` is a unique run name
  relevant to the current configuration::

    cylc vip --run-name=<run-name> -O metoffice

* Browse the logs using `Cylc Review`_, a web service for browsing logs via an
  HTTP interface.
