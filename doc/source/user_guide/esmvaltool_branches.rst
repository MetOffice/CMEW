.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

Using a branch of ESMValTool
============================

.. include:: ../common.txt


Branches
--------

By default, |CMEW| will use a released version of ESMValTool such as v.2.13.0.

There may be circumstances where it is desirable instead to use a different branch, for example,
a CMEW user may have their own recipes and diagnostic scripts available in a branch of ESMValTool,
or they may wish to use a new diagnostic which is in main but not yet in a release.

This functionality is controlled by two variables in the `rose-suite.conf` file.
e.g. to use the branch "main" one would set the following::

    USE_ESMVALTOOL_BRANCH=true
    ESMVALTOOL_BRANCH="main"
