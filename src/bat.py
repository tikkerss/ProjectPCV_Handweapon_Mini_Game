import cv2 as cv
import numpy as np
import os

from utils import overlay_sprite

BAT_MIN      = 130
BAT_MAX      = 280
SIZE_BAT_FAC = 0.30


def load_base_sprite(filename="../assets/bat.png"):
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)
    sprite = cv.imread(full_path, cv.IMREAD_UNCHANGED)
    if sprite is None:
        print(f"ERROR: {full_path} tidak ditemukan!")
        exit()
    return sprite

base_sprite = load_base_sprite()


def make_sprite(length):
    h_asli, w_asli = base_sprite.shape[:2]
    h_baru = length
    w_baru = max(1, int(w_asli * length / h_asli))
    return cv.resize(base_sprite, (w_baru, h_baru), interpolation=cv.INTER_LINEAR)


class Bat:
    def __init__(self):
        self.sizebat = 190.0
        self._cache = {}
        self.hit_radius = 45

    def update_size(self, hand_area, hand_min=2000, hand_max=10000, size_min=180, size_max=350):
        t = max(0.0, min(1.0, (hand_area - hand_min) /
                                          max(1, hand_max - hand_min)))
        target       = size_min + (size_max - size_min) * t
        self.sizebat = SIZE_BAT_FAC * target + (1 - SIZE_BAT_FAC) * self.sizebat
        self.hit_radius = int(self.sizebat) // 3

    def get_sprite(self, length):
        length = max(BAT_MIN, min(BAT_MAX, (length // 5) * 5))
        if length not in self._cache:
            self._cache[length] = make_sprite(length)
            if len(self._cache) > 40:
                del self._cache[next(iter(self._cache))]
        return self._cache[length]

    def draw(self, frame, cx, cy):
        sprite = self.get_sprite(int(self.sizebat))
        sh, sw = sprite.shape[:2]
        overlay_sprite(frame, sprite, cx - int(sw * 0.20), cy - int(sh * 0.85))
        cv.circle(frame, (cx, cy), 4, (0, 255, 100), -1)

    def reset(self):
        self.sizebat = 190.0