import numpy as np
from .phase_sanitize import sanitize_phase
from .hampel import hampel_filter
from .clutter import remove_clutter
from .bandpass import bandpass

WINDOW = 200    # frames (~2 s at 100 Hz)
FS = 100        # Hz (target sample rate)

def run_pipeline(frames: list) -> dict:
    """
    Input:  list of CsiFrame, length >= WINDOW
    Output: dict with cleaned amplitude+phase arrays and bandpassed signals
    """
    recent = frames[-WINDOW:]
    # Stack to (n_frames, n_subcarriers) complex matrix
    X = np.stack([f.subcarriers for f in recent])          # (200, 52)

    amp   = np.abs(X)
    phase = np.angle(X)

    # Stage 1: phase sanitize
    phase = sanitize_phase(phase)

    # Stage 2: Hampel on amplitude (per subcarrier)
    amp = np.apply_along_axis(hampel_filter, 0, amp)

    # Stage 3: SVD static clutter removal on amplitude
    amp = remove_clutter(amp)

    # Stage 4: Bandpass
    breathing_signal = bandpass(amp, FS, low=0.1, high=0.5)
    heart_signal     = bandpass(amp, FS, low=0.8, high=2.0)

    return {
        "amp": amp,
        "phase": phase,
        "breathing": breathing_signal,
        "heart": heart_signal,
        "fs": FS,
    }
