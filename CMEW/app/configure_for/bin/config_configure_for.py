#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.

# Information about the locations of specific ESMValTool recipes.
recipes_dict = {
    "correlation": {
        "recipe_name": "recipe_correlation.yml",
        "recipe_fp": "examples/recipe_correlation.yml",
        "empty_additional_datasets": True,
    },
    "python": {
        "recipe_name": "recipe_python.yml",
        "recipe_fp": "examples/recipe_python.yml",
    },
    "ref_cre": {
        "recipe_name": "recipe_ref_cre.yml",
        "recipe_fp": "ref/recipe_ref_cre.yml",
    },
}
