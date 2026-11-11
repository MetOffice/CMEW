.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

.. include:: ../../common.txt

==================
Inspect the output
==================

|CMEW| outputs images to webpages.
The style of the pages will be determined by whether the assessment tool was AutoAssess or ESMValTool.

-------------------------------------
1) Explore the ``cylc_run`` directory
-------------------------------------

In your terminal, type the commands::

   cd ~/cylc_run/CMEW/runN/
   ls

This takes us to the directory for the most recent run of |CMEW|,
and displays the contents.

All of the output is in subdirectories of the shared directory for the cycle.
Navigate further into this directory::

   cd share/cycle/1/
   ls

We will find two subdirectories at this level:

 - ``recipe_radiation_budget_<date and time>``, and
 - ``u-cw673_vs_u-bv526``.

The first of these contains our output for the ESMValTool recipe ``radiation_budget``,
and the second contains all AutoAssess output.

------------------------------
2) Open the AutoAssess results
------------------------------

In your terminal, type the command::

   gio open u-cw673_vs_u-bv526/index.html

This will open an internet browser window,
displaying output for the AutoAssess area ``monsoon``.

We will notice the string *A comparison of my model run against a previous version*,
which we noted earlier in the tutorial.

------------------------------
3) Open the ESMValTool results
------------------------------

In your internet browser,
remove ``u-cw673_vs_u-bv526/index.html`` from the end of the address and press enter.
Now the browser will display both subfolders.

Click on the folder name ``recipe_radiation_budget_<date and time>``,
then on ``index.html``.

The browser now displays outputs for the ESMValTool recipe ``radiation_budget``.

**Congratulations, you have now finished the CMEW tutorial!**
