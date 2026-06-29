from collections import deque
import numpy as np

class FallDetector:
    def __init__(self, energy_threshold=2.0, stillness_threshold=0.01, frames_to_wait=500):
        self.energy_threshold = energy_threshold
        self.stillness_threshold = stillness_threshold
        self.frames_to_wait = frames_to_wait
        self.energy_history = deque(maxlen=frames_to_wait)
        self.fall_suspected_frame = -1
        self.frame_count = 0

    def update(self, energy: float) -> bool:
        self.frame_count += 1
        self.energy_history.append(energy)

        if energy > self.energy_threshold:
            self.fall_suspected_frame = self.frame_count

        if self.fall_suspected_frame > 0 and self.frame_count - self.fall_suspected_frame >= self.frames_to_wait:
            recent_energy = list(self.energy_history)[-self.frames_to_wait//2:]
            if np.mean(recent_energy) < self.stillness_threshold:
                # Sustained stillness after a spike!
                self.fall_suspected_frame = -1
                return True
            else:
                self.fall_suspected_frame = -1

        return False
