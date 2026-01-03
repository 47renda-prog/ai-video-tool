# AI Video Tool

A simple video analysis CLI that reports basic metrics such as resolution, duration, average brightness, motion score, and scene change count.

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```bash
python -m video_analyzer.cli path/to/video.mp4 --pretty
```

### Options

- `--sample-rate`: Seconds between sampled frames (default: 1.0)
- `--scene-threshold`: Threshold for scene change detection (default: 25.0)
- `--pretty`: Pretty-print JSON output
