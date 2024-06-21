from typing import Any, Literal, overload

import h5py

from mfmc import _group, _probe


class Law(_group.Group):
    _MANDATORY_DATASETS = ("PROBE", "ELEMENT")
    _MANDATORY_ATTRS = ("TYPE",)
    _OPTIONAL_DATASETS = ("DELAY", "WEIGHTING")
    _OPTIONAL_ATTRS = ()

    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a law which belongs to a sequence.

        Args:
            grp: The h5py group for the law.
        """
        self._group = grp

    @overload
    def __getitem__(self, key: Literal["probe"]) -> tuple[_probe.Probe]: ...

    def __getitem__(self, key: str) -> Any:
        if key.upper() == "PROBE":
            return tuple(_probe.Probe(p) for p in self._group["PROBE"])

        return super().__getitem__(key)
