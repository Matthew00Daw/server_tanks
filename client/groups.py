from typing import List, Any, Tuple

import pygame as pg
import numpy as np

from sprites import Block, TankSprite

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

    def random_level(self):
        sprites = []
        for i in range(int(0.05*self.dims[0]*self.dims[1])):
            # X, Y = np.meshgrid(np.arange(self.dims[0]), np.arange(self.dims[1]))
            x, y = np.random.randint(self.dims[0]), np.random.randint(self.dims[1])
            sprites.append(Block((x, y)))
        self.add(*sprites)

    def generate_border(self):
        sprites = []
        y_const = np.arange(0, self.dims[0] - 1)
        x_const = np.arange(-1, self.dims[1])
        sprites.extend([Block([-1, y]) for y in x_const])
        sprites.extend([Block([self.dims[0], y]) for y in x_const])
        sprites.extend([Block([x, -1]) for x in y_const])
        sprites.extend([Block([x, self.dims[1]]) for x in y_const])
        self.add(*sprites)

    def __init__(self, dims: Tuple[int, int]):
        super().__init__()
        self.dims = dims
        #self.random_level()
        self.generate_border()

class TanksGroup(pg.sprite.Group):
    
    def __init__(self, sprites: List[TankSprite]):
        self.nickname_font = pg.font.SysFont("segoe-print", 24)
        self.users = [sprite.nickname for sprite in sprites]
        super().__init__(sprites)

    def update(self, *args: Any, **kwargs: Any) -> None:
        self.add_connected(args[0])
        self.remove_disconnected(args[0])
        return super().update(*args, **kwargs)

    def remove_disconnected(self, users: List[str]):
        to_remove = [sprite for sprite in self.sprites() if sprite.nickname not in users]
        self.remove(to_remove)

    def add_connected(self, sprites: List[str]):
        current_nicknames = [sprite.nickname for sprite in self.sprites()]
        to_add = [sprite for sprite in sprites if sprite not in current_nicknames]
        self.add([TankSprite(nickname, [0, 0]) for nickname in to_add])

    def draw(self, surface: pg.Surface) -> List[pg.Rect]:
        for sprite in self.sprites():
            text_surface = self.nickname_font.render(sprite.nickname, False, (255, 255, 255))
            surface.blit(text_surface, (sprite.rect.x, sprite.rect.y - 32))
        return super().draw(surface)