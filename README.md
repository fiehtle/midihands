# Hand Gesture to MIDI Control

![Project Status: Active](https://img.shields.io/badge/Project%20Status-Active-green)

This project uses computer vision to detect hand gestures and convert them into MIDI commands for controlling Logic Pro.

## Setup

1. Install Python dependencies:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Configure macOS MIDI:
- Open Audio MIDI Setup
- Enable IAC Driver if not already enabled
- Create a virtual MIDI port if needed

## Usage

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Run the application:
```bash
python src/main.py
```

## Features

- Left hand (1-5 fingers): Select chord/MIDI note
- Right hand (gesture/spacing): Control MIDI CC values
- Real-time webcam feedback
- Low latency performance (≥15 FPS)

## Requirements

- Python 3.9+
- macOS with webcam
- Logic Pro (or other DAW that accepts MIDI input)

## Development Status

Currently implementing:
- [x] Hand detection and finger counting
- [ ] MIDI output integration
- [ ] Gesture-to-MIDI mapping
- [ ] Performance optimization 