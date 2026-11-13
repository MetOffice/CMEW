.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

In this tutorial,
we will put a copy of the |CMEW| workflow onto our local machine
and use it to compare model run **u-cw673** to model run **u-bv546**
with regards to radiation budget and monsoon metrics.

We will use a single terminal, which will at times open the Rose GUI.
At some steps, the terminal will also open our internet browser.

Prerequisites
=============

a) SSH access to GitHub
b) ``moo login``
c) No previous runs of |CMEW| in ``cylc-run``

.. dropdown:: What if I do have previous runs of CMEW?

   We are going to use a named run of |CMEW| in this tutorial.
   |Cylc| will not allow a mixture of named and numbered runs of the same workflow.
   |Cylc| will also not allow the same workflow to be run from different locations,
   and this tutorial installs |CMEW| into a new directory.

   If the above apply,
   then in order to follow the steps in this tutorial,
   you will have to clean all previous runs of |CMEW|.

   To do this, clean all workflow containing "CMEW" with the command::

       cylc clean '*CMEW*'
