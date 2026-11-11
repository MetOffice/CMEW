# (C) Crown Copyright 2022-2026, Met Office.
# The LICENSE.md file contains full licensing details.
# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import sys
from pathlib import Path

sys.path.insert(0, str(Path("../../").resolve()))
from doc.source.common import GLOSSARY, LINKS  # noqa: E402

RST_EPILOG = f"{GLOSSARY}{LINKS}"

# -- Project information -----------------------------------------------------

project = "Climate Model Evaluation Workflow (CMEW)"
copyright = "Crown Copyright 2022-2026, Met Office"
author = "CMEW developers"
version = "0.2.0dev"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx_design",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

rst_epilog = RST_EPILOG

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#primary-sidebar-left
html_sidebars = {"index": ["sidebar-nav"]}
html_context = {
    "github_url": "https://github.com",
    "github_user": "MetOffice",
    "github_repo": "CMEW",
    "github_version": "main",
    "doc_path": "doc/source",
}
html_theme = "pydata_sphinx_theme"
html_theme_options = {
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#footer
    "footer_start": ["copyright", "last-updated"],
    "footer_end": ["sphinx-version", "theme-version"],
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/header-links.html#icon-links
    "icon_links": [
        {
            "name": "GitHub Discussions",
            "url": "https://github.com/MetOffice/CMEW/discussions",
            "icon": "fa fa-comments fa-fw",
        },
        {
            "name": "GitHub Issues",
            "url": "https://github.com/MetOffice/CMEW/issues",
            "icon": "fa-brands fa-square-github fa-fw",
        },
    ],
    "icon_links_label": "Quick Links",
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/branding.html#logo-title-and-alternative-text
    "logo": {
        "text": "CMEW",
    },
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#secondary-sidebar-right
    "secondary_sidebar_items": [
        "page-toc",
        "sourcelink",
        "support",
        "contribute",
    ],
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/navigation.html#control-how-many-navigation-levels-are-shown-by-default
    "show_nav_level": 1,
    # https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/source-buttons.html#add-an-edit-button
    "use_edit_page_button": True,
}
# https://pydata-sphinx-theme.readthedocs.io/en/stable/user_guide/layout.html#build-date
html_last_updated_fmt = ""

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Ignore the following URLs when running linkcheck.
linkcheck_ignore = [
    r"https://github.com/MetOffice/AutoAssess",
    r"https://github.com/MetOffice/CMEW.*",
    r"https://wcrp-cmip.org/",
]
