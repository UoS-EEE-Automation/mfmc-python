from typing import Any, Literal, overload

import h5py

from mfmc.read import _group, probe


class Law(_group.Group):
    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a law which belongs to a sequence.

        Args:
            grp: The h5py group for the law.
        """
        super().__init__()
        self._group = grp

    @overload
    def __getitem__(
        self, key: Literal["probe", "PROBE"]
    ) -> tuple[probe.Probe, ...]: ...

    @overload
    def __getitem__(self, key: str) -> Any: ...

    def __getitem__(self, key):
        if key.upper() == "PROBE":
            return tuple(probe.Probe(p) for p in self._group["PROBE"])

        return super().__getitem__(key)
