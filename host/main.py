import asyncio
import uvicorn
from fastapi import FastAPI
from ingest.udp_receiver import receive_loop, RING_BUFFER
from dsp.pipeline import run_pipeline, WINDOW
from features.breathing import extract_breathing
from features.motion import extract_motion
from intelligence.state_machine import StateMachine
from intelligence.fall_detector import FallDetector
from intelligence.alerts import AlertsSystem
from storage.db import init_db
from storage.writer import AsyncBulkWriter
from api.server import app, ws_manager
from api import routes

async def processing_loop():
    writer = AsyncBulkWriter()
    sm = StateMachine()
    fd = FallDetector()
    alerts = AlertsSystem()

    while True:
        await asyncio.sleep(0.1) # 10 Hz processing
        
        if len(RING_BUFFER) < WINDOW:
            continue
            
        frames = list(RING_BUFFER)[-WINDOW:]
        
        try:
            # 1. DSP
            dsp_out = run_pipeline(frames)
            
            # 2. Features
            br = extract_breathing(dsp_out["breathing"], dsp_out["fs"])
            mo = extract_motion(dsp_out["amp"])
            
            # 3. Intelligence
            fall = fd.update(mo["energy"])
            anomaly_score = 0.9 if fall else 0.0 # Mocking AE for now
            
            vitals = {
                "ts": frames[-1].timestamp_ms / 1000.0,
                "breathing_bpm": br["bpm"],
                "breathing_confidence": br["confidence"],
                "motion_energy": mo["energy"],
                "anomaly_score": anomaly_score,
            }
            
            state = sm.update(vitals)
            vitals["state"] = state.value
            
            # 4. Alerts
            new_alerts = alerts.process(vitals, state.value)
            
            # 5. Global State Update
            routes.global_vitals = vitals
            routes.global_status["frames_processed"] += WINDOW
            
            # 6. Broadcast & Storage
            await ws_manager.broadcast({"vitals": vitals, "alerts": new_alerts})
            await writer.add_vital(vitals)
            
        except Exception as e:
            routes.global_status["errors"] += 1
            print(f"Processing error: {e}")

async def main():
    await init_db()
    # Start background loops
    asyncio.create_task(receive_loop(port=5005))
    asyncio.create_task(processing_loop())
    
    # Run FastAPI
    config = uvicorn.Config(app, host="0.0.0.0", port=8000, log_level="info")
    server = uvicorn.Server(config)
    await server.serve()

if __name__ == "__main__":
    asyncio.run(main())
