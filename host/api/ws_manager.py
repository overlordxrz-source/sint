from fastapi import WebSocket
from typing import List

class WSManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, ws: WebSocket):
        await ws.accept()
        self.active_connections.append(ws)

    def disconnect(self, ws: WebSocket):
        if ws in self.active_connections:
            self.active_connections.remove(ws)

    async def broadcast(self, payload: dict):
        for connection in self.active_connections:
            try:
                await connection.send_json(payload)
            except Exception:
                pass
