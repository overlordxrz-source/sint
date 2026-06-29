import numpy as np
from scipy.signal import spectrogram as scipy_spectrogram

def make_spectrogram(signal: np.ndarray, fs: float = 100,
                     nperseg: int = 64) -> np.ndarray:
    """Returns (freq_bins, time_bins) normalised to [0, 1] for CNN input."""
    _, _, Sxx = scipy_spectrogram(signal, fs=fs, nperseg=nperseg,
                                   noverlap=nperseg // 2)
    Sxx = np.log1p(Sxx)
    Sxx -= Sxx.min()
    denom = Sxx.max()
    return Sxx / denom if denom > 0 else Sxx
