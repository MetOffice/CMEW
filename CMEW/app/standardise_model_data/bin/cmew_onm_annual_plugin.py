#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
CMEW-owned mip_convert mapping plugin for annualising monthly NEMO ``onm``
data to ``Oyr``.

This leaves the shared mip_convert/CDDS installation unchanged.  It
inherits the installed HadGEM3 mappings and overrides only the four ocean
variables required by the CMEW annual ocean diagnostic.
"""

from mip_convert.plugins.hadgem3.hadgem3_plugin import HadGEM3MappingPlugin


PLUGIN_ID = "CMEWGCModelDevOnmAnnual"

ANNUAL_EXPRESSIONS = {
    "tos": "annual_from_monthly_2d(tos)",
    "sos": "annual_from_monthly_2d(sos)",
    "thetao": "annual_from_monthly_3d(thetao, thkcello)",
    "so": "annual_from_monthly_3d(so, thkcello)",
}


class CMEWOnmAnnualMappingPlugin(HadGEM3MappingPlugin):
    """Annualise monthly ocean data using mip_convert processors."""

    def is_responsible(self, plugin_id):
        return plugin_id == PLUGIN_ID

    def load_model_to_mip_mapping(self, mip_table_name):
        mapping_config = super().load_model_to_mip_mapping(mip_table_name)

        for var_name, expression in ANNUAL_EXPRESSIONS.items():
            if not mapping_config.config.has_section(var_name):
                raise ValueError(
                    "No installed HadGEM3 mapping found for {!r}".format(
                        var_name
                    )
                )

            mapping_config.config.set(
                var_name,
                "expression",
                expression,
            )

            current_tables = mapping_config.config.get(
                var_name,
                "mip_table_id",
            )
            if "Oyr" not in current_tables.split():
                mapping_config.config.set(
                    var_name,
                    "mip_table_id",
                    current_tables + " Oyr",
                )

        return mapping_config
