from __future__ import annotations

import os
from types import TracebackType

import h5py
import natsort

from mfmc import probe, sequence


class File:
    def __init__(self, path: os.PathLike | str) -> None:
        """A wrapper for accessing an MFMC file.

        This enumerates the probes and sequences and laws which are contained in the
        file.

        Args:
            path: The path of the MFMC file.
        """
        self._h5file = h5py.File(path, "r")

        try:
            if self._h5file.attrs["TYPE"] != "MFMC":
                raise ValueError("File type is invalid")

            version = self._h5file.attrs["VERSION"]
            if version != "2.0.0":
                raise ValueError(f"Unsupported version: {version}")
        except KeyError:
            raise ValueError("File does not contain MFMC data")

        self._probes = {}
        for k, v in self._h5file.items():
            if v.attrs["TYPE"] == "PROBE":
                self._probes[k] = probe.Probe(v)

        self._sequences = {}
        for k, v in self._h5file.items():
            if v.attrs["TYPE"] == "SEQUENCE":
                self._sequences[k] = sequence.Sequence(v)

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
        """A collection of the probes defined in the file."""
        keys = natsort.natsorted(self._probes.keys())
        return {probe: self._probes[p] for p in keys}

    @property
    def sequences(self) -> dict[str, sequence.Sequence]:
        """A collection of the sequences defined in the file."""
        keys = natsort.natsorted(self._sequences.keys())
        return {sequence: self._sequences[s] for s in keys}
