import enum

class Direction(enum.Enum):
    UP = -1
    DOWN = 1
    LEFT = -1
    RIGHT = 1

@enum.unique
class Status(enum.Enum):
    OPEN = 0
    IN_PROGRESS = 1
    DONE = 2