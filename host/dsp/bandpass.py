import numpy as np
from scipy.signal import butter, sosfiltfilt

def bandpass(amp: np.ndarray, fs: float, low: float, high: float,
             order: int = 4) -> np.ndarray:
    """
    Apply bandpass to each subcarrier, return best subcarrier signal.
    Best = highest in-band SNR.
    """
    sos = butter(order, [low, high], btype="band", fs=fs, output="sos")
    filtered = np.apply_along_axis(lambda col: sosfiltfilt(sos, col), 0, amp)
    # Select subcarrier with highest in-band energy ratio
    in_band_energy = np.var(filtered, axis=0)
    best_sc = np.argmax(in_band_energy)
    return filtered[:, best_sc]
