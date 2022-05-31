import enum

class State(enum.Enum):
    FREE = 0
    MOVEUP = 1
    MOVEDOWN = 2
    HOLD = 3
    OPENING = 4
    CLOSING = 5