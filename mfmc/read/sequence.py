from __future__ import annotations

import datetime
import enum
import functools
from collections.abc import Iterator

from typing import Any, Literal, overload

import h5py
import numpy as np

from mfmc import _exceptions
from mfmc.read import _group, _types, law, probe


class FilterType(enum.IntEnum):
    NONE = 0
    LOW_PASS = 1
    HIGH_PASS = 2
    BAND_PASS = 3
    OTHER = 4


class Sequence(_group.Group):
    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a sequence from a MFMC file.

        Args:
            grp: The h5py group for the sequence.
        """
        super().__init__()
        self._group = grp

    @property
    def laws(self) -> dict[str, law.Law]:
        """The laws for the sequence."""
        laws = {}
        for k, v in self._group.items():
            try:
                if v.attrs["TYPE"] == "LAW":
                    laws[k] = law.Law(v)
            except KeyError:
                continue

        return laws

    @overload
    def __getitem__(
        self,
        item: Literal["transmit_law", "TRANSMIT_LAW", "receive_law", "RECEIVE_LAW"],
    ) -> tuple[law.Law]: ...

    @overload
    def __getitem__(
        self, item: Literal["probe_list", "PROBE_LIST"]
    ) -> tuple[probe.Probe]: ...

    @overload
    def __getitem__(
        self, item: Literal["filter_type", "FILTER_TYPE"]
    ) -> FilterType: ...

    @overload
    def __getitem__(
        self, item: Literal["date_and_time", "DATE_AND_TIME"]
    ) -> datetime.datetime: ...

    @overload
    def __getitem__(self, item: str) -> Any: ...

    def __getitem__(self, item: str):
        match item.upper():
            case "TRANSMIT_LAW" | "RECEIVE_LAW" as field_name:
                return tuple(law.Law(l) for l in self._group[field_name])
            case "PROBE_LIST":
                return tuple(probe.Probe(p) for p in self._group["PROBE_LIST"])
            case "FILTER_TYPE":
                try:
                    return FilterType(self._group["FILTER_TYPE"])
                except KeyError:
                    raise _exceptions.OptionalDatafieldError("FILTER_TYPE")
            case "DATE_AND_TIME":
                try:
                    return datetime.datetime.fromisoformat(self._group["DATE_AND_TIME"])
                except KeyError:
                    raise _exceptions.OptionalDatafieldError("DATE_AND_TIME")

        return super().__getitem__(item)

    @functools.cached_property
    def n_ascans(self) -> int:
        return self["mfmc_data"].shape[1]

    @functools.cached_property
    def ascan_length(self) -> int:
        return self["mfmc_data"].shape[2]

    @functools.cached_property
    def sample_times(self) -> np.ndarray:
        n_samples = self.ascan_length
        start = self["start_time"][()]
        step = self["time_step"][()]
        return start + np.arange(n_samples) * step

    @functools.cached_property
    def velocities(self) -> _types.Velocities:
        specimen_velocity = self["specimen_velocity"]
        wedge_velocity = self.get("wedge_velocity", (None, None))

        return _types.Velocities(*specimen_velocity, *wedge_velocity)

    @functools.cached_property
    def norm_divisor(self) -> float:
        dtype = self["mfmc_data"].dtype
        if dtype.kind == "f":
            return 1.0

        min_ = int(np.min(self["mfmc_data"]))
        max_ = int(np.max(self["mfmc_data"]))

        if dtype.kind == "u":
            return max_
        elif dtype.kind == "i":
            return max(-min_, max_)

    def get_ascan(self, index: int, normalise: bool = False) -> _types.AScan:
        data = self["mfmc_data"][:, index, :]
        if normalise:
            data = np.asarray(data, np.float32) / self.norm_divisor

        transmit = law.Law(self["transmit_law"][index])
        receive = law.Law(self["receive_law"][index])
        return _types.AScan(data, transmit, receive)

    def ascan_iterator(self) -> Iterator[_types.AScan]:
        for i in range(self.n_ascans):
            yield self.get_ascan(i)
