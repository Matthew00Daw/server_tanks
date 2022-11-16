import asyncio
import subprocess
import time

import pytest

from client.serverinterface import ServerInterface, NotAuthorizedException
from server.protocol import ServerProtocol
from server.gamestate import GameState


@pytest.fixture(scope="session")
def server():
    server = subprocess.Popen("python ./gameserver.py")
    yield server
    server.terminate()

@pytest.fixture(scope="session")
def server_interface():
    interface = ServerInterface("127.0.0.1", 8888)
    yield interface
    interface.disconnect()

@pytest.fixture(scope="session")
def another_server_interface():
    interface = ServerInterface("127.0.0.1", 8888)
    interface.connect("Robot")
    yield interface
    interface.disconnect()


class TestServerClient:

    # не интеграционный
    def test_required_connection(self, server_interface):
        with pytest.raises(NotAuthorizedException):
            server_interface.get_gamestate()
    
    def test_login(self, server_interface):
        x, y = server_interface.connect("Roman")
        assert (0 <= x <= 600) and (0 <= y <= 400)

    def test_position(self, server_interface, another_server_interface):

        direction = 0 # right
        position = (250.0, 250.0)
        server_interface.send_position(position, direction)

        players = another_server_interface.get_positions()
        assert players.get("Roman") is not None
        player = players.get("Roman")
        assert (player.get("position") == position) and (player.get("angle") == direction) # такие вот костыли

    def test_players(self, server_interface, another_server_interface):
        players = server_interface.get_positions()
        assert "Robot" in players


    def test_disconnect(self, server_interface, another_server_interface):
        
        another_server_interface.disconnect()
        players = server_interface.get_positions()
        assert "Robot" not in players