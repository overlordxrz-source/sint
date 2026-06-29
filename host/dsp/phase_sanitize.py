import numpy as np

def sanitize_phase(phase: np.ndarray) -> np.ndarray:
    """phase: (n_frames, n_subcarriers)"""
    # Unwrap per subcarrier
    unwrapped = np.unwrap(phase, axis=0)
    # Remove linear trend (caused by CFO/STO offsets)
    t = np.arange(len(phase))
    for sc in range(phase.shape[1]):
        coeffs = np.polyfit(t, unwrapped[:, sc], 1)
        unwrapped[:, sc] -= np.polyval(coeffs, t)
    return unwrapped
