.. (C) Crown Copyright 2022-2026, Met Office.
.. The LICENSE.md file contains full licensing details.
.. include:: ../common.txt

The workflow
============

An overview of the workflow
---------------------------

|CMEW| performs the following steps:

``install_env_file``
  :Description:
     Activates the environment for |ESMValTool|, based on the ``SITE`` provided.
  :Executes:
     The ``install_env_file.sh`` script from the |Rose| app.
  :Details:
     Runs once at the start of the workflow.

``copy_datasets``
  :Description:
     Reads the namelist files in the top level of the cylc workflow,
     then copies these details to YAML files
     in the cylc workflow ``share/etc`` directory.
  :Executes:
     The ``add_datasets_to_share.py`` script from the |Rose| app.
  :Details:
     Runs once.

``configure_recipe``
  :Description:
     Creates and modifies the |ESMValTool| user and developer configuration files,
     and writes them to the cylc workflow ``share/etc`` directory.
  :Executes:
     The ``configure_recipe.py`` script from the |Rose| app.
  :Details:
     Runs immediately after the successful completion of the ``install_env_file`` job.
     Temporarily, creates ESMValTool developer configuration file at ``share/etc`` directory in the installed workflow.

``configure_for``
  :Description:
     Copies an updated version of the |ESMValTool| recipe
     into the Cylc workflow ``share/etc`` directory
     in the installed workflow and configures it
     to use standardised model data.
     Also reads the required variables from the recipe
     and writes these to a folder in the Cylc workflow ``share/etc`` directory
     for use later in the workflow.
  :Executes:
     For the required recipe,
     executes the ``esmvaltool recipes get`` command
     followed by the ``update_recipe_file.py`` and ``output_variables.py``
     scripts from the |Rose| app.
  :Details:
     Runs once for each recipe,
     immediately after the successful completion
     of the ``install_env_file`` job.
     The recipe is updated with CMEW required variables
     (e.g. "Activity": "ESMVal")
     and also with user configurable variables
     from the |Rose Edit GUI|_/``rose-suite.conf``,
     for both model runs.
  :Families:
     ``RECIPE``

``configure_standardise``
  :Description:
     Creates the |CDDS| request metadata
     and variables list required to standardise two model development runs,
     then prepares the |CDDS| directory structure.
     If previously saved raw data is being used,
     the raw data will be symlinked to the this task's work directory.
  :Executes:
     The ``configure_standardise.sh`` script from the |Rose| app.
  :Details:
     Runs once for each recipe, immediately after the successful
     completion of the ``configure_for`` job.
     Generates |CDDS| request metadata for each model run (reference and evaluation):
     ``request_ref.json``, ``request_eval.json``.
     Generates a list of variables to standardise for each model run
     based on the lists of variables required for each recipe.
     Reads model-specific values from the workflow environment.
     Creates the required directory structure to support
     multiple |CDDS| standardisation workflows
     within the same |CMEW| cycle.

``standardise_model_data``
  :Description:
     Launches the CDDS workflow and converts both model runs into |CMIP|-compliant
     datasets suitable for |ESMValTool| evaluation.
     Saves new raw data if required.
  :Executes:
     The ``cdds_convert`` command and the ``restructure_dirs.sh`` script
     from the |Rose| app.
  :Details:
     Runs after the successful completion of the ``configure_standardise`` job.
     Executes |CDDS| standardisation for both the reference and evaluation model run
     to produces |CMIP|-compliant output for each.
     Uses ``restructure_dirs.sh`` to move standardised data into a BADC DRS structure.

``housekeeping``
  :Description:
     Removes any intermediate files from the cylc run directory that were
     created by the |CDDS| workflow in ``standardise_model_data``
  :Executes:
     The |rose_prune|_ application
  :Details:
     Runs after the successful completion of the ``standardise_model_data`` job

``run_evaluation_tool``
  :Description:
     Runs the evaluation tool
  :Executes:
     The |ESMValTool| command line script
  :Details:
     Runs once for each recipe,
     after the successful completion of the ``standardise_model_data``
     and the ``configure_recipe`` jobs.
  :Families:
     ``RECIPE``

``compare``
  :Description:
     Ensures the expected output files are generated
     by the ``run_evaluation_tool`` jobs
  :Executes:
     The ``compare.sh`` script from the |Rose| app
  :Details:
     Runs only in test mode (``-O test``)
     for the ESMValTool recipe ``radiation_budget``
     and the AutoAssess area ``monsoon``,
     after the completion of the ``run_evaluation_tool`` job

The |AutoAssess| assessments use the following steps:

