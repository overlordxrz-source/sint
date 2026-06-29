CREATE TABLE IF NOT EXISTS vitals (
    ts                   REAL PRIMARY KEY,
    breathing_bpm        REAL,
    heart_bpm            REAL,
    breathing_confidence REAL,
    motion_energy        REAL,
    activity             TEXT,
    sleep_stage          TEXT,
    anomaly_score        REAL,
    state                TEXT
);

CREATE TABLE IF NOT EXISTS events (
    ts       REAL,
    type     TEXT,
    severity TEXT,
    payload  TEXT   -- JSON blob
);

CREATE TABLE IF NOT EXISTS csi_raw (
    ts          REAL,
    subcarriers BLOB   -- np.ndarray.tobytes(), dtype complex64
);

CREATE INDEX IF NOT EXISTS idx_vitals_ts  ON vitals (ts);
CREATE INDEX IF NOT EXISTS idx_events_ts  ON events (ts);
