.. _recipes_valnote:

.. include:: ../../common.txt

Validation Note
===============

This recipe is available via |AutoAssess|.

Overview
--------

This is a generic assessment that can use a large number of model diagnostics and
compares two experiments with an appropriate observation for context. The general
diagnostic plot is a "4up" showing:

a. Reference field
b. Experiment - Reference difference
c. Reference - Observation difference
d. Experiment - Observation difference

If the model diagnostic does not lend itself to this format then other variations
plot can be used, see examples.


Available recipes and diagnostics
---------------------------------

The assessment code is available from the `AutoAssess`_ repository.


User settings in recipe
-----------------------

There are no user settings for this recipe


Variables
---------

Any available model diagnostic as either an annual or seasonal multi-annual mean.


Observations and reformat scripts
---------------------------------

A large number of observations are used for this assessment and are appropriate
for the model diagnostic being compared.


References
----------

There are no references for this assessment


Example plots
-------------

.. figure:: 0010_PMSL_djf_v_era-interim.png
   :scale: 50 %
   :alt: 0010_PMSL_djf_v_era-interim.png

   Comparison of PMSL to ERA-Interim

.. figure:: 0052_U_wind_djf_v_era-interim_logY.png
   :scale: 50 %
   :alt: 0052_U_wind_djf_v_era-interim_logY.png

   Comparison of zonal mean zonal wind to ERA-Interim using log(pressure) Y axis

.. figure:: 1860_Zonal_mean_zonal_wind_stress_djf_v_scatterometer.png
   :scale: 50 %
   :alt: 1860_Zonal_mean_zonal_wind_stress_djf_v_scatterometer.png

   Comparison of surface wind stress to scatterometer

.. figure:: 5000_Wbig_where_W_gt_1.png
   :scale: 50 %
   :alt: 5000_Wbig_where_W_gt_1.png

   Comparison of instances of vertical velocities > 1 ms-1
