from typing import Tuple


class GameState:
    def __init__(self):
        self.timer: float = 0
        self.current_level = None
        self.players: Tuple[str, str, int] = []  # пара ip-адрес, никнейм, score

    def start(self):
        pass

    def stop(self):
        pass

    def add_player(self):
        pass

    def kick_player(self):
        pass
