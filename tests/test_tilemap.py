import pytest
import os
import pygame as pg

from client.tilemap import TileMap

TILEMAP_PATH = "resources\\tanks_sheet.png"

class TestTileMap:
    
    def setup_class(self) -> None:
        self.tilemap  = TileMap(TILEMAP_PATH, (8, 4))

    def test_dims(self):
        assert self.tilemap.get_tile_dimentions() == (32, 32)

    def test_quantity(self):
        assert len(self.tilemap.tiles) == 8*4

    def test_crop(self):
        image = pg.image.load(TILEMAP_PATH)
        test_tile = pg.Surface((32, 32))
        test_tile.blit(image, (0, 0), pg.Rect(32*1, 0, 32, 32))
        tile = self.tilemap.get_tile(1)
        for i in range(32**2):
            coordinates = [i%32, i//32]
            assert tile.get_at(coordinates) == test_tile.get_at(coordinates)