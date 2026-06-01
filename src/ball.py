import cv2 as cv
import math
import random
import os

from utils import ROI_X1, ROI_Y1, ROI_W, ROI_H, ROI_X2, ROI_Y2, overlay_sprite


def load_ball_sprite(filename="../assets/ball.png"):
    base_dir  = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, filename)
    sprite = cv.imread(full_path, cv.IMREAD_UNCHANGED)
    if sprite is None:
        print(f"ERROR: {full_path} tidak ditemukan!")
        exit()
    return sprite

ball_sprite = load_ball_sprite()


class Ball:
    MIN_R = 4
    MAX_R = 75
    HIT_MIN_R = 32

    def __init__(self):
        cx = ROI_X1 + ROI_W//2 + random.randint(-ROI_W//8, ROI_W//8)
        cy = ROI_Y1 + ROI_H//3 + random.randint(-ROI_H//8, ROI_H//8)
        self.x = float(cx)
        self.y = float(cy)

        tx = ROI_X1 + ROI_W//2 + random.randint(-ROI_W//5, ROI_W//5)
        ty = ROI_Y1 + int(ROI_H * 0.72) + random.randint(-30, 30)

        jarak        = math.hypot(tx - cx, ty - cy) or 1
        kecepatan    = random.uniform(2.0, 3.5)
        self.vx = (tx - cx) / jarak * kecepatan
        self.vy = (ty - cy) / jarak * kecepatan
        
        self.t        = 0.0
        self.active   = True
        self.hit      = False
        self.radius   = self.MIN_R
        self.hittable = False

    def update(self):
        acc     = 1.0 + self.t * 3.5
        self.x += self.vx * acc
        self.y += self.vy * acc
        self.t  = min(1.0, self.t + 0.013)

        self.radius   = int(self.MIN_R + (self.MAX_R - self.MIN_R) * (self.t ** 1.4))
        self.hittable = self.radius >= self.HIT_MIN_R

        if (self.x < ROI_X1 - 80 or self.x > ROI_X2 + 80 or self.y < ROI_Y1 - 80 or self.y > ROI_Y2 + 80 or self.t >= 1.0):
            self.active = False

    def draw(self, frame):
        cx, cy = int(self.x), int(self.y)
        r = self.radius

        size    = max(1, r * 2)
        resized = cv.resize(ball_sprite, (size, size), interpolation=cv.INTER_LINEAR)
        overlay_sprite(frame, resized, cx - r, cy - r)

        if self.hittable:
            label = "HIT!"
            fs, th = 0.58, 2
            (tw, tH), bl = cv.getTextSize(label, cv.FONT_HERSHEY_DUPLEX, fs, th)
            lx = cx - tw//2
            ly = cy - r - 10
            p  = 4
            cv.rectangle(frame, (lx-p, ly-tH-p), (lx+tw+p, ly+bl+p), (0, 160,  50), -1)
            cv.rectangle(frame, (lx-p, ly-tH-p), (lx+tw+p, ly+bl+p), (0, 100,  20),  1)
            cv.putText(frame, label, (lx, ly), cv.FONT_HERSHEY_DUPLEX, fs, (255, 255, 255), th)

    def check_hit(self, bx, by, bat_r):
        return (self.hittable and math.hypot(self.x - bx, self.y - by) < (self.radius + bat_r))