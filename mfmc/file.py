import os
from typing import Dict, Union

import h5py

from .probe import Probe
from .sequence import Sequence

__all__ = ["File"]


class File:
    def __init__(self, path: Union[os.PathLike, str]) -> None:
        """A wrapper for accessing an MFMC file.

        This enumerates the probes and sequences and laws which are contained in the
        file.

        Args:
            path: The path of the MFMC file.
        """
        self._h5file = h5py.File(path, "r")

        try:
            if self._h5file.attrs["TYPE"] != b"MFMC":
                raise ValueError("File type is invalid")

            version = self._h5file.attrs["VERSION"].decode("ASCII")
            if version != "2.0.0":
                raise ValueError(f"Unsupported version: {version}")
        except KeyError:
            raise ValueError("File does not contain MFMC data")

        self._probes = {}
        for k, v in self._h5file.items():
            if v.attrs["TYPE"] == b"PROBE":
                self._probes[k] = Probe(v)

        self._sequences = {}
        for k, v in self._h5file.items():
            if v.attrs["TYPE"] == b"SEQUENCE":
                self._sequences[k] = Sequence(v)

    def close(self) -> None:
        """Closes a MFMC file."""
        self._h5file.close()

    @property
    def probes(self) -> Dict[str, Probe]:
        """A list of the probes defined in the file."""
        return self._probes

    @property
    def sequences(self) -> Dict[str, Sequence]:
        """A list of the sequences defined in the file."""
        return self._sequences
