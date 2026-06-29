import time

class AlertsSystem:
    def __init__(self, cooldown_s=60):
        self.cooldown_s = cooldown_s
        self.last_alert_time = {}

    def process(self, vitals: dict, state: str) -> list:
        alerts = []
        now = time.time()

        def _add_alert(alert_type, msg, severity="HIGH"):
            if now - self.last_alert_time.get(alert_type, 0) > self.cooldown_s:
                alerts.append({"type": alert_type, "msg": msg, "severity": severity, "ts": now})
                self.last_alert_time[alert_type] = now

        bpm = vitals.get("breathing_bpm", 0)
        confidence = vitals.get("breathing_confidence", 0)

        if state == "FALLING":
            _add_alert("FALL_DETECTED", "A fall was detected followed by stillness", "CRITICAL")
        
        if state in ("SLEEPING", "ACTIVE", "PRESENT") and confidence > 0.5:
            if bpm < 6:
                _add_alert("LOW_BREATHING", f"Breathing rate critically low: {bpm:.1f} BPM", "CRITICAL")
            elif bpm > 30:
                _add_alert("HIGH_BREATHING", f"Breathing rate critically high: {bpm:.1f} BPM", "CRITICAL")

        return alerts
