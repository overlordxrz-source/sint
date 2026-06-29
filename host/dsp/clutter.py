import numpy as np

def remove_clutter(amp: np.ndarray) -> np.ndarray:
    """Remove static component via SVD (zero largest singular value)."""
    U, S, Vt = np.linalg.svd(amp, full_matrices=False)
    S[0] = 0.0
    return U @ np.diag(S) @ Vt
