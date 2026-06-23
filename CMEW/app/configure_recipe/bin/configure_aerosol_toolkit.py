#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os
from pathlib import Path
import subprocess

from CMEW.app.unittest.tests.test_scrape_ini import scrape_ini

aerosol_driver_example_fp = f"{os.environ['CYLC_WORKFLOW_RUN_DIR']}/lib/python/aerosol_evaluation_toolkit/namelists/namelist_aerosol_evaluation_toolkit_EXAMPLE.py"
place_to_copy_example_to = f"{os.environ['CYLC_WORKFLOW_SHARE_DIR']}/etc/aerosol_configuration.py"

command = f"""
    mkdir -p {Path(place_to_copy_example_to).parent}
    cp {aerosol_driver_example_fp} {place_to_copy_example_to}
    """

subprocess.run(command, shell=True)

with open(place_to_copy_example_to, "r") as f:
    content = f.read()
print(content)

new_content = f"""
def run_namelist():
    namelist_outputs = dict()
    namelist_outputs['suite_ids'] = [{scrape_ini.list_datasets(f"{os.environ['CYLC_WORKFLOW_RUN_DIR']}/rose-suite.conf")}]
    namelist_outputs['model_paths'] = []
    namelist_outputs['github_root_path'] = [{f"{os.environ['CYLC_WORKFLOW_RUN_DIR']}/lib/python"}]
    namelist_outputs['root_plot_path'] = [{f"{os.environ['CYLC_TASK_SHARE_CYCLE_DIR']}/aerosol_toolkit"}]
    namelist_outputs['merged_figure_filename'] = ['merged.pdf']
    namelist_outputs['model_version'] = ['made_up_model_name_1','made_up_model_name_2']
    namelist_outputs['model_years'] = [['1993'],['1994']]
    namelist_outputs['observation_years'] = ['1993','1994']
    namelist_outputs['comparison_type'] = ['model_model']
    namelist_outputs['free_or_nudged'] = ['free','free']
    namelist_outputs['l_average_obs_years'] = [False,True]
    namelist_outputs['l_average_model_years'] = [False,False]
    namelist_outputs['i_mode_setup'] = ['2','2']
    namelist_outputs['seasonal_only'] = ['T']
    namelist_outputs['l_N50_augment'] = ['T']
    return (namelist_outputs)
"""

with open(place_to_copy_example_to, "w") as f:
    f.write(new_content)

aerosol_sh_fp = f"{os.environ['CYLC_WORKFLOW_RUN_DIR']}/lib/python/aerosol_evaluation_toolkit/DRIVER_aerosol_evaluation_toolkit_azure_spice.sh"
string_to_replace_in_sh_file = "../../namelists/namelist_aerosol_evaluation_toolkit_target.py"

with open(aerosol_sh_fp, "r") as aerosol_sh_file:
    aerosol_sh_content = aerosol_sh_file.read()
aerosol_sh_content.replace(string_to_replace_in_sh_file, place_to_copy_example_to)
with open(aerosol_sh_fp, "w") as aerosol_sh_file:
    aerosol_sh_file.write(aerosol_sh_content)

dir_to_be_in = Path(aerosol_sh_fp).parent

command = f"""
    cd {dir_to_be_in}
    sbatch {aerosol_sh_fp}
    """
