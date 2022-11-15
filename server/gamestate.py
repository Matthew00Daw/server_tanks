import struct
import time
from typing import List

from server.player import Player
from common.util import singleton


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