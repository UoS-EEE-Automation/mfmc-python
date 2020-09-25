import h5py

from .group import Group


class Probe(Group):
    _MANDATORY_DATASETS = [
        "ELEMENT_POSITION",
        "ELEMENT_MINOR",
        "ELEMENT_MAJOR",
        "ELEMENT_SHAPE",
    ]
    _MANDATORY_ATTRS = ["TYPE", "CENTRE_FREQUENCY"]
    _OPTIONAL_DATASETS = [
        "ELEMENT_RADIUS_OF_CURVATURE",
        "ELEMENT_AXIS_OF_CURVATURE",
        "DEAD_ELEMENT",
    ]
    _OPTIONAL_ATTRS = [
        "WEDGE_SURFACE_POINT",
        "WEDGE_SURFACE_NORMAL",
        "BANDWIDTH",
        "PROBE_MANUFACTURER",
        "PROBE_SERIAL_NUMBER",
        "PROBE_TAG",
        "WEDGE_MANUFACTURER",
        "WEDGE_SERIAL_NUMBER",
        "WEDGE_TAG",
    ]

    def __init__(self, group: h5py.Group) -> None:
        """Representation of a probe from a MFMC file.

        Args:
            group: The h5py group for the probe.
        """
        self._group = group
