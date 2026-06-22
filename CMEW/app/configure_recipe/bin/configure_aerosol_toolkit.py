#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import os
from pathlib import Path

aerosol_driver_example_fp = f"{os.environ["CYLC_WORKFLOW_RUN_DIR"]}/lib/python/aerosol_evaluation_toolkit/namelists/namelist_aerosol_evaluation_toolkit_EXAMPLE.py"
place_to_copy_example_to = f"{os.environ["CYLC_WORKFLOW_SHARE_DIR"]}/etc/aerosol_configuration.py"

command = f"""
    cp {aerosol_driver_example_fp} {place_to_copy_example_to}
    """

with open(place_to_copy_example_to, "r") as f:
    content = f.read()
print(content)

# aerosol_sh_fp = f"{os.environ["CYLC_WORKFLOW_RUN_DIR"]}/lib/python/aerosol_evaluation_toolkit/DRIVER_aerosol_evaluation_toolkit_azure_spice.sh"
# string_to_replace_in_sh_file = "../../namelists/namelist_aerosol_evaluation_toolkit_target.py"
#
# with open(aerosol_sh_fp, "r") as aerosol_sh_file:
#     aerosol_sh_content = aerosol_sh_file.read()
# aerosol_sh_content.replace(string_to_replace_in_sh_file, place_to_copy_example_to)
# with open(aerosol_sh_fp, "w") as aerosol_sh_file:
#     aerosol_sh_file.write(aerosol_sh_content)
#
# dir_to_be_in = Path(aerosol_sh_fp).parent
#
# command = f"""
#     cd {dir_to_be_in}
#     sbatch {aerosol_sh_fp}
#     """
