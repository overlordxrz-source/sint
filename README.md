# WiFi CSI Sensing Stack

A complete, end-to-end WiFi Channel State Information (CSI) sensing system. 

This project uses an ESP32-S3 to capture subcarrier-level WiFi signal distortions caused by human movement. The raw CSI data is streamed over UDP to a Python host, where it undergoes a strict Digital Signal Processing (DSP) pipeline. The cleaned data is then passed through Machine Learning models to extract vital signs (breathing, heart rate), track room occupancy, detect falls, and classify sleep stages. 

Everything is visualized on a real-time React dashboard.

## System Architecture

The stack is heavily decoupled into 6 distinct phases:

1. **Firmware (`firmware/`)**: ESP-IDF C code that configures the ESP32-S3 to capture raw CSI frames and broadcast them as lightweight UDP packets.
2. **Ingestion (`host/ingest/`)**: High-speed asynchronous Python UDP receiver and binary struct parser.
3. **DSP Pipeline (`host/dsp/`)**: Applies Phase Unrolling, Linear Trend Removal, Hampel Filtering (outlier rejection), SVD Clutter Removal (static environment rejection), and Butterworth Bandpass filtering.
4. **Machine Learning (`scripts/` & `host/features/`)**: 
    - **ActivityCNN**: Classifies activities from CSI spectrograms.
    - **HeartLSTM**: Tracks periodic heartbeats from sequential data.
    - **CsiAE**: Autoencoder for anomaly and fall detection.
5. **Intelligence Engine (`host/intelligence/`)**: State machine handling room occupancy (EMPTY, PRESENT, ACTIVE, SLEEPING) and critical alerts.
6. **Dashboard (`ui/`)**: A Vite + React frontend providing a live WebSocket stream of vitals and historical sleep reports.

## Prerequisites

- An **ESP32-S3** development board.
- A 2.4 GHz WiFi router (transmitting beacon frames).
- **Docker** (optional, for building the ESP32 firmware without installing ESP-IDF locally).
- **Python 3.10+**
- **Node.js 18+**

## Quick Start

### 1. Build and Flash the Firmware
The firmware is hardcoded to connect to your WiFi and send UDP packets to your host machine's IP address.

If you have ESP-IDF installed:
```bash
cd firmware
idf.py set-target esp32s3
idf.py build
idf.py -p /dev/cu.usbmodemXXXX flash monitor
```

*Alternatively, you can build it using Docker:*
```bash
docker run --rm -v $PWD/firmware:/project -w /project espressif/idf:release-v5.2 /bin/bash -c "idf.py set-target esp32s3 && idf.py build"
```

### 2. Start the Python Backend
Install the required dependencies and start the ingestion server, DSP pipeline, and FastAPI backend:

```bash
cd host
pip install numpy scipy h5py fastapi uvicorn aiosqlite torch
python main.py
```
*The backend will listen for UDP packets on port 5005 and serve the WebSocket API on port 8000.*

### 3. Start the React UI
Launch the Vite development server to view the real-time dashboard:

```bash
cd ui
npm install
npm run dev
```

Open `http://localhost:5173` in your browser.

## Repository Structure

```
wifi-csi-stack/
├── firmware/                  # ESP32-S3 C firmware (ESP-IDF)
│   ├── main/
│   │   ├── main.c             # WiFi init and CSI config
│   │   ├── csi_handler.c      # CSI callback and UDP broadcasting
│   │   └── csi_handler.h
│   └── CMakeLists.txt
├── host/                      # Python Backend
│   ├── main.py                # Main orchestrator loop
│   ├── ingest/                # UDP Receiver and Parser
│   ├── dsp/                   # Signal Processing Pipeline (Hampel, SVD, Bandpass)
│   ├── features/              # Breathing, Motion, and Spectrogram extraction
│   ├── intelligence/          # State Machine and Fall Detection
│   ├── api/                   # FastAPI Server and WebSocket Manager
│   └── storage/               # SQLite Async Writer
├── scripts/                   # CLI Tools
│   ├── collect_dataset.py     # Dump raw CSI to .h5 for ML training
│   └── train_models.py        # PyTorch model definitions
└── ui/                        # React Dashboard (Vite)
    ├── src/
    │   ├── App.jsx            # Main dashboard layout
    │   └── components/        # VitalSigns, ActivityFeed, SleepReport
    └── package.json
```
