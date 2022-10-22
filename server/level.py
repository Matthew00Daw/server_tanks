from enum import Enum
from typing import Tuple, List


class TileType(Enum):
    WALL = 1  # Невозможно сломать
    BRICK = 2  # Ломается от выстрела
    BUSH = 3  # Танк проходит сквозь
    WATER = 4  # Наедешь -- умрёщь, DeathCause == INCIDENT


class LevelBuilder:

    def __init__(self, dictionary: dict):
        self.level = Level()
        pass

    def get_result(self):
        return self.level


class Level:
    # Придумать как инициализировать, нужен десериализатор json файла
    def __init__(self, dimensions: Tuple[int, int]):
        # разложение по главной оси
        self.destruction_matrix = b"0x00"*dimensions[0]*dimensions[1]
        self.tiles_positions = dict([(TT.name.lower(), []) for TT in TileType])
        pass

    def set_tiles_type(self, tile_type: TileType, positions_list: List):
        self.tiles_positions[tile_type.name.lower()] = positions_list

    def get_tile_type(self, position, direction):
        pass

    def create_projectile(self, position, direction):
        pass
