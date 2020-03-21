from enum import Enum, IntEnum

class Axis(Enum):
    X = 1
    Y = 2


class SVSLevelRatio(IntEnum):
    LEVEL_0_BASE = 1
    LEVEL_1 = 4
    LEVEL_2 = 16
    LEVEL_3 = 32


class ResolutionLevel(IntEnum):
    LEVEL_0_BASE = 0
    LEVEL_1 = 1
    LEVEL_2 = 2
    LEVEL_3 = 3