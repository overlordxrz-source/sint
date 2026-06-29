import asyncio
from typing import List, Dict, Any
from .db import get_db

class AsyncBulkWriter:
    def __init__(self, batch_size=10, write_interval_s=5.0):
        self.batch_size = batch_size
        self.write_interval_s = write_interval_s
        self.vitals_buffer = []
        self.events_buffer = []
        self.raw_buffer = []
        self._task = asyncio.create_task(self._writer_loop())

    async def _writer_loop(self):
        while True:
            await asyncio.sleep(self.write_interval_s)
            await self.flush()

    async def add_vital(self, vital: Dict[str, Any]):
        self.vitals_buffer.append(vital)
        if len(self.vitals_buffer) >= self.batch_size:
            await self.flush()

    async def flush(self):
        if not self.vitals_buffer and not self.events_buffer and not self.raw_buffer:
            return

        async with get_db() as db:
            if self.vitals_buffer:
                await db.executemany(
                    "INSERT INTO vitals (ts, breathing_bpm, heart_bpm, breathing_confidence, motion_energy, activity, sleep_stage, anomaly_score, state) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                    [(v["ts"], v.get("breathing_bpm"), v.get("heart_bpm"), v.get("breathing_confidence"), v.get("motion_energy"), v.get("activity"), v.get("sleep_stage"), v.get("anomaly_score"), v.get("state")) for v in self.vitals_buffer]
                )
                self.vitals_buffer.clear()
            await db.commit()
