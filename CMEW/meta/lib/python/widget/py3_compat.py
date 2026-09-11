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

try:
    from rose.config_editor.valuewidget.choice import ChoicesValueWidget
except ImportError:
    from metomi.rose.config_editor.valuewidget.choice import ChoicesValueWidget
