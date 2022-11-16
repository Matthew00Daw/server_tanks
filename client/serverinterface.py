import socket
import struct
from typing import Tuple

from common.package import NetworkPackageBuilder, PackageType, CommandType, RequestType, ActionType


class NotAuthorizedException(Exception):
    pass

def connection_reqired(func):
    def wrapper(self, *args, **kwargs):
        if self.connected():
            return func(self, *args, **kwargs)
        else:
            raise NotAuthorizedException("Попытка обратиться к серверу до установления подключения!")
    return wrapper

class ServerInterface:

    def __init__(self, host: str, port: int):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.settimeout(5)
        self.is_connected = False
        self.s.connect((host, port))

    def connect(self, nickname: str) -> Tuple[float, float]:
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.COMMAND)
        builder.set_action(CommandType.CONNECT)
        builder.set_raw_data(nickname.encode() + bytes(10-len(nickname)))
        self.s.sendall(builder.build())
        response = self.s.recv(256)
        position = struct.unpack("!ff", response[3:])
        self.is_connected = True
        return position

    def connected(self):
        return self.is_connected
    
    def disconnect(self) -> None:
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.COMMAND)
        builder.set_action(CommandType.DISCONNECT)
        self.s.sendall(builder.build())
        self.s.recv(256)
        self.is_connected = False

    @connection_reqired
    def send_position(self, position, direction):
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.ACTION)
        builder.set_action(ActionType.MOVE)
        builder.set_data("!ffB", *position, direction)
        self.s.sendall(builder.build())
        self.s.recv(256)

    @connection_reqired
    def get_positions(self):
        retval = {}
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.REQUEST)
        builder.set_action(RequestType.POSITIONS)
        self.s.sendall(builder.build())
        response = self.s.recv(256)
        num_tanks = response[3]
        other_tanks = struct.unpack("!"+num_tanks*"10sffBB", response[4:])
        for i in range(num_tanks):
            tank_data = other_tanks[i*5:(i + 1)*5]
            retval[tank_data[0].replace(b"\x00", b"").decode()] = {"position": tank_data[1:3], "is_alive": bool(tank_data[3]), "angle": 90*(tank_data[4]-1)}
        return retval

    @connection_reqired
    def get_gamestate(self):
        pass

    @connection_reqired
    def get_level_destruct(self):
        pass

    @connection_reqired
    def respawn(self):
        builder = NetworkPackageBuilder()
        builder.set_package(PackageType.COMMAND)
        builder.set_action(CommandType.RESPAWN)
        self.s.sendall(builder.build())
        response = self.s.recv(256)
        position = struct.unpack("!ff", response[3:])
        return position