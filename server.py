import asyncio
import struct
import time
from random import randint
from typing import Tuple, List, Union
from enum import Enum

from common.package import NetworkPackageBuilder, PackageType, CommandType, ActionType, RequestType

class PlayerState(Enum):
    ALIVE = 1
    DEAD = 2

class PlayerDirection(Enum):
    RIGHT = 1
    UP = 3
    LEFT = 2
    DOWN = 4

def singleton(cls):
    instances = {}
    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]
    return getinstance

class Player:
    
    def __init__(self, nickname: str, position: Tuple[float, float]):
        self.nickname = nickname
        self.position = position
        self.state = PlayerState.DEAD
        self.direction = PlayerDirection.UP

    def deserialize(self):
        nickname = self.nickname.encode() + bytes(10 - len(self.nickname))
        retval = struct.pack("!10sffBB", nickname, *self.position, self.state.value, self.direction.value)
        return retval

    def set_state(self, state: PlayerState):
        self.state = state

    def set_position(self, position: Tuple[float, float]):
        self.position = position

    def move(self, position: Tuple[float, float], direction: PlayerDirection):
        self.set_position(position)
        self.direction = direction

@singleton
class GameState:
    
    def __init__(self):
        self.map_name = "Unknown"
        self.start_timestamp = None
        self.players: List[Player] = []

    def in_work(self):
        return bool(self.start_timestamp)

    def start(self):
        self.start_timestamp = time.time()

    def deserialize(self):
        name = self.map_name.encode() + bytes(10 - len(self.map_name))
        return struct.pack("!10sI", self.map_name, int(time.time()-self.start_timestamp))

    def add_player(self, player: Player):
        self.players.append(player)

    def remove_player(self, player: Player):
        self.players.remove(player)

    def deserialize_players(self, exclude: str):
        retval = struct.pack("B", len(self.players)-1) + b''.\
            join([player.deserialize() for player in self.players if player.nickname != exclude])
        return retval

class ServerProtocol(asyncio.Protocol):

    def __init__(self):
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
        self.gs.remove_player(self.player)
        self.player = None
        peername = self.transport.get_extra_info('peername')
        print('Connection with {} closed'.format(peername))

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


async def main():
    # Get a reference to the event loop as we plan to use
    # low-level APIs.
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ServerProtocol(),
        '127.0.0.1', 8888)

    async with server:
        await server.serve_forever()


asyncio.run(main())