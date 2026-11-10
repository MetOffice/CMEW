.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

**********************************
Evaluating a model run with |CMEW|
**********************************

-------------------------------------------------------------------------------------------------
Comparing the radiation budget and monsoon assessment areas of a GC5 model run to a GC3 model run
-------------------------------------------------------------------------------------------------

.. include:: ../common.txt

In this tutorial,
we will put a copy of the |CMEW| workflow onto our local machine
and use it to compare model run **u-cw673** to model run **u-bv546**
with regards to radiation budget and monsoon metrics.


0. Prerequisites
----------------

a) SSH access to GitHub
b) ``moo hello``

1. Clone the |CMEW| repository from GitHub
------------------------------------------

In this section, we will copy |CMEW| from GitHub
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


2. Configure the datasets for our |CMEW| run
--------------------------------------------

|CMEW| is set up to take a reference (control) model run,
and compare an evaluation (experiment) run to this reference.

In this section, we will use the default control run,
but replace the experiment run with a new dataset.

**a) Navigate to the directory containing the** ``rose-suite.conf`` **file**

All of the code and configuration relating to the workflow is in the directory ``CMEW``.
Navigate to the directory ``CMEW``::

    cd CMEW
    ls

We can confirm that files listed include ``flow.cylc`` and ``rose-suite.conf``.

**b) Configure the workflow**

This is done using the Rose GUI.
Open the Rose GUI::

    rose edit

Now we will use the GUI to change some options.

**i) Change the number of years**

Some |CMEW| assessment areas require a minimum of five years' of data to run.
For this tutorial, we will pick areas that only need two years' worth of data to run.
In order to make our tutorial run quicker, we will reduce the number of years to 2.

In the GUI we need to click
 - the arrow next to **suite conf**, then
 - the arrow next to **Options**, then
 - the section labelled **Required**, then
 - the down arrow, until **2** is displayed.

.. image:: images/amending_number_of_years.png
   :alt: An image of the Rose GUI showing the "suite conf",
         with the "Options" section expanded,
         the "Required" section selected,
         and a "2" next to variable NUMBER_OF_YEARS.
   :width: 600px

**ii) Change the experiment dataset details**

A typical |CMEW| user should already know what model run they would like to assess.
For the purposes of this tutorial,
we are going to evaluate model run ``u-cw673``.
Information about this model run can be found at the following address:
https://code.metoffice.gov.uk/trac/roses-u/browser/c/w/6/7/3/trunk/rose-suite.info

Here is a copy of the information, for ease of reference:

.. image:: images/u-cw673_suite_info.png
   :alt: An image of the Rose GUI showing the "suite conf",
         with the "Datasets" section expanded,
         the "Model runs to assess" section selected,
         and a pop-up menu over the "experiment" entry.
   :width: 600px

Now in the GUI we need to click
 - the arrow next to **Datasets**, then
 - the arrow next to **Model runs to assess**, then
 - the section labelled **experiment**.

.. image:: images/editing_experiment_dataset.png
   :alt: An image of a webpage showing the following lines of code:
         1	awarning=FOR MET OFFICE AND MONSOON USERS ONLY:
         2	        =
         3	        =**** THIS SUITE WILL ARCHIVE NON-DUPLEXED DATA TO MOOSE.
         4	        =FOR CRITICAL MODEL RUNS SWITCH TO DUPLEXED IN:
         5	        =postproc --> Post Processing - common settings --> Moose Archiving --> non_duplexed_set
         6	        =Follow guidance in http://www-twiki/Main/MassNonDuplexPolicy
         7	description=Copy of u-cw653/trunk@256293
         8	owner=dancopsey
         9	project=Coupled Climate
         10	title=GC5 N96 ORCA1 UM13.1 YR2000 pesent day control run
   :width: 600px

Overwrite the experiment dataset with the following details:

**suite_id**

This is the main identifier of the model run to assess,
informing where the data on MASS will be extracted from.

*Enter the value*
 - ``u-cw673``

**label_for_plots**

This is a short description of the model run,
for example you might describe the parametrization changes.

*Enter the value*
 - ``CMEW tutorial model run``

**model_configuration**

Line 10 of the information about the model run starts ``title=GC5 ...``.

*Select the option*
 - ``"GC5"``

**resolution**

Line 10 of the information about the model run continues ``... N96 ORCA1 ...``.
By clicking the help button for resolution,
we can see that this counts as low resolution data.

.. image:: images/resolution_help_button.png
   :alt: An image of a Rose GUI help page, displaying the following text:
         This is used to determine a model ID.
         N96 ORCA1 is low resolution.
         N215 ORCA025 is medium resolution.
   :width: 800px

*Select the option*
 - ``"low"``

**calendar**

I THINK WE SHOULD HIDE ALL THE FOLLOWING DETAILS:
``moo_ppfp -tim :/crum/u-cw673/apm.pp/cw673a.pm1993jan.pp``
12**1** means Gregorian.

*Select the option*
 - ``"gregorian"``
