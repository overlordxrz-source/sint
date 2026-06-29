from dataclasses import dataclass
import numpy as np
import struct

@dataclass
class CsiFrame:
    timestamp_ms: int
    rssi: float          # dBm (negative)
    noise_floor: float   # dBm (negative)
    channel: int
    subcarriers: np.ndarray  # complex64, shape (n_sc,)

def parse_packet(raw: bytes) -> CsiFrame | None:
    if len(raw) < 12:
        return None
    ts  = struct.unpack_from("<Q", raw, 0)[0]
    rssi  = -float(raw[8])
    noise = -float(raw[9])
    ch    = raw[10]
    n_sc  = raw[11]
    if len(raw) < 12 + n_sc * 2:
        return None
    iq = np.frombuffer(raw[12:12 + n_sc * 2], dtype=np.int8).astype(np.float32)
    I, Q = iq[0::2], iq[1::2]
    return CsiFrame(ts, rssi, noise, ch, (I + 1j * Q).astype(np.complex64))
