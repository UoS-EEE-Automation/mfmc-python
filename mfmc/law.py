import h5py

from .group import Group


class Law(Group):
    _MANDATORY_DATASETS = ["PROBE", "ELEMENT"]
    _MANDATORY_ATTRS = ["TYPE"]
    _OPTIONAL_DATASETS = ["DELAY", "WEIGHTING"]
    _OPTIONAL_ATTRS = []

    def __init__(self, group: h5py.Group) -> None:
        """Representation of a law which belongs to a sequence.

        Args:
            group: The h5py group for the law.
        """
        self._group = group
