from __future__ import annotations

import enum
from typing import Any, Literal, overload

import h5py

from mfmc import _group


class ElementShape(enum.IntEnum):
    RECTANGULAR = 1
    ELLIPTICAL = 2


class Probe(_group.Group):
    _MANDATORY_DATASETS = (
        "ELEMENT_POSITION",
        "ELEMENT_MINOR",
        "ELEMENT_MAJOR",
        "ELEMENT_SHAPE",
    )
    _MANDATORY_ATTRS = ("TYPE", "CENTRE_FREQUENCY")
    _OPTIONAL_DATASETS = (
        "ELEMENT_RADIUS_OF_CURVATURE",
        "ELEMENT_AXIS_OF_CURVATURE",
        "DEAD_ELEMENT",
    )
    _OPTIONAL_ATTRS = (
        "WEDGE_SURFACE_POINT",
        "WEDGE_SURFACE_NORMAL",
        "BANDWIDTH",
        "PROBE_MANUFACTURER",
        "PROBE_SERIAL_NUMBER",
        "PROBE_TAG",
        "WEDGE_MANUFACTURER",
        "WEDGE_SERIAL_NUMBER",
        "WEDGE_TAG",
    )

    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a probe from a MFMC file.

        Args:
            grp: The h5py group for the probe.
        """
        self._group = grp

    @overload
    def __getitem__(self, item: Literal["element_shape"]) -> tuple[ElementShape]: ...

    @overload
    def __getitem__(self, item: str) -> Any: ...

    def __getitem__(self, item):
        if item.upper() == "ELEMENT_SHAPE":
            return tuple(ElementShape(e) for e in self._group["ELEMENT_SHAPE"])
        if item.upper() == "DEAD_ELEMENT":
            return tuple(bool(e) for e in self._group["DEAD_ELEMENT"])
        else:
            return super().__getitem__(item)
