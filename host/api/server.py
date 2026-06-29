import asyncio
import json
import time
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from .ws_manager import WSManager
from .routes import router

app = FastAPI(title="WiFi CSI Sensing Stack")
app.add_middleware(CORSMiddleware, allow_origins=["*"])
app.include_router(router)
ws_manager = WSManager()

@app.websocket("/stream")
async def ws_endpoint(ws: WebSocket):
    await ws_manager.connect(ws)
    try:
        while True:
            await asyncio.sleep(0.5)  # keepalive
    except WebSocketDisconnect:
        ws_manager.disconnect(ws)
