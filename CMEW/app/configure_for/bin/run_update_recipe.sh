#!/usr/bin/env bash
set -euxo pipefail

# Wrapper to fetch, locate, move and update the ESMValTool recipe for the configure_for
# Rose app. Uses environment variables provided by Cylc/Rose (e.g. CYLC_TASK_PARAM_recipe,
# RECIPE_PATH, RECIPE_DICT_PATH, DATASETS_LIST_DIR, RECIPE_VARIABLES_PATH).

ESMVALTOOL_RECIPE_PATH=$(cmew-esmvaltool-env esmvaltool recipes list | grep "$CYLC_TASK_PARAM_recipe" | tail -n 1 | sed "s/^ • //" | sed 's/:.*$//') || true
cmew-esmvaltool-env esmvaltool recipes get "$ESMVALTOOL_RECIPE_PATH"
pwd
ESMVALTOOL_RECIPE_NAME=${ESMVALTOOL_RECIPE_PATH##*/}

mkdir -p "$(dirname $RECIPE_PATH)"

# ESMVALTOOL_RECIPE_SRC=$(find . -maxdepth 4 -type f -name "$ESMVALTOOL_RECIPE_NAME" -print -quit || true)

# test -n "$ESMVALTOOL_RECIPE_SRC" || { echo "Recipe source not found" >&2; exit 1; }
mv "$ESMVALTOOL_RECIPE_NAME" "$RECIPE_PATH"
ls -l "$RECIPE_PATH"

cmew-esmvaltool-env update_recipe_file \
  --recipe_path "$RECIPE_PATH" \
  --model_runs_yml_fp "${DATASETS_LIST_DIR}/model_runs.yml" \
  --cmip6_datasets_yml_fp "${DATASETS_LIST_DIR}/cmip6_datasets.yml" \
  --recipe_id "$CYLC_TASK_PARAM_recipe" \
  --recipe_dict_fp "$RECIPE_DICT_PATH"

cmew-esmvaltool-env get_variables_from_recipe \
  --recipe_path "$RECIPE_PATH" \
  --output_filepath "$RECIPE_VARIABLES_PATH"
