import numpy as np
from scipy.signal import periodogram

def extract_breathing(signal: np.ndarray, fs: float = 100) -> dict:
    freqs, psd = periodogram(signal, fs=fs)
    mask = (freqs >= 0.1) & (freqs <= 0.5)
    if not mask.any():
        return {"bpm": 0.0, "confidence": 0.0}
    peak_idx  = np.argmax(psd[mask])
    peak_freq = freqs[mask][peak_idx]
    bpm       = peak_freq * 60
    confidence = float(psd[mask].max() / (psd.sum() + 1e-9))
    return {"bpm": float(bpm), "confidence": confidence}
