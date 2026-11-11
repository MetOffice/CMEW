.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

.. include:: ../../common.txt

In this tutorial,
we will put a copy of the |CMEW| workflow onto our local machine
and use it to compare model run **u-cw673** to model run **u-bv546**
with regards to radiation budget and monsoon metrics.

We will use a single terminal and a single instance of the Rose GUI.
At some steps, the terminal will also open our internet browser.

Prerequisites
=============

a) SSH access to GitHub
b) ``moo hello``
c) No named runs of |CMEW| in ``cylc_run``

Clone the |CMEW| repository from GitHub
=======================================

In this section, we will copy |CMEW| from GitHub
into a directory called ``cmew_tutorial`` on the home space.

1) Create a new directory for the |CMEW| repository
---------------------------------------------------

Type the following commands into a terminal window::

    cd ~
    mkdir cmew_tutorial
    cd cmew_tutorial

2) Obtain the |CMEW| repository from GitHub
-------------------------------------------

In your terminal, type::

    git clone git@github.com:MetOffice/CMEW.git .

We now have a copy of CMEW that we can inspect and run.

3) Inspect our new repository
-----------------------------

Let's investigate at the |CMEW| repository.
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

.. note::
   Cloning the CMEW repository does not have to be done every time a user wishes to run |CMEW|.
   However, as it is likely that |CMEW| will undergo further development,
   we recommend periodically updating the repository from GitHub.
