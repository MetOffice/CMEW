#!/bin/bash
# (C) Crown Copyright 2022-2025, Met Office.
# The LICENSE.md file contains full licensing details.
#
# USAGE configure_for.sh
#
# ENVIRONMENT
#   RECIPE_NAME             : Name of recipe for ESMValTool
#   RECIPE_PATH             : Path of test recipe file
#   RECIPE_PATH_REFERENCE   : Path of reference recipe file
#   VARIANT_LABEL           : Variant label of test model
#   VARIANT_LABEL_REFERENCE : Variant label of reference model

# Send the output from 'set -x' to 'stdout' rather than 'stderr'.
BASH_XTRACEFD=1
set -eux

cmew-process-env esmvaltool recipes get "${RECIPE_NAME}"
mv "${RECIPE_NAME}" "${RECIPE_PATH}"
cp "${RECIPE_PATH}" "${RECIPE_PATH_REFERENCE}"
update_recipe_file.py -p "${RECIPE_PATH}" -v "${VARIANT_LABEL}"
update_recipe_file.py -p "${RECIPE_PATH_REFERENCE}" -v "${VARIANT_LABEL_REFERENCE}"
