.. (C) Crown Copyright 2022-2023, the Met Office.

Quick Start
===========

.. include:: ../common.txt

* Checkout the |CMEW|::

    git clone git@github.com:MetOffice/CMEW.git

* Configure the |CMEW|::

    cd CMEW/climate-model-evaluation-workflow
    rose

* If running any cylc commands and version of cylc is 8, run this command before moving to the next step ::

    export CYLC_VERSION=8

* Run the |CMEW| at the Met Office ::

    cylc vip -O metoffice

* Browse the logs using `Cylc Review`_, a web service for browsing logs via an
  HTTP interface.
