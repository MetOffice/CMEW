#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.
import pytest

cmew_mip_convert_plugin = pytest.importorskip(
    "cmew_mip_convert_plugin",
    reason="mip_convert (from the CDDS environment) is not available here",
)


def test_is_responsible_matches_custom_plugin_id():
    plugin = cmew_mip_convert_plugin.CMEWAnnualOceanMappingPlugin()
    assert plugin.is_responsible(cmew_mip_convert_plugin.PLUGIN_ID)
    assert not plugin.is_responsible("HadGEM3")


def test_plugin_id_left_as_hadgem3_for_mapping_file_lookup():
    plugin = cmew_mip_convert_plugin.CMEWAnnualOceanMappingPlugin()
    # The inherited load_model_to_mip_mapping() looks up mapping files by
    # self._plugin_id, so this must remain "HadGEM3", not our custom id.
    assert plugin._plugin_id == "HadGEM3"


def test_load_model_to_mip_mapping_adds_oyr_to_annual_variables():
    plugin = cmew_mip_convert_plugin.CMEWAnnualOceanMappingPlugin()
    mapping_config = plugin.load_model_to_mip_mapping("GCModelDev_Oyr")

    for var_name in cmew_mip_convert_plugin.ANNUAL_VARIABLES:
        mip_table_ids = mapping_config.config.get(
            var_name, "mip_table_id"
        ).split()
        assert "Oyr" in mip_table_ids


def test_load_model_to_mip_mapping_preserves_existing_mip_table_ids():
    plugin = cmew_mip_convert_plugin.CMEWAnnualOceanMappingPlugin()
    mapping_config = plugin.load_model_to_mip_mapping("GCModelDev_Omon")

    tos_mip_table_ids = mapping_config.config.get(
        "tos", "mip_table_id"
    ).split()
    for original in ("Oday", "Omon", "OPmon", "OPday"):
        assert original in tos_mip_table_ids