``install_autoassess``
  :Description:
     Installs the |AutoAssess| code base locally so the workflow can make use of it
  :Executes:
     The ``install_package.sh`` script from the workflow ``bin`` directory
  :Details:
     Makes use of the |Rose| install capabilities to copy a specified commit of
     the |AutoAssess| repository to the workflow share directory. The script
     then runs a pip install command to create the required executables in the
     required location.

``retrieve_data<area><dataset>``
  :Description:
     Retrieves UM model data from MASS in PP format
  :Executes:
     The |AutoAssess| ``aa_retriever`` script from the ``aa_retrieve_data`` |Rose| app.
     There is an optional configuration for retrieving data for the Validation Note that
     uses the ``aa_mksuper`` script.
  :Details:
     This task runs on a per area and per dataset basis

``index_data<area><dataset>``
  :Description:
     Prepares the retrieved model data in a form that can be more quickly read by Iris
  :Executes:
     The |AutoAssess| ``aa_data_indexer`` script from the ``aa_index_data`` |Rose| app.
  :Details:
     This task runs on a per area and per dataset basis. There is an optional
     configuation for the Aerosols area to invoke the ``--ncconv`` option that
     forces conversion to netcdf before indexing.

``run_area<area>``
  :Description:
     Runs the |AutoAssess| area assessment
  :Executes:
     The |AutoAssess| ``aa_run_area`` script from the ``aa_run_area`` |Rose| app.
     Optional configurations exist for the Australia and MJO areas which run the
     ``aa_australia`` and ``aa_mjo`` |AutoAssess| scripts respectively. There
     is also an optional configuration for Validation Notes that uses the
     ``aa_mksource`` and ``aa_valnote`` scripts.
  :Details:
     This task runs on a per area basis.

``nac_plot<area>``
  :Description:
     Produces a Normalised Assessment Criteria (NAC) plot based on the calculated
     metrics in the ``run_area<area>`` task
  :Executes:
     The |AutoAssess| ``aa_create_nac_plots`` script from the ``aa_nac_plot`` |Rose| app.
     There is an optional configuration for the Validation Note that effectively skips
     this task as no NAC plots need to be produced.
  :Details:
     This task runs after the ``run_area<area>`` task on a per area basis. The
     inputs are csv files containing metric values generated from the
     ``run_area<area>`` task.

``html_page<area>``
  :Description:
     Produces an HTML page containing the results of the area assessment
  :Executes:
     The |AutoAssess| ``aa_create_page`` script from the ``aa_html_page`` |Rose| app.
     There is an optional configuration for the Validation Note that effectively skips
     this task as an html page does not need to be produced.
  :Details:
     This task runs on a per area basis, and runs after the ``nac_plot<area>``
     task. It uses a jinja2 template from the |AutoAssess| code base along with
     information on the assessment period and the datasets being assessed.

``html_page_overview``
  :Description:
     Produces an HTML page containing an overview of the area assessments that
     have been run
  :Executes:
     The |AutoAssess| ``aa_create_page`` script from the ``aa_html_page`` |Rose| app
  :Details:
     This task runs the ``template`` optional configuration for the app in order
     to use the specified jinja2 template file rather than the centrally held
     |AutoAssess| template files.

Design considerations
---------------------

Portability
~~~~~~~~~~~

|CMEW| is portable; site-specific information can be found in the ``site`` and
``opt`` directories within the workflow. The files required are:

``site/<site>.cylc``
  Contains task definitions specific to the ``SITE``

``site/<site>_autoassess.cylc``
  Contains task definitions specific for AutoAssess at the ``SITE``

``site/<site>-standardise-env``
  Contains details on how to set up the environment for CDDS at the ``SITE``

``site/<site>-esmvaltool-env``
  Contains details on how to set up the environment for ESMValTool at the
  ``SITE``

``opt/rose-suite-<site>.conf``
  Contains configuration items specific to the ``SITE``, including ``SITE``

Families
~~~~~~~~
Several tasks in |CMEW| are grouped into `families`_ with shared configurations.
The following families are used in the workflow:

``RECIPE``
  A family that is inherited by tasks that run
  for each recipe independently

Metadata
~~~~~~~~

|CMEW| uses Rose metadata. Every item defined in the suite configuration file
(``rose-suite.conf``) will have an entry in the main metadata configuration
file (``meta/rose-meta.conf``).

Resources
~~~~~~~~~

The resources used by the ``run_evaluation_tool`` jobs
are defined in the ``site/<site>.cylc`` file,
allowing the jobs to be configured by ``SITE`` as well as by recipe.
This ensures only the required resources are requested
when running each of the ``run_evaluation_tool`` jobs.
