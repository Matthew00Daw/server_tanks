import random
import math
from typing import Any, Iterator, List, Tuple

import pygame as pg
import numpy as np

class Tank(pg.sprite.Sprite):

    def __init__(self):
        super().__init__()
        self.image = pg.image.load("C:\\users\\workstation2\\downloads\\sprite.png")
        self.angle = 90
        self.key_pressed = 0
        # self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
        self.rect.x = 400
        self.rect.y = 300
        self.last_state = self.rect.x, self.rect.y
        self.speed = 0.15


    def handle_input(self, event):
        if event.type == pg.KEYDOWN:
            self.key_pressed = event.key

        if event.type == pg.KEYUP:
            if event.key == self.key_pressed:
                self.key_pressed = 0

    def update(self, delta_time: int):
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
                self.image = pg.transform.rotate(self.image, desired_angle-self.angle)
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

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, pos):
       # Call the parent class (Sprite) constructor
       pg.sprite.Sprite.__init__(self)

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pg.Surface([16, 16])
       self.image.fill((128, 128, 0))

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()
       self.rect.x, self.rect.y = [p*16 for p in pos]


class CompositeGroup(pg.sprite.Group):
    
    def __init__(self, *groups):
        self._groups: List[pg.sprite.Group] = groups

    def draw(self, surface: pg.Surface) -> List[pg.Rect]:
        retval = []
        [retval.extend(group.draw(surface)) for group in self._groups]
        return retval

    def update(self, *args: Any, **kwargs: Any) -> None:
        return [group.update(args, kwargs) for group in self._groups]

    def sprites(self) -> List[pg.sprite.Sprite]:
        retval = []
        [retval.extend(group.sprites) for group in self._groups]
        return retval


class Level(pg.sprite.Group):
    def __init__(self, dims: Tuple[int, int]):
        super().__init__()
        sprites = []
        for i in range(int(0.05*dims[0]*dims[1])):
            X, Y = np.meshgrid(np.arange(dims[0]), np.arange(dims[1]))
            x, y = np.random.randint(dims[0]), np.random.randint(dims[1])
            sprites.append(Block((x, y)))
        self.add(*sprites)
            
        
        pass

if __name__ == "__main__":
    pg.init()
    font = pg.font.SysFont("segoe-print", 24)
    client_tank = pg.sprite.Group()
    screen = pg.display.set_mode([800, 600])
    tank = Tank()
    client_tank.add(tank)
    game_clock = pg.time.Clock()
    level = Level((64, 64))
    pg.sprite.spritecollide(tank, level, dokill=True)
    running = True

    while running:
        for event in pg.event.get():
            tank.handle_input(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
            elif event.type == pg.QUIT:
                running = False

        
        screen.fill((0, 0, 0))
        dt = game_clock.tick(60)
        #pg.draw.circle(screen, (0, 255, 0), (400, 300), 25, 0)
        level.draw(screen)
        client_tank.update(dt)
        if pg.sprite.spritecollide(tank, level, dokill=False):
            tank.undo_move()
        text_surface = font.render(f"x: {tank.rect.x}, y: {tank.rect.y}", False, (255, 255, 255))
        screen.blit(text_surface, (0, 0))
        client_tank.draw(screen)
        
        
        pg.display.flip()

    
    pg.quit()