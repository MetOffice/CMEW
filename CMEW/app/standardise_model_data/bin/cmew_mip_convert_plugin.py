#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
"""
CMEW-owned external mip_convert mapping plugin for the annual ``ony``
standardisation route.

CDDS 4.0.0's installed HadGEM3 model-to-MIP mapping config restricts
``tos``/``sos``/``thetao``/``so`` to ``mip_table_id = Oday Omon OPmon
OPday``, excluding ``Oyr``. Rather than modifying the shared CDDS
installation, this plugin subclasses the installed ``HadGEM3MappingPlugin``
and widens only those four mappings to also support ``Oyr``, reusing all
other HadGEM3 mappings unchanged. It is loaded by standalone ``mip_convert``
via the ``mip_convert_external_plugin``/``mip_convert_external_plugin_location``
cfg options -- no change to the installed mip_convert package is required.
"""
from mip_convert.plugins.hadgem3.hadgem3_plugin import HadGEM3MappingPlugin

ANNUAL_VARIABLES = ["tos", "sos", "thetao", "so"]
PLUGIN_ID = "CMEWGCModelDevAnnual"


class CMEWAnnualOceanMappingPlugin(HadGEM3MappingPlugin):
    """Extends HadGEM3's mappings to support Oyr for annual ocean variables."""

    def is_responsible(self, plugin_id):
        # Match our own plugin_id here, but leave self._plugin_id as
        # "HadGEM3" (set by the parent class) so the inherited
        # load_model_to_mip_mapping() still finds the installed
        # HadGEM3_*_mappings.cfg files.
        return plugin_id == PLUGIN_ID

    def load_model_to_mip_mapping(self, mip_table_name):
        mapping_config = super().load_model_to_mip_mapping(mip_table_name)
        for var_name in ANNUAL_VARIABLES:
            if mapping_config.config.has_section(var_name):
                current = mapping_config.config.get(var_name, "mip_table_id")
                if "Oyr" not in current.split():
                    mapping_config.config.set(
                        var_name, "mip_table_id", current + " Oyr"
                    )
        return mapping_config
