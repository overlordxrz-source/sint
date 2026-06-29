import numpy as np

def hampel_filter(x: np.ndarray, k: int = 5, n_sigma: float = 3.0) -> np.ndarray:
    """1-D Hampel identifier. Replaces outliers with rolling median."""
    x = x.copy()
    for i in range(k, len(x) - k):
        window = x[i - k:i + k + 1]
        med = np.median(window)
        mad = np.median(np.abs(window - med))
        if abs(x[i] - med) > n_sigma * 1.4826 * mad:
            x[i] = med
    return x
