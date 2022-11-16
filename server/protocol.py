import asyncio
import struct
from random import randint
from typing import Union
from logging import Logger, DEBUG

from server.player import Player, PlayerDirection
from server.gamestate import GameState
from common.package import NetworkPackageBuilder, PackageType, CommandType, ActionType, RequestType

class ServerProtocol(asyncio.Protocol):

    def __init__(self):
        self.logger = Logger(__name__, level=DEBUG)
        self.gs = GameState()
        self.message_n = 0
        self.player: Union[Player, None] = None
        self.transport = None
        pass

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport
        if not self.gs.in_work():
            self.gs.start()

    def data_received(self, data):
        self.message_n += 1
        self.handle_input(data)

    def connect_player(self, nickname):
        self.player = Player(nickname, (randint(0, 600), randint(0, 400)))
        self.gs.add_player(self.player)

    def respawn_player(self):
        self.player.set_position((randint(0, 600), randint(0, 400)))

    def disconnect_player(self):
        if self.player is not None:
            self.gs.remove_player(self.player)
            self.player = None
            peername = self.transport.get_extra_info('peername')
            print('Connection with {} closed'.format(peername))
        else:
            self.logger.warning("Trying to disconnect already disconnected player!")

    def handle_action(self, packet, action, data):
        action = ActionType(action)
        builder = NetworkPackageBuilder()
        builder.set_package(packet)
        builder.set_action(action)
        if action == ActionType.MOVE:
            pos_x, pos_y, direction = struct.unpack("!ffB", data)
            self.player.move((pos_x, pos_y), PlayerDirection(direction + 1))
        if action == ActionType.FIRE:
            pass
        if action == ActionType.MOVE_LEFT:
            pass
        if action == ActionType.MOVE_RIGHT:
            pass
        if action == ActionType.MOVE_DOWN:
            pass
        if action == ActionType.MOVE_UP:
            pass
        self.transport.write(builder.build())

    def handle_command(self, packet, action, data):
        action = CommandType(action)
        builder = NetworkPackageBuilder()
        builder.set_package(packet)
        builder.set_action(action)
        if action == CommandType.CONNECT:
            print(data)
            nickname, = struct.unpack("!10s", data)
            self.connect_player(nickname.decode())
            builder.set_data("!ff", *self.player.position)
        elif action == CommandType.DISCONNECT:
            self.disconnect_player()
        elif action == CommandType.RESPAWN:
            self.respawn_player()
            builder.set_data("!ff", *self.player.position)
        else:
            return
        self.transport.write(builder.build())

    def handle_request(self, packet, action, data):
        action = RequestType(action)
        builder = NetworkPackageBuilder()
        builder.set_package(packet)
        builder.set_action(action)
        if action == RequestType.GAME_STATE:
            builder.set_raw_data(self.gs.deserialize())
        if action == RequestType.LEVEL_DESTRUCTION:
            pass
        if action == RequestType.POSITIONS:
            builder.set_raw_data(self.gs.deserialize_players(self.player.nickname))
        self.transport.write(builder.build())

    def handle_input(self, data):
        packet, action, data_len = struct.unpack("!BBB", data[:3])
        packet = PackageType(packet)
        if packet == PackageType.ACTION:
            self.handle_action(packet, action, data[3:])
        elif packet == PackageType.COMMAND:
            self.handle_command(packet, action, data[3:])
        elif packet == PackageType.REQUEST:
            self.handle_request(packet, action, data[3:])