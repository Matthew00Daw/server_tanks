import pygame as pg

from client.tilemap import TileMap

class AnimationDirector:

    def __init__(self, tilemap: TileMap):
        self.timer = 0
        self.frame_time = 125 #ms
        self.image_index = 0
        self.tilemap = tilemap
        self.rotation = 0
        self.num_tiles = self.tilemap.get_num_tiles()
        self.current_tile = self.tilemap.get_tile(self.image_index)
        pass

    def get_image(self) -> pg.surface.Surface:
        return self.current_tile

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.current_tile = pg.transform.rotate(self.tilemap.get_tile(self.image_index), self.rotation)

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer %= self.frame_time
            self.image_index = (self.image_index + 1)%self.num_tiles
            self.current_tile = pg.transform.rotate(self.tilemap.get_tile(self.image_index), self.rotation)