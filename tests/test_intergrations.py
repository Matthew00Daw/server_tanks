import asyncio

import pytest

from client.serverinterface import ServerInterface, NotAuthorizedException
from server.protocol import ServerProtocol
from server.gamestate import GameState


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="session")
def server_interface():
    interface = ServerInterface("127.0.0.1", 3888)
    yield interface
    interface.disconnect()


@pytest.mark.asyncio
class TestServerClient:

    async def test_server_startup(self, event_loop):
        async def start_server():
            server = await event_loop.create_server(
        lambda: ServerProtocol(),
        '127.0.0.1', 3888)
            return server.start_serving()
        self.server = await start_server()

    # не интеграционный
    def test_required_connection(self, server_interface):
        with pytest.raises(NotAuthorizedException):
            server_interface.get_gamestate()
    
    def test_login(self, server_interface):
        x, y = server_interface.connect("Roman")
        assert (0 <= x <= 600) and (0 <= y <= 400)
        game_state = GameState()
        assert "Roman" in [player.nickname for player in game_state.players]

    def test_position(self, server_interface):
        direction = 0 # right
        position = (250, 250)
        server_interface.send_position(position, direction)
        game_state = GameState()
        player, = [player for player in game_state.players if player.nickname == "Roman"]
        assert (player.position == position) and (player.direction.value - 1 == direction) # такие вот костыли

    def test_players(self, server_interface):
        another_server_interface = ServerInterface("127.0.0.1", 8888)
        another_server_interface.connect("Robot")
        players = server_interface.get_positions()
        assert "Robot" in players
 
    async def teardown_class(self):
        await asyncio.sleep(2)
        self.server.close()