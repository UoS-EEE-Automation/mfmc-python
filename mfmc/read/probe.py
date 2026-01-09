from __future__ import annotations

import enum
from typing import Any, Literal, cast, overload

import h5py
import numpy as np
from numpy import typing as npt

from mfmc.read import _group


class ElementShape(enum.IntEnum):
    RECTANGULAR = 1
    ELLIPTICAL = 2


class Probe(_group.Group):
    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a probe from a MFMC file.

        Args:
            grp: The h5py group for the probe.
        """
        super().__init__()
        self._group = grp

    @overload
    def __getitem__(
        self, item: Literal["element_shape", "ELEMENT_SHAPE"]
    ) -> tuple[ElementShape, ...]: ...

    @overload
    def __getitem__(
        self, item: Literal["dead_element", "DEAD_ELEMENT"]
    ) -> tuple[bool, ...]: ...

    @overload
    def __getitem__(self, item: str) -> Any: ...

    def __getitem__(self, item: str):
        if item.upper() == "ELEMENT_SHAPE":
            return tuple(
                ElementShape(s) for s in cast(h5py.Group, self._group["ELEMENT_SHAPE"])
            )
        if item.upper() == "DEAD_ELEMENT":
            return tuple(bool(e) for e in cast(h5py.Group, self._group["DEAD_ELEMENT"]))
        else:
            return super().__getitem__(item)

    def ultrasound_direction(self) -> npt.NDArray[np.floating]:
        if "element_radius_of_curvature" in self:
            if "element_axis_of_curvature" in self:
                raise NotImplementedError("TODO: sphere")
            else:
                raise NotImplementedError("TODO: cylinder")

        return self["element_major"] @ self["element_minor"]
