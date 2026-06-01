import cv2 as cv
import numpy as np
import math
import os

from utils import overlay_sprite

BAT_MIN = 130
BAT_MAX = 280

ANGLE_READY =  0.0
ANGLE_SWING = -45.0
EMA_ANGLE_SPEED =  0.35
EMA_SIZE_BAT    = 0.20


def load_base_sprite(filename="../assets/bat.png"):
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)
    sprite = cv.imread(full_path, cv.IMREAD_UNCHANGED)
    if sprite is None:
        print(f"ERROR: {full_path} tidak ditemukan!")
        exit()
    return sprite

base_sprite = load_base_sprite()


def make_sprite(length, angle_deg):
    bh, bw = base_sprite.shape[:2]

    new_h   = length
    new_w   = max(1, int(bw * length / bh))
    resized = cv.resize(base_sprite , (new_w, new_h), interpolation=cv.INTER_LINEAR)

    diag = int(math.hypot(new_w, new_h)) + 20
    px   = (diag - new_w) // 2
    py   = (diag - new_h) // 2
    pad  = np.zeros((diag, diag, 4), dtype=np.uint8)
    pad[py:py+new_h, px:px+new_w] = resized

    center  = (diag // 2, diag // 2)
    M_rot   = cv.getRotationMatrix2D(center, angle_deg, 1.0)
    rotated = cv.warpAffine(pad, M_rot, (diag, diag), flags=cv.INTER_LINEAR, borderMode=cv.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))

    ach  = rotated[:, :, 3]
    rows = np.any(ach > 0, axis=1)
    cols = np.any(ach > 0, axis=0)
    if not rows.any():
        return rotated

    r0, r1 = np.where(rows)[0][[0, -1]]
    c0, c1 = np.where(cols)[0][[0, -1]]
    return rotated[r0:r1+1, c0:c1+1]


class Bat:
    def __init__(self):
        self.size  = 190.0
        self.angle = ANGLE_READY
        self._cache = {}
        self.hit_radius = 45

    def update_size(self, hand_area,hand_min=1000, hand_max=20000, size_min=130,  size_max=280):
        t = max(0.0, min(1.0, (hand_area - hand_min) /
                                          max(1, hand_max - hand_min)))
        target = size_min + (size_max - size_min) * t    
        self.size = EMA_SIZE_BAT * target + (1 - EMA_SIZE_BAT) * self.size
        self.hit_radius = int(self.size) // 3

    def update_angle(self, swinging):
        target      = ANGLE_SWING if swinging else ANGLE_READY
        self.angle = self.angle + EMA_ANGLE_SPEED * (target - self.angle)


    def get_sprite(self, length, angle):
        length = max(BAT_MIN, min(BAT_MAX, (length // 5) * 5))
        key    = (length, angle)
        if key not in self._cache:
            self._cache[key] = make_sprite(length, angle)  # tidak return tuple lagi
            if len(self._cache) > 40:
                del self._cache[next(iter(self._cache))]
        return self._cache[key]

    def draw(self, frame, cx, cy):
        sprite = self.get_sprite(int(self.size), int(self.angle))
        sh, sw = sprite.shape[:2]
        overlay_sprite(frame, sprite, cx - int(sw * 0.20), cy - int(sh * 0.85))
        cv.circle(frame, (cx, cy), 4, (0, 255, 100), -1)

    def reset(self):
        self.size  = 190.0
        self.angle = ANGLE_READY