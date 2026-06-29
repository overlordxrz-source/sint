import asyncio
import socket
from collections import deque
from .csi_parser import parse_packet, CsiFrame

RING_BUFFER: deque[CsiFrame] = deque(maxlen=2000)  # ~20s at 100 Hz

async def receive_loop(host="0.0.0.0", port=5005):
    loop = asyncio.get_event_loop()
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((host, port))
    sock.setblocking(False)
    print(f"Listening for CSI on UDP {port}")
    while True:
        try:
            data = await loop.sock_recv(sock, 512)
            frame = parse_packet(data)
            if frame:
                RING_BUFFER.append(frame)
        except Exception:
            await asyncio.sleep(0.001)
