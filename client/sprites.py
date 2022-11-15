import math
import struct
from typing import Tuple

import pygame as pg

from client.animationdirector import AnimationDirector
from client.resourcemanager import ResourceManager

class EntitySprite(pg.sprite.Sprite):

    def __init__(self, nickname: str, position):
        super().__init__()
        self.rect = pg.Rect(position, (32, 32))
        self.angle = 90
        self.nickname = nickname
        self.is_alive = False

    def update(self, data):
        print(data)
        self.rect.x, self.rect.y = data[self.nickname]["position"]
        self.is_alive = data[self.nickname]["is_alive"]
        desired_angle = data[self.nickname]["angle"]
        if self.angle != desired_angle:
                self.image = pg.transform.rotate(self.image, desired_angle-self.angle)
                self.angle = desired_angle

    def move(self, position):
        self.rect.x, self.rect.y = position

    def deserialize(self):
        struct.pack("ffBB", *self.position, self.is_alive, self.angle//90)

    def get_position(self) -> Tuple[int, int]:
        return self.rect.x, self.rect.y

class TankSprite(EntitySprite):

    def __init__(self, nickname: str, position: Tuple[float, float]):
        super().__init__(nickname, position)
        self.image = ResourceManager().get_tile_for("Tank")

class PlayerTank(EntitySprite):

    def __init__(self, position):
        super().__init__("Вы", position)
        self.animation_director = AnimationDirector(ResourceManager().get_animation_tilemap_for("Tank"))
        self.key_pressed = 0
        self.last_state = self.rect.x, self.rect.y
        self.speed = 0.15

    @property
    def image(self):
        return self.animation_director.get_image()

    @image.setter
    def set_image(self, image):
        pass

    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            self.key_pressed = event.key

        if event.type == pg.KEYUP:
            if event.key == self.key_pressed:
                self.key_pressed = 0

    def is_moving(self) -> bool:
        return self.key_pressed != 0

    def update(self, delta_time: int):
        self.animation_director.update(delta_time)
        self.last_state = self.rect.x, self.rect.y
        if self.key_pressed == pg.K_w:
            self.move_stuff(90, delta_time)
            self.rotation_stuff(90)
        if self.key_pressed == pg.K_d:
            self.move_stuff(0, delta_time)
            self.rotation_stuff(0)
        if self.key_pressed == pg.K_a:
            self.move_stuff(180, delta_time)
            self.rotation_stuff(180)
        if self.key_pressed == pg.K_s:
            self.move_stuff(270, delta_time)
            self.rotation_stuff(270)

    def undo_move(self):
        self.rect.x, self.rect.y = self.last_state

    def rotation_stuff(self, desired_angle):
        if self.angle != desired_angle:
                self.animation_director.set_rotation(desired_angle-90)
                self.angle = desired_angle

    def move_stuff(self, desired_angle, delta_time):
        if self.angle != desired_angle:
            modx = self.rect.x % 16
            mody = self.rect.y % 16
            if modx <= 4 and modx >= 12 and int(math.cos(math.radians(desired_angle))) == 0:
                self.rect = self.rect.move(-modx if modx < 2 else 16-modx, 0)
            elif mody <= 4 and mody >= 12 and abs(int(math.cos(math.radians(desired_angle)))) == 1:
                self.rect = self.rect.move(0, -mody if mody < 2 else 16-mody)

        self.rect = self.rect.move(self.speed*delta_time*math.cos(math.radians(desired_angle)),
                                   -self.speed*delta_time*math.sin(math.radians(desired_angle)))


class Block(pg.sprite.Sprite):

    def __init__(self, pos):
       pg.sprite.Sprite.__init__(self)

       self.image = pg.Surface([16, 16])
       self.image.fill((128, 255, 0))

       self.rect = self.image.get_rect()
       self.rect.x, self.rect.y = [p*16 for p in pos]