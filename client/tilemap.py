from typing import Tuple, List

import pygame as pg


class TileMap:
    
    def __init__(self, filename: str, dimentions: Tuple[int, int]):
        self.tilemap = pg.image.load(filename)
        self.dimentions = dimentions
        self.tile_dimentions: Tuple[int, int] = [dim//num for dim, num in zip(self.tilemap.get_size(), self.dimentions)]
        self.tiles: List[pg.surface.Surface] = list()
        self._fill_tiles()

    def crop_tilemap(self, indices: Tuple[int, int]) -> pg.Surface:
        tile = pg.Surface(self.get_tile_dimentions())
        crop_coords = [dim*index for dim, index in zip(self.get_tile_dimentions(), indices)]
        tile.blit(self.tilemap, (0, 0), crop_coords)
        return tile

    def _fill_tiles(self):
        x, y = self.dimentions
        for i in range(x):
            for j in range(y):
                self.tiles.append(self.crop_tilemap(i, j))

    def get_tile_dimentions(self) -> Tuple[int, int]: 
        return self.tile_dimentions

    def get_tile(self, index: int):
        return self.tiles[index]