import struct
from enum import Enum
from typing import Tuple, Union


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

class ErrorType(Enum):
    NO_ERROR = 0
    VALUE_ERROR = 1


class NetworkPackageBuilder:

    def __init__(self):
        self.package_type = None
        self.action_type = None
        self.data = b''
        self.data_length = 0
        pass

    def set_package(self, type: PackageType):
        self.package_type = type.value

    def set_action(self, type: Union[ActionType, CommandType, RequestType, ErrorType]):
        self.action_type = type.value

    def set_data(self, format: str, *data):
        self.data = struct.pack(format, *data)
        self.data_length = len(self.data)

    def set_raw_data(self, data: bytes):
        self.data_length = len(data)
        self.data = data

    def build(self):
        return struct.pack("!BBB", self.package_type, self.action_type, self.data_length) + self.data

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
        data = data.encode() + bytes(10-len(data))
        format, value = self.make_header()
        return struct.pack(format + "BB10s", value, PackageType.COMMAND.value, type.value, data)

    def make_action(self, type: ActionType, position: Tuple[float, float]):
        format, value = self.make_header()
        return struct.pack(format + "BBff", value, PackageType.ACTION.value, type.value, *position)
