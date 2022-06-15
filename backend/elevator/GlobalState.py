import enum

class State(enum.Enum):
    MOVEDOWN = 0
    MOVEUP = 1
    ACTIVE = 2
    INACTIVE = 3
    HOLDING = 4