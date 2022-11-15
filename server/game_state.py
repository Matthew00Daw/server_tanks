from enum import Enum
from typing import Tuple, List


class State(Enum):
    Stop = 1
    Running = 2
    Pause = 3


class GameState:
    def __init__(self):
        self.timer: float = 0
        self.current_level = None
        self.state = State.Stop
        self.players: List[Tuple[str, str, int]] = []  # пара ip-адрес, никнейм, score

    def start(self, level):
        self.state = State.Running
        self.current_level = level

    def stop(self):
        self.state = State.Stop
        self.current_level = None

    def add_player(self, ip, nickname):
        self.players.append((ip, nickname, 0))

    def kick_player(self, nickname):
        self.players.remove(*[player for player in self.players
                              if player[1] == nickname])

