# Copyright (c) 2025 marine
# Licensed under the MIT License.
# This file is part of chikooMusic
#CHIKOO-CODER

import shutil
from pathlib import Path

from chikoo import logger


def ensure_dirs():
    """
    Ensure that the necessary directories exist.
    """
    if not shutil.which("ffmpeg"):
        raise RuntimeError("FFmpeg must be installed and accessible in the system PATH.")

    for dir in ["cache", "downloads"]:
        Path(dir).mkdir(parents=True, exist_ok=True)
    logger.info("Cache directories updated.")
