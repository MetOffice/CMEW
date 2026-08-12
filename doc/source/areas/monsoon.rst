.. _recipes_monsoon:

Monsoon
=======

Overview
--------

This diagnostic analyses the South and and East Asian monsoon.


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

Fixed Variables:

* sftlf (atmos, fixed, longitude latitude)

Daily Mean Variables:

* pr (atmos, daily mean, longitude latitude time)
* ua (850) (atmos, daily mean, longitude latitude time)
* va (850) (atmos, daily mean, longitude latitude time)

Monthly Mean Variables:

* pr (atmos, monthly mean, longitude latitude time)
* ua (850, 200) (atmos, monthly mean, longitude latitude plev time)
* va (850, 200) (atmos, monthly mean, longitude latitude plev time)
* psl (atmos, monthly mean, longitude latitude time)
* tas (atmos, monthly mean, longitude latitude time)
* uas (atmos, monthly mean, longitude latitude time)
* "Column integrated u*q" (atmos, monthly mean, longitude latitude time)

Seasonal Mean Variables:

* pr (atmos, seasonal mean, longitude latitude time)
* ua (850, 300, 200) (atmos, seasonal mean, longitude latitude plev time)
* va (850, 300, 200) (atmos, seasonal mean, longitude latitude plev time)
* zg (850, 500) (atmos, seasonal mean, longitude latitude plev time)
* psl (atmos, seasonal mean, longitude latitude time)
* tas (atmos, seasonal mean, longitude latitude time)
* uas (atmos, seasonal mean, longitude latitude time)


Observations and reformat scripts
---------------------------------

*Note: (1) obs4MIPs data can be used directly without any preprocessing;
(2) see headers of reformat scripts for non-obs4MIPs data for download
instructions.*

* ECMWF Reanalysis (ERA-Interim?) (psl, ua, va, uas, zg)
* Climate Research Unit (CRU-TS 3.23? tmp) (tas)
* GPCP (vn2.2?) (pr)

  *Reformat script:* <myreformatscript.py>

References
----------

Example plots
-------------
