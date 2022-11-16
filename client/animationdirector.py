import pygame as pg

from client.tilemap import TileMap

class AnimationDirector:

    def __init__(self, tilemap: TileMap, in_reverse: bool):
        self.timer = 0
        self.frame_time = 125 #ms
        self.tilemap = tilemap
        self.rotation = 0
        self.in_reverse = in_reverse
        self.image_index = 0
        self.num_tiles = self.tilemap.get_num_tiles()
        self.current_tile = self.tilemap.get_tile(self.get_index())
        pass

    def get_index(self):
        return self.num_tiles - (self.image_index + 1) if self.in_reverse else self.image_index

    def get_image(self) -> pg.surface.Surface:
        return self.current_tile

    def set_rotation(self, rotation):
        self.rotation = rotation
        self.current_tile = pg.transform.rotate(self.tilemap.get_tile(self.get_index()), self.rotation)

    def update(self, dt: float):
        self.timer += dt
        if self.timer >= self.frame_time:
            self.timer %= self.frame_time
            self.image_index = (self.image_index + 1)%self.num_tiles
            self.current_tile = pg.transform.rotate(self.tilemap.get_tile(self.get_index()), self.rotation)