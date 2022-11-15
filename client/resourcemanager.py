import pygame as pg

from client.tilemap import TileMap, NestedTileMap
from common.util import singleton

TILEMAP_PATH = "resources\\tanks_sheet.png"
TILEMAP_DIMS = (8, 4)


@singleton
class ResourceManager:
    
    def __init__(self):
        self.root_tilemap = TileMap(TILEMAP_PATH, TILEMAP_DIMS)

    def get_tile_for(self, idx: str) -> pg.Surface:
        if idx == "Tank":
            return self.root_tilemap.get_tile(1)
        elif idx == "Bullet":
            return self.root_tilemap.get_tile(20)
        else:
            raise Exception("No such resource")

    def get_animation_tilemap_for(self, idx: str) -> TileMap:
        if idx == "Tank":
            return NestedTileMap(self.root_tilemap, slice(1, 8))
        