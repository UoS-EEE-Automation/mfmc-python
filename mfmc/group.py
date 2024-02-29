from collections.abc import Iterator, Mapping
import itertools
from typing import Any, ClassVar, overload, TypeVar

import h5py

from mfmc import exceptions

_T = TypeVar("_T")


class Group(Mapping[str, Any]):
    """A dictionary-like representation of a HDF5 group.

    Datafield access is case-insensitive.
    """

    # Class attributes, overridden in subclasses
    _MANDATORY_DATASETS: ClassVar[list[str]] | None = None
    _MANDATORY_ATTRS: ClassVar[list[str]] | None = None
    _OPTIONAL_DATASETS: ClassVar[list[str]] | None = None
    _OPTIONAL_ATTRS: ClassVar[list[str]] | None = None

    # Instance attribute type definition
    _group: h5py.Group

    def __getitem__(self, key: str) -> Any:
        if not isinstance(key, str):
            raise TypeError("Datafield name must be a string")

        key = key.upper()

        try:
            if key in self._MANDATORY_DATASETS + self._OPTIONAL_DATASETS:
                return self._decode_data(self._group[key])
            elif key in self._MANDATORY_ATTRS + self._OPTIONAL_ATTRS:
                return self._decode_data(self._group.attrs[key])
            else:
                raise KeyError(f"Unknown datafield name: {key}")
        except KeyError:
            if key in self._MANDATORY_DATASETS + self._MANDATORY_ATTRS:
                raise exceptions.RequiredDatafieldError(key)
            elif key in self._OPTIONAL_DATASETS + self._OPTIONAL_ATTRS:
                raise exceptions.OptionalDatafieldError(key)

    def __len__(self) -> int:
        return len(self._group) + len(self._group.attrs)

    def __iter__(self) -> Iterator[Any]:
        return itertools.chain(self._group, self._group.attrs)

    @classmethod
    def is_mandatory(cls, datafield_name: str) -> bool:
        """Checks if a datafield name is mandatory.

        Args:
            datafield_name: The name of a datafield name to check.

        Returns:
            Whether the datafield name is mandatory.
        """
        item = datafield_name.upper()
        return item in cls._MANDATORY_DATASETS + cls._MANDATORY_ATTRS

    @classmethod
    def is_optional(cls, datafield_name: str) -> bool:
        """Checks if a datafield name is optional.

        Args:
            datafield_name: The name of a datafield_name to check.

        Returns:
            Whether the datafield_name is optional.
        """
        item = datafield_name.upper()
        return item in cls._OPTIONAL_DATASETS + cls._OPTIONAL_ATTRS

    @staticmethod
    @overload
    def _decode_data(data: bytes) -> str:
        ...

    @staticmethod
    @overload
    def _decode_data(data: h5py.Dataset) -> float | h5py.Dataset:
        ...

    @staticmethod
    @overload
    def _decode_data(data: _T) -> _T:
        ...

    @staticmethod
    def _decode_data(data):
        if isinstance(data, bytes):
            return data.decode("ascii")
        elif isinstance(data, h5py.Dataset):
            try:
                return data[()].item()  # Try to return a scalar
            except ValueError:
                return data[()]
        else:
            return data

    @property
    def user_attributes(self) -> dict[str, Any]:
        """A dictionary with pairs of name and attribute values."""
        return {
            k: v
            for k, v in self._group.attrs.items()
            if k not in self._MANDATORY_ATTRS + self._OPTIONAL_ATTRS
        }

    @property
    def user_datasets(self) -> dict[str, Any]:
        """A dictionary with pairs of name and dataset values."""
        return {
            k: v
            for k, v in self._group.items()
            if k not in self._MANDATORY_DATASETS + self._OPTIONAL_DATASETS
        }

    @classmethod
    def create(cls, file: h5py.File, name: str) -> None:
        """Create a group containing the required datasets and attributes."""
        group = file.create_group(name)

        for dataset_name in cls._MANDATORY_DATASETS:
            group.create_dataset(dataset_name)

        for attr in cls._MANDATORY_ATTRS:
            group.attrs[attr] = None

    @property
    def hdf5_group(self) -> h5py.Group:
        return self._group
