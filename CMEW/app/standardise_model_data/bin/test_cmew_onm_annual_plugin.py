#!/usr/bin/env python
# (C) Crown Copyright 2026, Met Office.
# The LICENSE.md file contains full licensing details.

import cmew_onm_annual_plugin


def test_plugin_responsibility():
    plugin = cmew_onm_annual_plugin.CMEWOnmAnnualMappingPlugin()

    assert plugin.is_responsible(cmew_onm_annual_plugin.PLUGIN_ID)
    assert not plugin.is_responsible("GCModelDev")


def test_annual_expressions():
    assert cmew_onm_annual_plugin.ANNUAL_EXPRESSIONS == {
        "tos": "annual_from_monthly_2d(tos)",
        "sos": "annual_from_monthly_2d(sos)",
        "thetao": "annual_from_monthly_3d(thetao, thkcello)",
        "so": "annual_from_monthly_3d(so, thkcello)",
    }


def test_loaded_mapping_adds_oyr_and_annual_expressions():
    plugin = cmew_onm_annual_plugin.CMEWOnmAnnualMappingPlugin()

    mapping = plugin.load_model_to_mip_mapping("GCModelDev_Oyr")

    expected = {
        "tos": "annual_from_monthly_2d(tos)",
        "sos": "annual_from_monthly_2d(sos)",
        "thetao": "annual_from_monthly_3d(thetao, thkcello)",
        "so": "annual_from_monthly_3d(so, thkcello)",
    }

    for variable, expression in expected.items():
        assert mapping.value(variable, "expression", str) == expression

        mip_tables = mapping.value(
            variable,
            "mip_table_id",
            str,
        ).split()
        assert "Oyr" in mip_tables
