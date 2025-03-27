import dataclasses

import numpy as np

from mfmc.read import law


@dataclasses.dataclass
class AScan:
    data: np.ndarray
    transmit_law: law.Law
    receive_law: law.Law


@dataclasses.dataclass
class Frame:
    ascans: tuple[AScan]


@dataclasses.dataclass
class Velocities:
    specimen_shear: float
    specimen_longitudinal: float
    wedge_shear: float | None = None
    wedge_longitudinal: float | None = None
