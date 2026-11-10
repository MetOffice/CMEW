.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

**********************************
Evaluating a model run with |CMEW|
**********************************

-------------------------------------------------------------------------------------------------
Comparing the radiation budget and monsoon assessment areas of a GC5 model run to a GC3 model run
-------------------------------------------------------------------------------------------------

.. include:: ../common.txt

0. Prerequisites
----------------

a) SSH access to GitHub
b) `moo hello`

1. Clone the |CMEW| repository from GitHub
------------------------------------------

In this tutorial,
we will put a copy of the |CMEW| workflow onto our local machine,
into a directory called ``cmew_tutorial`` on the home space.

**a) Create a new directory for the |CMEW| repository**

Type the following commands into a terminal window::

    cd ~
    mkdir cmew_tutorial
    cd cmew_tutorial

**b) Obtain the |CMEW| repository from GitHub**

In your terminal, type::

    git clone git@github.com:MetOffice/CMEW.git .

We now have a copy of CMEW that we can inspect and run.

Let's look at the |CMEW| repository.
Within the same terminal window, type::

    ls

We can confirm that the following have been created inside our directory `cmew_tutorial`:
 - ``CMEW`` (a directory)
 - ``CODE_OF_CONDUCT.md`` (a document)
 - ``doc`` (a directory)
 - ``README.md`` (a document)
 - ``SUPPORT.md`` (a document)
 - ``CONTRIBUTING.md`` (a document)
 - ``LICENSE.md`` (a document)
 - ``SECURITY.md`` (a document)

**c) Navigate to the directory containing the** ``flow.cylc`` **file**

All of the code and configuration relating to the workflow is in the directory ``CMEW``.
Let's inspect this directory::

    ls CMEW

We can confirm that files listed include ``flow.cylc`` and ``rose-suite.conf``.
To |Cylc| workflow,
we must be in the directory containing these files to edit and start the workflow.

    cd CMEW
