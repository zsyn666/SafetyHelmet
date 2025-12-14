#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   @File Name:     app.py
   @Author:        zhang
   @Date:          2025/8/6
   @Description:
-------------------------------------------------
"""
from pathlib import Path
import sys

# Get the parent directory of the current file (relative path)
root_path = Path(__file__).parent

# Add the root path to the sys.path list if it is not already there
if root_path not in sys.path:
    sys.path.append(str(root_path))

# Get the root directory path (relative path)
ROOT = root_path


# Source
SOURCES_LIST = ["Image", "Video", "Webcam"]


# DL model config
DETECTION_MODEL_DIR = ROOT / 'weights' / 'detection'
YOLOv8n = DETECTION_MODEL_DIR / "yolov8n.pt"
SafetyHelmetWearing = DETECTION_MODEL_DIR / "SafetyHelmetWearing.pt"

DETECTION_MODEL_LIST = [
    "yolov8n.pt",
    "SafetyHelmetWearing.pt",
 ]
