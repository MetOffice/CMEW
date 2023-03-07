.. (C) Crown Copyright 2022, the Met Office.

Quick Start
===========

.. include:: ../common.txt

* Checkout the |CMEW|::

    git clone git@github.com:MetOffice/climate-model-evaluation-workflow.git

* Configure the |CMEW|::

    cd climate-model-evaluation-workflow/climate-model-evaluation-workflow
    rose edit

* Run the |CMEW| at the Met Office, where ``<run-name>`` is a unique run name
  relevant to the current configuration::

    cylc install --run-name=<run-name> -O metoffice
    cylc play climate-model-evaluation-workflow/<run-name>

* Browse the logs using `Cylc Review`_, a web service for browsing logs via an
  HTTP interface.
