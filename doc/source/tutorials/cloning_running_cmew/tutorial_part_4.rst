.. (C) Crown Copyright 2026, Met Office.
.. The LICENSE.md file contains full licensing details.

=========================
Start the |CMEW| workflow
=========================

Now we have configured |CMEW|, we are ready to set the workflow running.

------------------------------
1) Save and close the Rose GUI
------------------------------

Click the X in the top right of the Rose GUI to close the window.
A pop-up will appear asking whether to save the changes.
**Click the button that says "Yes"**,
this is the rightmost button.

-------------------------------
2) Use Cylc to run the workflow
-------------------------------

Using our terminal window from earlier in the tutorial,
we will confirm that we are still in the directory containing the ``flow.cylc`` file::

    pwd

This will return the value ``<your home directory>/cmew_tutorial/CMEW``.

In the same terminal, type the command::

    cylc vip -O metoffice

This will print messages from cylc about validating and installing the workflow,
and some ``[INFO]`` about the workflow.

Congratulations, we have now set the |CMEW| workflow running.
