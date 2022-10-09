from enum import Enum
from typing import Tuple


class TileType(Enum):
    WALL = 1  # Невозможно сломать
    BRICK = 2  # Ломается от выстрела
    BUSH = 3  # Танк проходит сквозь
    WATER = 4  # Наедешь -- умрёщь, DeathCause == INCIDENT


class Level:
    # Придумать как инициализировать, нужен десериализатор json файла
    def __init__(self, dimensions: Tuple[int, int]):
        pass

    def get_block_state(self, position, direction):
        pass

    def create_projectile(self, position, direction):
        pass
