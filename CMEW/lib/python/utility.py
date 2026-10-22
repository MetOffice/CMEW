#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
Testing python interface
"""

def select_recipes(recipes: str, source_recipes: dict[str, str], tool: str) -> str:
    tool_recipes = [x for x in recipes.split(",") if source_recipes[x] == tool]
    print(f"Selected recipes for {tool} are {tool_recipes}")
    return ",".join(tool_recipes)
