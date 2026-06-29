from enum import Enum
import time

class RoomState(Enum):
    EMPTY = "EMPTY"
    PRESENT = "PRESENT"
    ACTIVE = "ACTIVE"
    SLEEPING = "SLEEPING"
    FALLING = "FALLING"

class StateMachine:
    def __init__(self):
        self.state = RoomState.EMPTY
        self.last_active_time = time.time()
        self.last_presence_time = time.time()

    def update(self, vitals: dict) -> RoomState:
        # State machine logic based on motion energy, activity classification, and breathing
        if vitals.get("motion_energy", 0) > 0.05:
            self.last_active_time = time.time()
            self.last_presence_time = time.time()
            self.state = RoomState.ACTIVE
        elif vitals.get("motion_energy", 0) > 0.01:
            self.last_presence_time = time.time()
            self.state = RoomState.PRESENT
        else:
            if time.time() - self.last_presence_time > 60:
                self.state = RoomState.EMPTY
            elif time.time() - self.last_active_time > 300:
                self.state = RoomState.SLEEPING

        # Check for anomalies/falls
        if vitals.get("anomaly_score", 0) > 0.8:
            self.state = RoomState.FALLING

        return self.state
