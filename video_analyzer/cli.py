"""Command line interface for the video analyzer."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from video_analyzer.analyzer import analyze_video


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Analyze a video file and report metrics.")
    parser.add_argument("path", type=Path, help="Path to the video file")
    parser.add_argument(
        "--sample-rate",
        type=float,
        default=1.0,
        help="Seconds between sampled frames (default: 1.0)",
    )
    parser.add_argument(
        "--scene-threshold",
        type=float,
        default=25.0,
        help="Threshold for scene change detection (default: 25.0)",
    )
    parser.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON output",
    )
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    result = analyze_video(
        str(args.path),
        sample_rate=args.sample_rate,
        scene_threshold=args.scene_threshold,
    )

    output = result.to_dict()
    if args.pretty:
        print(json.dumps(output, indent=2))
    else:
        print(json.dumps(output))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
