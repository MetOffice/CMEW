.. _recipes_africa:

.. include:: ../../common.txt

Africa
======

This recipe is available via |AutoAssess|.

Overview
--------

This diagnostic analyses African Easterly Waves (AEW) during the months May to September.

(Possibly West African Monsoon?)


Available recipes and diagnostics
---------------------------------

The assessment code is available from the `AutoAssess`_ repository.


User settings in recipe
-----------------------

There are no user settings for this recipe


Variables
---------

* pr (atmos, daily mean, longitude latitude time)
* ua (700) (atmos, daily mean, longitude latitude time)
* va (700) (atmos, daily mean, longitude latitude time)


Observations and reformat scripts
---------------------------------

* ECMWF Reanalysis (ERA-Interim?) (ua, va)
* MERRA (ua, va)


References
----------

Bain, C.L., K. Williams, S. Milton, J. Heming (2013):
Tracking African Easterly Waves in Met Office models
QJRMS


Example plots
-------------

.. figure:: africa_overview.png
   :align: center
   :scale: 50 %
   :alt: NAC plot for Africa area

   Summary overview of metrics from the Africa assessment

.. figure:: AEWstats.png
   :align: center
   :scale: 50 %
   :alt: AEWstats.png

   Statistics of various aspects of African Easterly Waves

.. figure:: raincoupling.png
   :align: center
   :scale: 50 %
   :alt: raincoupling.png

   Coupling between AEWs and rainfall

.. figure:: egAEWhov.png
   :align: center
   :scale: 50 %
   :alt: egAEWhov.png

   Hovmoller of curvature vorticity overlaid with AEW tracks

.. figure:: egAEWRAINhov.png
   :align: center
   :scale: 50 %
   :alt: egAEWRAINhov.png

   Hovmoller of rainfall overlaid with AEW tracks
