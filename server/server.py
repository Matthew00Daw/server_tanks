import socket
import asyncio


class Server:

    def __init__(self, port: int):
        self.listener = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listener.bind(("localhost", port))
        self.listener.listen(8)
        self.listener.setblocking(False)

    async def handle_new_connection(self, client, address):
        loop = asyncio.get_event_loop()
        print("connection accepted. address: ", address)
        while True:
            in_data = await loop.sock_recv(client, 255)
            if in_data.decode("utf8") == "exit":
                pass
                #break
            await loop.sock_sendall(client, in_data)

        client.close()

    async def run(self):
        loop = asyncio.get_event_loop()
        print("server is running!")
        retval = await loop.sock_accept(self.listener)
        loop.create_task(self.handle_new_connection(*retval))
