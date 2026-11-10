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

a) Access to GitHub
b) `moo hello`

1. Clone the |CMEW| repository from GitHub
------------------------------------------

We will put a copy of the CMEW workflow onto our local machine,
into a directory called `cmew_tutorial` on the home space.

The following steps should be undertaken in a terminal.

a) Create a new directory for the |CMEW| repository::

    cd ~
    mkdir cmew_tutorial
    cd cmew_tutorial

b) Obtain the |CMEW| repository from GitHub::

    git clone git@github.com:MetOffice/CMEW.git .

We now have a copy f CMEW that we can inspect and run.

Let's look at the |CMEW| repository.
Within the same terminal window, type::

    ls

We can see the following have been created inside our directory `cmew_tutorial`:
CMEW
CODE_OF_CONDUCT.md
doc
README.md
SUPPORT.md
cmewpy
CONTRIBUTING.md
LICENSE.md
SECURITY.md
