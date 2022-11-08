import struct
from enum import Enum
from typing import Tuple


class ActionType(Enum):
    MOVE = 0
    MOVE_RIGHT = 1
    MOVE_LEFT = 2
    MOVE_UP = 3
    MOVE_DOWN = 4
    FIRE = 5


class PackageType(Enum):
    COMMAND = 1
    ACTION = 2
    REQUEST = 3


class CommandType(Enum):
    CONNECT = 1
    DISCONNECT = 2
    RESPAWN = 3


class RequestType(Enum):
    POSITIONS = 1
    GAME_STATE = 2
    LEVEL_DESTRUCTION = 3


class PackageManager:

    def __init__(self, client_info):
        self.info = client_info
        pass

    def make_header(self):
        return "!c", b'0'

    def make_request(self, type: RequestType):
        format, value = self.make_header()
        return struct.pack(format + "BB", value, PackageType.REQUEST.value, type.value)

    def make_command(self, type: CommandType, data):
        data = data.encode() + bytes(10 - len(data))
        format, value = self.make_header()
        return struct.pack(format + "BB10s", value, PackageType.COMMAND.value, type.value, data)

    def make_action(self, type: ActionType, position: Tuple[float, float], angle: int):
        format, value = self.make_header()
        return struct.pack(format + "BBffB", value, PackageType.ACTION.value, type.value, *position, angle)


class ServerPackageManager:
    pass
