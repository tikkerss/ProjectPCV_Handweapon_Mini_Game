import cv2 as cv
import numpy as np
import math
from collections import deque

from utils import (ROI_X1, ROI_Y1, ROI_W, ROI_H, opening, closing)


# ─────────────────────────────────────────
#  HAND DETECTOR
# ─────────────────────────────────────────
class HandDetector:
    LOWER = np.array([35,  80,  50])
    UPPER = np.array([85, 255, 255])
    MIN_AREA = 800
    SMOOTH   = 0.6
    GRIP_MIN = 2000
    GRIP_MAX = 10000

    def __init__(self):
        self.detected  = False
        self.cx = None
        self.cy = None
        self.area = 0.0
        self.mask = None
        self.EMAsmooth_x = None
        self.EMAsmooth_y = None
        self._frame_c  = 0
        self.allclean = None
        self.is_gripping = False

    def update(self, frame):
        roi      = frame[ROI_Y1:ROI_Y1+ROI_H, ROI_X1:ROI_X1+ROI_W]
        hsv      = cv.cvtColor(roi, cv.COLOR_BGR2HSV)
        raw_mask = cv.inRange(hsv, self.LOWER, self.UPPER)

        # Morphology tiap 7 frame
        self._frame_c += 1
        if self._frame_c % 7 == 0:
            small       = cv.resize(raw_mask, (80, 80))
            clean       = opening(small)
            clean       = closing(clean)
            self.allclean = cv.resize(clean, (ROI_W, ROI_H))
        if self.allclean is None:
            self.allclean = raw_mask

        self.mask = self.allclean

        contours, _ = cv.findContours(self.allclean, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        self.detected = False
        self.cx = self.cy = None
        self.area = 0.0

        if not contours:
            self.EMAsmooth_x = self.EMAsmooth_y = None
            return

        biggest   = max(contours, key=cv.contourArea)
        self.area = cv.contourArea(biggest)

        if self.area < self.MIN_AREA:
            self.EMAsmooth_x = self.EMAsmooth_y = None
            return

        M = cv.moments(biggest)
        if M["m00"] == 0:
            return

        center_x = int(M["m10"] / M["m00"])
        center_y = int(M["m01"] / M["m00"])

        if self.EMAsmooth_x is None:
            self.EMAsmooth_x, self.EMAsmooth_y = center_x, center_y
        else:
            self.EMAsmooth_x = int(self.SMOOTH * center_x + (1 - self.SMOOTH) * self.EMAsmooth_x)
            self.EMAsmooth_y = int(self.SMOOTH * center_y + (1 - self.SMOOTH) * self.EMAsmooth_y)

        self.cx  = ROI_X1 + self.EMAsmooth_x
        self.cy  = ROI_Y1 + self.EMAsmooth_y
        self.detected = True
        self.is_gripping = self.GRIP_MIN < self.area < self.GRIP_MAX

    def reset(self):
        self.EMAsmooth_x = self.EMAsmooth_y = None
        self.allclean    = None
        self._frame_c  = 0
        self.detected  = False
        self.cx = self.cy = None
        self.area = 0.0


# swing detector
class SwingDetector:
    SWING_THR = 40
    COOLDOWN  = 25

    def __init__(self):
        self.history   = deque(maxlen=5)
        self._cooldown = 0
        self.is_active = False

    def update(self, cx, cy):
        self.history.append((cx, cy))
        self._cooldown = max(0, self._cooldown - 1)
        self.is_active = self._cooldown > 0

        if len(self.history) < 2:
            return False

        h  = list(self.history)
        dx = h[-1][0] - h[0][0]
        dy = h[-1][1] - h[0][1]

        if math.hypot(dx, dy) >= self.SWING_THR:
            self._cooldown = self.COOLDOWN
            self.is_active = True
            return True

        return False

    def reset(self):
        self.history.clear()
        self._cooldown = 0
        self.is_active = False