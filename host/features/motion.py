import numpy as np
from scipy.stats import entropy as scipy_entropy

def extract_motion(amp: np.ndarray) -> dict:
    """amp: (n_frames, n_subcarriers)"""
    per_sc_var = np.var(amp, axis=0)
    energy = float(per_sc_var.mean())
    # Normalised histogram entropy across subcarriers
    hist, _ = np.histogram(amp.ravel(), bins=64, density=True)
    ent = float(scipy_entropy(hist + 1e-9))
    return {"energy": energy, "entropy": ent, "presence": energy > 0.01}
