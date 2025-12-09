.. (C) Crown Copyright 2022-2025, Met Office.
.. The LICENSE.md file contains full licensing details.

Quick Start
===========

.. include:: ../common.txt

* Ensure you have read the prerequisites


* Checkout |CMEW|::

    git clone git@github.com:MetOffice/CMEW.git


* Run |CMEW| at the Met Office with the current configuration::

    cylc vip -O metoffice


* Browse the logs using `Cylc Review`_, a web service for browsing logs via an
  HTTP interface.

.. note::   Model developers and others may wish to configure |CMEW|.
             These users should be aware of named and numbered runs in Cylc workflows.
