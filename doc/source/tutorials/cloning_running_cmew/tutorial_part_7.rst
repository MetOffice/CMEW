.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Inspect the output
------------------

|CMEW| outputs images to webpages.
The style of the pages will be determined by whether the assessment tool was AutoAssess or ESMValTool.

1) Explore the ``cylc-run`` directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: On the command line, type
   :class: admonition-todo

   .. code-block::

      cd ~/cylc-run/CMEW/GC5_vs_GC3/
      ls

This takes us to the directory for our tutorial run of |CMEW|,
and displays the contents.

All of the output is in subdirectories of the shared directory for the cycle.
Navigate further into this directory:

.. admonition:: On the command line, type
   :class: admonition-todo

   .. code-block::

      cd share/cycle/1/
      ls

We will find two subdirectories at this level:

* ``recipe_radiation_budget_<date and time>``, and
* ``u-cw673_vs_u-bv526``.

The first of these contains our output for the ESMValTool recipe ``radiation_budget``,
and the second contains all AutoAssess output.

2) Open the AutoAssess results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: On the command line, type
   :class: admonition-todo

   .. code-block::

      gio open u-cw673_vs_u-bv526/index.html

This will open an internet browser window,
displaying output for the AutoAssess area ``monsoon``.
No images show in the other areas,
because we did not select them in the "Assessment Areas" section of the Rose GUI earlier on.

.. image:: images/autoassess_output.png
   :alt: An image of a webpage with the title
         "A comparison of my mode run against a previous version",
         with subtitles "u-cw673 vs. u-bv526 (reference)"
         and "1992/12/01 to 1994/12/01",
         a blue link with text "Validation Note",
         and the top of a graph under the section header "Monsoon".
         An enlargement of the graph's legend displays the text
         "Vs A GC 3.1 reference run (u-bv526), CMEW tutorial model run (u-cw673)".
   :width: 600px

We read the title *A comparison of my model run against a previous version*,
which we noted earlier in the tutorial.

We can also note that a link has been created to the Validation Note ("ValNote"),
but as we did not select ``valnote`` as an assessment area earlier,
this will not lead us to any further output.

3) Open the ESMValTool results
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. admonition:: In your internet browser,
   :class: admonition-todo

   * remove ``u-cw673_vs_u-bv526/index.html`` from the end of the address, then
   * press enter.

Now the browser will display both subfolders.

.. admonition:: In your internet browser, click
   :class: admonition-todo

   * the folder name ``recipe_radiation_budget_<date and time>``, then
   * ``index.html``.

The browser now displays outputs for the ESMValTool recipe ``radiation_budget``.
To display the plots produced, we must scroll about two thirds of the way down the page.

.. image:: images/esmvaltool_output.png
   :alt: An image of a webpage section with the title
         "Single_Value_Radiation_Budget",
         with three graphs displayed.
         An enlargement of each graph's title in turn displays the texts
         "Radiation budget for ACCESS-CM2 for comparison",
         "Radiation budget for A GC 3.1 reference run", and
         "Radiation budget for CMEW tutorial model run".
   :width: 600px

Here we will notice an *extra* graph, for dataset "ACCESS-CM2",
that we did not enter into our datasets section earlier on.
Let's find out where the instruction to include this dataset came from.

Now we will navigate to the CMIP6 dataset information in the Rose GUI.
Under the section **Datasets**:

.. admonition:: In the Rose GUI, click
   :class: admonition-todo

   * the arrow next to **Extra CMIP6 datasets for ESMValTool**, then
   * the option **1**.

We can confirm that details for the ACCESS-CM2 dataset were also present in the configuration.
Currently, |CMEW| will only successfully include a CMIP6 dataset in an ESMValTool recipe
if all the necessary data already exists locally.
The data for running the radiation budget recipe for the CMIP6 model ACCESS-CM2
had already been added to drives at the Met Office.

**Congratulations, you have now finished the CMEW tutorial!**
