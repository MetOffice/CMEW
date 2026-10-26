.. (C) Crown Copyright 2022-2026, Met Office.
.. The LICENSE.md file contains full licensing details.

********
Glossary
********

.. include:: common.txt

.. glossary::

   Assessment Area
     A thematic aspect of model performance; a collection of |metrics| and plots
     relating to that thematic aspect, owned by a single domain expert.
     An assessment area contains at least one |recipe| and multiple |metrics|.

   AutoAssess
     `AutoAssess`_ is the internal Met Office tool for evaluating climate model
     simulations. It is being phased out in preference to |CMEW| and
     |ESMValTool| |recipes|.

   CDDS
     CDDS is a package that |CMEW| uses to standardise data for use in
     |ESMValTool| |recipes|.

   CMEW
     Climate Model Evaluation Workflow.

   CMIP
     Coupled Model Intercomparison Project, see the `CMIP Documentation`_.

   Cylc
     Cylc (“silk”) is a workflow engine for cycling systems, see the
     `Cylc Documentation`_.

   ESM
     Earth System Model

   ESMValTool
     ESMValTool is a community diagnostic and performance |metrics| tool for
     routine evaluation of |ESMs| in |CMIP|, see the
     `ESMValTool Documentation`_.

   Metric
     A number that quantifies model performance.

   MIAO
     Model Inputs And Outputs

   NAC Plot
     A Normalised Assessment Criteria (NAC) plot displays the relative value of
     model |metrics| to a given reference model. There is also the possibility of
     displaying observational and uncertainty information if provided, this also
     allows the plot to indicate whether the test |metrics| are in some sense
     better or worse than the reference.

   Recipe
     A grouping of |metrics|. If multiple |metrics| are needed for a single
     plot, they must be grouped together in a single |recipe|. A |recipe| may
     contain one or more plots. A |NAC Plot| could also be used to summerise the
     |metrics| in a recipe.

   Rose
     Rose is a toolkit for writing, editing and running application
     configurations, see the `Rose Documentation`_.
