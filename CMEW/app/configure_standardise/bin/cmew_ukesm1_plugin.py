"""UKESM1 mappings for CMEW's Amon wind extraction."""

from mip_convert.configuration.python_config import ModelToMIPMappingConfig
from mip_convert.plugins.ukesm1 import ukesm1_plugin


class CMEWUKESM1MappingPlugin(ukesm1_plugin.UKESM1MappingPlugin):
    """Enable extraction of the internal Amon/ua mapping."""

    def load_model_to_mip_mapping(
        self, mip_table_name: str
    ) -> ModelToMIPMappingConfig:
        """Load UKESM1 mappings with Amon/ua available for extraction."""
        mappings = super().load_model_to_mip_mapping(mip_table_name)
        if mip_table_name.casefold() in {
            "gcmodeldev_amon",
            "gcmodeldev_ga7mon",
        }:
            mappings.read(
                {
                    "ua": {
                        # Override the default mapping for 'ua' to extract
                        # data from MASS that is on 17 pressure levels
                        # (PLEV17), and has been sampled at 6-hourly intervals
                        # (lbtim_ia=6).
                        "status": "ok",
                        "dimension": "longitude latitude plev17 time",
                        "expression": (
                            "(m01s30i201[blev=PLEV17, lbproc=128, "
                            "lbtim_ia=6] / "
                            "m01s30i301[blev=PLEV17, lbproc=128, "
                            "lbtim_ia=6])"
                        ),
                    }
                }
            )
        return mappings
