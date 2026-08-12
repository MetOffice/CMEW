.. _recipes_africa:

Africa
======

Overview
--------

This diagnostic analyses African Easterly Waves (AEW) during the months May to September.

(Possibly West African Monsoon?)


Available recipes and diagnostics
---------------------------------

Recipes are stored in esmvaltool/recipes/

* recipe_<mynewrecipe>.yml

Diagnostics are stored in esmvaltool/diag_scripts/<mynewdiag>/

* <mynewdiag.py/.ncl/.r>: one line scription


User settings in recipe
-----------------------

#. Script <mynewdiag.py/.ncl/.r>

   *Required settings for script*

   * xxx: zzz

   *Optional settings for script*

   *Required settings for variables*

   *Optional settings for variables*

   *Required settings for preprocessor*

   *Optional settings for preprocessor*

   *Color tables*

   * list required color tables (if any) here


Variables
---------

* pr (atmos, daily mean, longitude latitude time)
* ua (700) (atmos, daily mean, longitude latitude time)
* va (700) (atmos, daily mean, longitude latitude time)


Observations and reformat scripts
---------------------------------

*Note: (1) obs4MIPs data can be used directly without any preprocessing;
(2) see headers of reformat scripts for non-obs4MIPs data for download
instructions.*

* ECMWF Reanalysis (ERA-Interim?) (ua, va)
* MERRA (ua, va)

  *Reformat script:* <myreformatscript.py>

References
----------

Bain, C.L., K. Williams, S. Milton, J. Heming (2013): 
Tracking African Easterly Waves in Met Office models 
QJRMS

Example plots
-------------
