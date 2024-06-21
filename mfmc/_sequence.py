from __future__ import annotations

import datetime
import enum
from typing import Any, Literal, overload

import h5py

from mfmc import _exceptions, _group, _law, _probe


class FilterType(enum.IntEnum):
    NONE = 0
    LOW_PASS = 1
    HIGH_PASS = 2
    BAND_PASS = 3
    OTHER = 4


class Sequence(_group.Group):
    _MANDATORY_DATASETS = (
        "MFMC_DATA",
        "PROBE_PLACEMENT_INDEX",
        "PROBE_POSITION",
        "PROBE_X_DIRECTION",
        "PROBE_Y_DIRECTION",
        "TRANSMIT_LAW",
        "RECEIVE_LAW",
        "PROBE_LIST",
    )
    _MANDATORY_ATTRS = ("TYPE", "TIME_STEP", "START_TIME", "SPECIMEN_VELOCITY")
    _OPTIONAL_DATASETS = ("MFMC_DATA_IM", "DAC_CURVE")
    _OPTIONAL_ATTRS = (
        "WEDGE_VELOCITY",
        "TAG",
        "RECEIVER_AMPLIFIER_GAIN",
        "FILTER_TYPE",
        "FILTER_PARAMETERS",
        "FILTER_DESCRIPTION",
        "OPERATOR",
        "DATE_AND_TIME",
    )

    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a sequence from a MFMC file.

        Args:
            grp: The h5py group for the sequence.
        """
        self._group = grp

    @property
    def laws(self) -> dict[str, _law.Law]:
        """The laws for the sequence."""
        laws = {}
        for k, v in self._group.items():
            try:
                if v.attrs["TYPE"] == "LAW":
                    laws[k] = _law.Law(v)
            except KeyError:
                continue

        return dict(sorted(laws.items()))

    @overload
    def __getitem__(
        self, item: Literal["transmit_law"] | Literal["receive_law"]
    ) -> tuple[_law.Law]: ...

    @overload
    def __getitem__(self, item: Literal["probe_list"]) -> tuple[_probe.Probe]: ...

    @overload
    def __getitem__(self, item: Literal["filter_type"]) -> FilterType: ...

    @overload
    def __getitem__(self, item: Literal["date_and_time"]) -> datetime.datetime: ...

    @overload
    def __getitem__(self, item: str) -> Any: ...

    def __getitem__(self, item):
        match item.upper():
            case "TRANSMIT_LAW" | "RECEIVE_LAW" as field_name:
                return tuple(_law.Law(l) for l in self._group[field_name])
            case "PROBE_LIST":
                return tuple(_probe.Probe(p) for p in self._group["PROBE_LIST"])
            case "FILTER_TYPE":
                try:
                    return FilterType(self._group["FILTER_TYPE"])
                except KeyError:
                    raise _exceptions.OptionalDatafieldError("FILTER_TYPE")
            case "DATE_AND_TIME":
                try:
                    return datetime.datetime.fromisoformat(
                        self._group["DATE_AND_TIME"]
                    )
                except KeyError:
                    raise _exceptions.OptionalDatafieldError("DATE_AND_TIME")

        return super().__getitem__(item)
