.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Clone the |CMEW| repository from GitHub
=======================================

In this section, we will copy |CMEW| from GitHub
into a directory called ``cmew_tutorial`` in your home area.

1) Create a new directory for the |CMEW| repository
---------------------------------------------------

Type the following on the command line::

    cd
    mkdir cmew_tutorial
    cd cmew_tutorial

2) Obtain the |CMEW| repository from GitHub
-------------------------------------------

On the command line, type::

    git clone git@github.com:MetOffice/CMEW.git .

We now have a copy of CMEW that we can inspect and run.

3) Inspect our new repository
-----------------------------

Let's investigate the |CMEW| repository.
On the command line, type::

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
