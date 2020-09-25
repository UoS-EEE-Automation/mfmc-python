from collections.abc import Mapping
import itertools
from typing import Any, ClassVar, Dict, List, Union

import h5py
import numpy as np

from .exceptions import RequiredDatafieldError, OptionalDatafieldError


class Group(Mapping[str, Union[str, np.ndarray]]):
    """A dictionary-like representation of a HDF5 group.

    Datafield access is case-insensitive.
    """

    # Class attributes, overridden in subclasses
    _MANDATORY_DATASETS: ClassVar[List[str]] = None
    _MANDATORY_ATTRS: ClassVar[List[str]] = None
    _OPTIONAL_DATASETS: ClassVar[List[str]] = None
    _OPTIONAL_ATTRS: ClassVar[List[str]] = None

    # Instance attribute type definition
    _group: h5py.Group

    def __getitem__(self, key: str) -> Union[str, np.ndarray]:
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
                raise RequiredDatafieldError(key)
            elif key in self._OPTIONAL_DATASETS + self._OPTIONAL_ATTRS:
                raise OptionalDatafieldError(key)

    def __len__(self) -> int:
        return len(self._group) + len(self._group.attrs)

    def __iter__(self):
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
    def _decode_data(data):
        if isinstance(data, bytes):
            return data.decode("ascii")
        elif isinstance(data, h5py.Dataset):
            return data[()]
        else:
            return data

    @property
    def user_attributes(self) -> Dict[str, Any]:
        """A dictionary with pairs of name and attribute values."""
        ret = {}
        for k, v in self._group.attrs.items():
            if k not in self._MANDATORY_ATTRS + self._OPTIONAL_ATTRS:
                ret[k] = self._decode_data(v)
        return ret

    @property
    def user_datasets(self) -> Dict[str, Any]:
        """A dictionary with pairs of name and dataset values."""
        ret = {}
        for k, v in self._group.items():
            if k not in self._MANDATORY_DATASETS + self._OPTIONAL_DATASETS:
                ret[k] = self._decode_data(v)
        return ret

    @classmethod
    def create(cls, file: h5py.File, name: str) -> None:
        """Create a group containing the required datasets and attributes."""
        group = file.create_group(name)

        for dataset_name in cls._MANDATORY_DATASETS:
            group.create_dataset(dataset_name)

        for attr in cls._MANDATORY_ATTRS:
            group.attrs[attr] = None
