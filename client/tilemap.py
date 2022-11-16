from typing import Tuple, List, Union

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
        tile.blit(self.tilemap, (0, 0), pg.Rect(crop_coords, (32, 32)))
        return tile

    def _fill_tiles(self):
        x, y = self.dimentions
        for j in range(y):
            for i in range(x):
                self.tiles.append(self.crop_tilemap((i, j)))

    def get_tile_dimentions(self) -> Tuple[int, int]: 
        return tuple(self.tile_dimentions)

    def get_tile(self, index: int):
        return self.tiles[index]

    def get_num_tiles(self) -> int:
        return len(self.tiles)


class NestedTileMap(TileMap):
    
    def __init__(self, tilemap: TileMap, selection: list):

        self.dimentions = tilemap.dimentions
        self.tile_dimentions: Tuple[int, int] = tilemap.get_tile_dimentions()
        self.tiles: List[pg.surface.Surface] = [tilemap.tiles[idx] for idx in selection]