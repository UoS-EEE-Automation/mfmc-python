from __future__ import annotations

import os
from types import TracebackType

import h5py

from mfmc.read import probe, sequence


class FileReader:
    def __init__(self, path: os.PathLike | str, group: str = "/") -> None:
        """A wrapper for accessing an MFMC file.

        This enumerates the probes and sequences and laws which are contained in the
        file.

        Args:
            path: The path of the MFMC file.
            group: The path of the group in the HDF5 file.
        """

        self.group = group  #: The path of the group in the HDF5 file.

        self._h5file = h5py.File(path, "r")

        try:
            if self._h5file.attrs["TYPE"] != "MFMC":
                raise ValueError("File type is invalid")

            version = self._h5file.attrs["VERSION"]
            if version != "2.0.0":
                raise ValueError(f"Unsupported version: {version}")
        except KeyError:
            raise ValueError("File does not contain MFMC data")

    def close(self) -> None:
        """Closes a MFMC file."""
        self._h5file.close()

    def __enter__(self) -> h5py.File:
        return self._h5file

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self._h5file.close()

    @property
    def probes(self) -> dict[str, probe.Probe]:
        probes = {}
        for k, v in self._h5file[self.group].items():
            if v.attrs["TYPE"] == "PROBE":
                probes[k] = probe.Probe(v)

        return dict(sorted(probes.items()))

    @property
    def sequences(self) -> dict[str, sequence.Sequence]:
        """A collection of the sequences defined in the file."""
        sequences = {}
        for k, v in self._h5file[self.group].items():
            if v.attrs["TYPE"] == "SEQUENCE":
                sequences[k] = sequence.Sequence(v)

        return dict(sorted(sequences.items()))
