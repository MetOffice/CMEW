# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
This module contains a wrapper around rose.config_editor widgets to allow
python3 compatability.

The basic construct here is for each rose widget

try:
    import python2 widget
except ImportError:
    import python3 widget

"""

import os
import sys

print(sys.path)
print(os.listdir("/home/runner/micromamba/envs/cmew-env/lib/python3.14/site-packages"))
print(os.listdir("/home/runner/micromamba/envs/cmew-env/lib/python3.14/site-packages/metomi"))
print(os.listdir("/home/runner/micromamba/envs/cmew-env/lib/python3.14/site-packages/metomi/rose"))


try:
    from rose.config_editor.valuewidget.choice import ChoicesValueWidget
except ImportError:
    print("Cannot import from rose.config_editor")

try:
    from metomi.rose.config_editor.valuewidget.choice import ChoicesValueWidget
except ImportError:
    print("Cannot import from metomi.rose.config_editor")

sys.exit(1)
