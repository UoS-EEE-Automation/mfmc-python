import h5py

from mfmc import group


class Law(group.Group):
    _MANDATORY_DATASETS = ["PROBE", "ELEMENT"]
    _MANDATORY_ATTRS = ["TYPE"]
    _OPTIONAL_DATASETS = ["DELAY", "WEIGHTING"]
    _OPTIONAL_ATTRS = []

    def __init__(self, grp: h5py.Group) -> None:
        """Representation of a law which belongs to a sequence.

        Args:
            grp: The h5py group for the law.
        """
        self._group = grp
