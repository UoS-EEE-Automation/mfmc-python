from __future__ import annotations

from collections.abc import Iterator, Mapping
import itertools
import pathlib
from typing import Any, overload

import h5py
import yaml

from mfmc import _exceptions


class Group(Mapping[str, Any]):
    """A dictionary-like representation of a HDF5 group.

    Datafield access is case-insensitive.
    """

    # Instance attribute type definition
    _group: h5py.Group

    def __init__(self) -> None:
        config_path = pathlib.Path(__file__).parent.parent / "format.yml"
        with open(config_path) as f:
            config = yaml.safe_load(f)[type(self).__name__.lower()]

        self._mandatory_datasets = []
        self._mandatory_attributes = []
        self._optional_datasets = []
        self._optional_attributes = []

        for name, metadata in config.items():
            if metadata["mandatory"]:
                if metadata["dataset"]:
                    self._mandatory_datasets.append(name)
                else:
                    self._mandatory_attributes.append(name)
            else:
                if metadata["dataset"]:
                    self._optional_datasets.append(name)
                else:
                    self._optional_attributes.append(name)

    def __getitem__(self, key: str) -> Any:
        """Get data from the group.

        Parameters:
            key: Case-insensitive field name.

        Returns:
            The data.
        """
        if not isinstance(key, str):
            raise TypeError("Datafield name must be a string")

        key = key.upper()

        try:
            if key in itertools.chain(
                self._mandatory_datasets, self._optional_datasets
            ):
                return self._decode_data(self._group[key])
            elif key in itertools.chain(
                self._mandatory_attributes, self._optional_attributes
            ):
                return self._decode_data(self._group.attrs[key])
            else:
                raise KeyError(f"Unknown datafield name: {key}")
        except KeyError:
            if key in itertools.chain(
                self._mandatory_datasets, self._mandatory_attributes
            ):
                raise _exceptions.MandatoryDatafieldError(key)
            elif key in itertools.chain(
                self._optional_datasets, self._optional_attributes
            ):
                raise _exceptions.OptionalDatafieldError(key)
            return None

    def __len__(self) -> int:
        return len(self._group) + len(self._group.attrs)

    def __iter__(self) -> Iterator[Any]:
        return itertools.chain(self._group, self._group.attrs)

    def is_mandatory(self, datafield_name: str) -> bool:
        """Checks if a datafield name is mandatory.

        Args:
            datafield_name: The name of a datafield name to check.

        Returns:
            Whether the datafield name is mandatory.
        """
        item = datafield_name.upper()
        return item in self._mandatory_datasets + self._mandatory_attributes

    def is_optional(self, datafield_name: str) -> bool:
        """Checks if a datafield name is optional.

        Args:
            datafield_name: The name of a datafield_name to check.

        Returns:
            Whether the datafield_name is optional.
        """
        item = datafield_name.upper()
        return item in self._optional_datasets + self._optional_attributes

    @staticmethod
    @overload
    def _decode_data(data: bytes) -> str: ...

    @staticmethod
    @overload
    def _decode_data(data: h5py.Dataset) -> h5py.Dataset: ...

    @staticmethod
    @overload
    def _decode_data[T](data: T) -> T: ...

    @staticmethod
    def _decode_data(data):
        if isinstance(data, bytes):
            return data.decode("ascii")
        else:
            return data

    @property
    def user_datasets(self) -> dict[str, Any]:
        """A dictionary with pairs of name and dataset values.

        Names are case-sensitive.
        """
        return {
            k: v
            for k, v in self._group.items()
            if k not in self._mandatory_datasets + self._optional_datasets
        }

    @property
    def user_attributes(self) -> dict[str, Any]:
        """A dictionary with pairs of name and attribute values.

        Names are case-sensitive.
        """
        return {
            k: v
            for k, v in self._group.attrs.items()
            if k not in self._mandatory_attributes + self._optional_attributes
        }
