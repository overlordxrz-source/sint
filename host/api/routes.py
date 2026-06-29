from fastapi import APIRouter
from typing import Dict, Any

router = APIRouter()

global_status = {
    "uptime": 0,
    "fps": 0,
    "frames_processed": 0,
    "errors": 0
}

global_vitals = {}

@router.get("/status")
async def get_status() -> Dict[str, Any]:
    return global_status

@router.get("/vitals")
async def get_vitals() -> Dict[str, Any]:
    return global_vitals

@router.get("/state")
async def get_state() -> Dict[str, Any]:
    return {
        "state": global_vitals.get("state", "empty"),
        "presence": global_vitals.get("presence", False),
        "activity": global_vitals.get("activity", "unknown"),
        "sleep_stage": global_vitals.get("sleep_stage", None)
    }

@router.get("/history")
async def get_history(hours: int = 8) -> list:
    # TODO: Fetch from SQLite
    return []

@router.get("/config")
async def get_config() -> dict:
    return {}

@router.post("/config")
async def update_config(config: dict) -> dict:
    return {"status": "updated"}

@router.get("/events")
async def get_events(limit: int = 50) -> list:
    # TODO: Fetch from SQLite
    return []
