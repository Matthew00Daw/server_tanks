from random import randint

import pytest

from client.groups import TanksGroup
from client.sprites import TankSprite


class TankGroupTest:
    
    def __init__(self):
        self.tanks_data = dict()
        for i in range(5):
            self.tanks_data["tank_" + str(i+1)] = {"position": [randint(0, 400), randint(0, 350)], "is_alive": True, "angle": 90}
        self.group = TanksGroup([TankSprite(nickname, (0, 0)) for nickname in self.tanks_data])

    def update_test(self):
        self.group.update(self.tanks_data)
        for sprite in self.group.sprites():
            nickname = sprite.nickname
            position = sprite.get_position()
            assert self.tanks_data[nickname].get("position") == position

    def remove_player_test(self):
        new_data = dict(self.tanks_data)
        del new_data["tank_2"]
        self.group.update(new_data)
        nicknames = [sprite.nickname for sprite in self.group.sprites()]
        assert (len(self.group.sprites) == 4
                and "tank_2" not in nicknames)
        self.group.update(self.tanks_data)

    def add_player_test(self):
        new_data = dict(self.tanks_data)
        new_data["tank_6"] = {"position": [randint(0, 400), randint(0, 350)], "is_alive": True, "angle": 90}
        self.group.update(new_data)
        nicknames = [sprite.nickname for sprite in self.group.sprites()]
        assert (len(self.group.sprites) == 6
                and "tank_6" in nicknames)
        self.group.update(self.tanks_data)

    