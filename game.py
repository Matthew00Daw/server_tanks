import struct
import socket
from typing import Tuple

import pygame as pg

from common.package import NetworkPackageBuilder
from common.network import PackageType, CommandType, RequestType, ActionType
from client.groups import Level, TanksGroup
from client.sprites import TankSprite, PlayerTank


class ServerInterface:

    def __init__(self, host: str, port: int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)
        self.s.connect((host, port))

    def connect(self, nickname: str) -> Tuple[float, float]:
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.COMMAND)
        builder.set_action(CommandType.CONNECT)
        builder.set_raw_data(nickname.encode() + bytes(10 - len(nickname)))
        self.s.sendall(builder.build())
        response = self.s.recv(256)
        position = struct.unpack("!ff", response[3:])
        return position

    def disconnect(self) -> None:
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.COMMAND)
        builder.set_action(CommandType.DISCONNECT)
        self.s.sendall(builder.build())
        self.s.recv(256)

    def send_position(self, position, direction):
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.ACTION)
        builder.set_action(ActionType.MOVE)
        builder.set_data("!ffB", *position, direction)
        self.s.sendall(builder.build())
        self.s.recv(256)

    def get_positions(self):
        retval = {}
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.REQUEST)
        builder.set_action(RequestType.POSITIONS)
        self.s.sendall(builder.build())
        response = self.s.recv(256)
        num_tanks = response[3]
        other_tanks = struct.unpack("!" + num_tanks * "10sffBB", response[4:])
        for i in range(num_tanks):
            tank_data = other_tanks[i * 5:(i + 1) * 5]
            retval[tank_data[0].replace(b"\x00", b"").decode()] = {"position": tank_data[1:3],
                                                                   "is_alive": bool(tank_data[3]),
                                                                   "angle": 90 * (tank_data[4] - 1)}
        return retval


class Game:

    def __init__(self):
        pg.init()
        self.server = None
        self.screen = pg.display.set_mode([800, 600])
        self.client_sprite = PlayerTank((0., 0.))
        self.client_tank = pg.sprite.GroupSingle(self.client_sprite)
        self.level = Level((64, 64))
        self.enemy_tanks = None
        self.game_clock = pg.time.Clock()
        self.running = False
        self.nickname = "mouse"

    def connect_and_get_state(self):
        try:
            self.server = ServerInterface("127.0.0.1", 8888)
            position = self.server.connect(self.nickname)
            self.client_sprite.move(position)
            tanks_data = self.server.get_positions()
            self.enemy_tanks = TanksGroup([TankSprite(nickname, (0., 0.)) for nickname in tanks_data])
            self.enemy_tanks.update(tanks_data)
        except struct.error as e:
            print(f"Protocol level error: {e}")
            self.stop()
        except (socket.timeout, ConnectionRefusedError) as e:
            print(f"Timeout exception")
            self.stop()

    def process_events(self):
        for event in pg.event.get():
            self.client_sprite.handle_input(event)
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.stop()
            elif event.type == pg.QUIT:
                self.stop()

    def update_game_objects(self):
        dt = self.game_clock.tick(60)
        tanks_data = self.server.get_positions()
        self.enemy_tanks.update(tanks_data)

        if self.client_sprite.is_moving():
            self.client_tank.update(dt)
            if (pg.sprite.spritecollide(self.client_sprite, self.level, dokill=False)
                    or pg.sprite.spritecollide(self.client_sprite, self.enemy_tanks, dokill=False)):
                self.client_sprite.undo_move()
            self.server.send_position([self.client_sprite.rect.x, self.client_sprite.rect.y],
                                      self.client_sprite.angle // 90)

    def start(self):
        self.running = True
        self.connect_and_get_state()
        while self.running:
            self.process_events()
            self.update_game_objects()
            self.draw()
        self.server.disconnect()
        pg.quit()

    def draw(self):
        self.screen.fill((0, 0, 0))
        # pg.draw.circle(screen, (0, 255, 0), (400, 300), 25, 0)
        self.level.draw(self.screen)
        self.client_tank.draw(self.screen)
        self.enemy_tanks.draw(self.screen)

        pg.display.flip()

    def stop(self):
        self.running = False


if __name__ == "__main__":
    game = Game()
    game.start()
