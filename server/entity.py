from enum import Enum
from typing import Tuple


class TankDirection(Enum):
    N = 1
    W = 2
    S = 3
    E = 4

    @staticmethod
    def get_mask_by_direction(value: TankDirection):
        if value == TankDirection.N:
            return [0, 1]
        elif value == TankDirection.W:
            return [1, 0]
        elif value == TankDirection.S:
            return [0, -1]
        elif value == TankDirection.E:
            return [-1, 0]

class DeathCause(Enum):
    HIT = 1
    COLLISION = 2
    INCIDENT = 3

class TankState(Enum):
    NORMAL = 1
    DEAD = 2
    SPAWNING = 3
    DROWNING = 4
    EXPLODING = 5


class TankEntity:

    def __init__(self, level, position: Tuple[float, float], direction: TankDirection):
        self.position = position
        self.direction = direction
        self.level = level
        self.state = TankState.DEAD

    def shot(self):
        """
        self.level.create_projectile(position, direction)
        :return:
        """
        pass

    def can_move(self) -> bool:
        """
        if self.level.get_block_state(position, direction)
        Проверяет может ли танк проехать в выбранном направлении
        :return:
        """
        return False

    def move(self):
        """
        Танчик тупа едет
        :return:
        """
        self.position += 0.25*TankDirection.get_mask_by_direction(self.direction)

    def rotate(self, new_direction: TankDirection):
        """
        повернуть танк
        :param new_direction:
        :return:
        """
        self.direction = new_direction

    def kill(self, killer, death_reason):
        self.state = TankState.DEAD

    def respawn(self, position):
        self.position = position
        self.state = TankState.SPAWNING
