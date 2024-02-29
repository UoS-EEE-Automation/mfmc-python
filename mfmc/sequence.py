from __future__ import annotations

import datetime
import enum
from typing import Any, Literal, overload

import h5py
import natsort

from mfmc import exceptions, group, law


class FilterType(enum.IntEnum):
    NONE = 0
    LOW_PASS = 1
    HIGH_PASS = 2
    BAND_PASS = 3
    OTHER = 4


class Sequence(group.Group):
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

    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a sequence from a MFMC file.

        Args:
            grp: The h5py group for the sequence.
        """
        self._group = grp

        self._laws = {}
        for k, v in self._group.items():
            try:
                if v.attrs["TYPE"] == "LAW":
                    self._laws[k] = law.Law(v)
            except KeyError:
                continue

    @property
    def laws(self) -> dict[str, law.Law]:
        """List of law objects for the sequence."""
        keys = natsort.natsorted(self._laws.keys())
        return {law: self._laws[l] for l in keys}

    @overload
    def __getitem__(self, item: Literal["filter_type"]) -> FilterType:
        ...

    def __getattr__(self, item: Literal["date_and_time"]) -> datetime.datetime:
        ...

    def __getitem__(self, item: str) -> Any:
        if item.lower() == "filter_type":
            try:
                return FilterType(self.hdf5_group["filter_type"])
            except KeyError:
                raise exceptions.OptionalDatafieldError
        elif item.lower() == "date_and_time":
            try:
                return datetime.datetime.fromisoformat(self.hdf5_group["date_and_time"])
            except KeyError:
                raise exceptions.OptionalDatafieldError
        else:
            return super().__getitem__(item)
