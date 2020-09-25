from typing import Dict

import h5py

from .group import Group
from .law import Law


class Sequence(Group):
    _MANDATORY_DATASETS = [
        "MFMC_DATA",
        "PROBE_PLACEMENT_INDEX",
        "PROBE_POSITION",
        "PROBE_X_DIRECTION",
        "PROBE_Y_DIRECTION",
        "TRANSMIT_LAW",
        "RECEIVE_LAW",
        "PROBE_LIST",
    ]
    _MANDATORY_ATTRS = ["TYPE", "TIME_STEP", "START_TIME", "SPECIMEN_VELOCITY"]
    _OPTIONAL_DATASETS = ["MFMC_DATA_IM", "DAC_CURVE"]
    _OPTIONAL_ATTRS = [
        "WEDGE_VELOCITY",
        "TAG",
        "RECEIVER_AMPLIFIER_GAIN",
        "FILTER_TYPE",
        "FILTER_PARAMETERS",
        "FILTER_DESCRIPTION",
        "OPERATOR",
        "DATE_AND_TIME",
    ]

    def __init__(self, group: h5py.Group):
        """Representation of a sequence from a MFMC file.

        Args:
            group: The h5py group for the sequence.
        """
        self._group = group

        self._laws = {}
        for k, v in self._group.items():
            try:
                if v.attrs["TYPE"] == b"LAW":
                    self._laws[k] = Law(v)
            except KeyError:
                continue

    @property
    def laws(self) -> Dict[str, Law]:
        """List of law objects for the sequence."""
        return self._laws
