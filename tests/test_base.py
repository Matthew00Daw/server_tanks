import pytest
import asyncio

from server.protocol import ServerProtocol



@pytest.mark.asyncio
class TestAsync:
    async def test_an_async_function(self, event_loop: asyncio.BaseEventLoop):
        async def start_server():
            server = await event_loop.create_server(lambda: ServerProtocol(), "127.0.0.1", 8888)
            await server.start_serving()
            return server
        self.server = await start_server()
        await asyncio.sleep(25)


    async def teardown_class(self):
        self.server.close()