.. (C) Crown Copyright 2022-2025, Met Office.
.. The LICENSE.md file contains full licensing details.

Quick Start
===========

.. include:: ../common.txt

* Complete all prerequisite steps


* Checkout |CMEW|::

    git clone git@github.com:MetOffice/CMEW.git


* Navigate to the directory containing the ``flow.cylc`` file, e.g.::

    cd CMEW/CMEW


* Run |CMEW| at the Met Office with the current configuration::

    cylc vip -O metoffice


* Monitor the workflow progress with ``cylc gui``,
  or browse the logs using `Cylc Review`_.

.. note::
   Model developers and others may wish to configure |CMEW|.
   These users should be aware of named and numbered runs in Cylc workflows.
