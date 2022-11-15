import struct
from enum import Enum
from typing import Tuple


class PlayerState(Enum):
    ALIVE = 1
    DEAD = 2


class PlayerDirection(Enum):
    RIGHT = 1
    UP = 3
    LEFT = 2
    DOWN = 4


class Player:
    
    def __init__(self, nickname: str, position: Tuple[float, float]):
        self.nickname = nickname
        self.position = position
        self.state = PlayerState.DEAD
        self.direction = PlayerDirection.UP

    def deserialize(self):
        nickname = self.nickname.encode() + bytes(10 - len(self.nickname))
        retval = struct.pack("!10sffBB", nickname, *self.position, self.state.value, self.direction.value)
        return retval

    def set_state(self, state: PlayerState):
        self.state = state

    def set_position(self, position: Tuple[float, float]):
        self.position = position

    def move(self, position: Tuple[float, float], direction: PlayerDirection):
        self.set_position(position)
        self.direction = direction
