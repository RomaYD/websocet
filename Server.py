import asyncio
import logging
import websockets
from websockets import WebSocketClientProtocol

logging.basicConfig(level=logging.INFO)


class Server:
    set_clients = set()

    async def registration(self, ws: WebSocketClientProtocol) -> None:
        self.set_clients.add(ws)
        logging.info(f'{ws.remote_address} connects.')

    async def unregistration(self, ws: WebSocketClientProtocol) -> None:
        self.set_clients.remove(ws)
        logging.info(f'{ws.remote_address} disconnects.')

    async def send_method(self, message: str) -> None:
        print(message)
        if self.set_clients:
            await asyncio.wait([user.send(message) for user in self.set_clients])

    async def ws_head(self, ws: WebSocketClientProtocol, url: str) -> None:
        await self.registration(ws)
        try:
            await self.destribute(ws)
        finally:
            await self.unregistration(ws)

    async def destribute(self, ws: WebSocketClientProtocol) -> None:
        async for mes in ws:
            await self.send_method(mes)


server = Server()

start = websockets.serve(server.ws_head, '0.0.0.0', 80)
loop = asyncio.get_event_loop()
loop.run_until_complete(start)
loop.run_forever()
