"""Core analysis logic for video files."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Iterable

import cv2
import numpy as np


@dataclass(frozen=True)
class AnalysisResult:
    path: str
    frame_count: int
    fps: float
    duration_seconds: float
    width: int
    height: int
    avg_brightness: float
    motion_score: float
    scene_changes: int

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass(frozen=True)
class _FrameStats:
    brightness: float
    motion: float
    scene_change: bool


def analyze_video(path: str, sample_rate: float = 1.0, scene_threshold: float = 25.0) -> AnalysisResult:
    """Analyze a video and return aggregate metrics.

    Args:
        path: Path to the video file.
        sample_rate: How many seconds between sampled frames.
        scene_threshold: Threshold for detecting scene changes based on mean diff.
    """
    if sample_rate <= 0:
        raise ValueError("sample_rate must be greater than 0")

    capture = cv2.VideoCapture(path)
    if not capture.isOpened():
        raise FileNotFoundError(f"Unable to open video: {path}")

    fps = capture.get(cv2.CAP_PROP_FPS) or 0.0
    frame_count = int(capture.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH) or 0)
    height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT) or 0)
    duration_seconds = frame_count / fps if fps else 0.0

    sample_step = max(int(fps * sample_rate), 1) if fps else 1

    stats = list(_iterate_frames(capture, sample_step, scene_threshold))
    capture.release()

    if not stats:
        avg_brightness = 0.0
        motion_score = 0.0
        scene_changes = 0
    else:
        avg_brightness = float(np.mean([stat.brightness for stat in stats]))
        motion_score = float(np.mean([stat.motion for stat in stats]))
        scene_changes = sum(1 for stat in stats if stat.scene_change)

    return AnalysisResult(
        path=path,
        frame_count=frame_count,
        fps=fps,
        duration_seconds=duration_seconds,
        width=width,
        height=height,
        avg_brightness=avg_brightness,
        motion_score=motion_score,
        scene_changes=scene_changes,
    )


def _iterate_frames(
    capture: cv2.VideoCapture,
    sample_step: int,
    scene_threshold: float,
) -> Iterable[_FrameStats]:
    previous_gray = None
    index = 0

    while True:
        success, frame = capture.read()
        if not success:
            break

        if index % sample_step != 0:
            index += 1
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        brightness = float(np.mean(gray))

        if previous_gray is None:
            motion = 0.0
            scene_change = False
        else:
            diff = cv2.absdiff(gray, previous_gray)
            motion = float(np.mean(diff))
            scene_change = motion >= scene_threshold

        previous_gray = gray
        index += 1

        yield _FrameStats(
            brightness=brightness,
            motion=motion,
            scene_change=scene_change,
        )
