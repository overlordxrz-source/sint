import asyncio
import numpy as np
import h5py
import time
import argparse
from host.ingest.udp_receiver import receive_loop, RING_BUFFER
from host.dsp.pipeline import WINDOW

async def collect_data(label: str, duration: int):
    print(f"Collecting data for label '{label}' for {duration} seconds...")
    print("Starting in 3 seconds...")
    await asyncio.sleep(3)
    
    start = time.time()
    frames = []
    
    while time.time() - start < duration:
        if RING_BUFFER:
            frames.append(RING_BUFFER.popleft())
        await asyncio.sleep(0.001)
        
    print(f"Collected {len(frames)} frames.")
    
    if not frames:
        return
        
    subcarriers = np.stack([f.subcarriers for f in frames])
    
    filename = f"data/dataset_{label}_{int(time.time())}.h5"
    with h5py.File(filename, "w") as f:
        f.create_dataset("subcarriers", data=subcarriers)
        f.create_dataset("label", data=label)
    
    print(f"Saved to {filename}")

async def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--label", type=str, required=True, help="Activity label (e.g., walking, sleeping)")
    parser.add_argument("--duration", type=int, default=60, help="Duration in seconds")
    args = parser.parse_args()
    
    asyncio.create_task(receive_loop())
    await collect_data(args.label, args.duration)

if __name__ == "__main__":
    import os
    os.makedirs("data", exist_ok=True)
    asyncio.run(main())
