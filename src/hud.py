import cv2 as cv
import math

from utils import ROI_X1, ROI_Y1, ROI_W, ROI_H, FPS


def draw_hud(frame, score, lives):
    H, W = frame.shape[:2]
    ov   = frame.copy()
    cv.rectangle(ov, (0, 0), (W, 60), (10, 10, 10), -1)
    cv.addWeighted(ov, 0.65, frame, 0.35, 0, frame)

    cv.putText(frame, f"SCORE  {score:05d}", (14, 40),
               cv.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

    lx = W - 185
    for i in range(lives):
        cv.circle(frame, (lx + 78 + i*26, 30), 9, (0, 0, 255), -1)

def draw_popups(frame, popups):
    keep = []
    for pop in popups:
        txt, px, py, timer = pop
        cv.putText(frame, txt, (px - 20, py - 8),
                   cv.FONT_HERSHEY_DUPLEX, 0.85, (0, 255, 190), 2)
        pop[3] -= 1
        if pop[3] > 0:
            keep.append(pop)
    return keep


def draw_pitch_wait(frame, pitch_waiting):
    secs = math.ceil(pitch_waiting / FPS)
    msg  = f"Next pitch in {secs}..."
    (tw, _), _ = cv.getTextSize(msg, cv.FONT_HERSHEY_DUPLEX, 0.85, 2)
    cv.putText(frame, msg,
               (ROI_X1 + (ROI_W - tw)//2, ROI_Y1 + ROI_H//2),
               cv.FONT_HERSHEY_DUPLEX, 0.85, (0, 200, 255), 2)


def draw_intro(frame, roi_box):
    H, W = frame.shape[:2]
    ov   = frame.copy()
    cv.rectangle(ov, (0, 0), (W, H), (0, 0, 0), -1)
    cv.addWeighted(ov, 0.55, frame, 0.45, 0, frame)

    x1, y1, x2, y2 = roi_box
    cv.rectangle(frame, (x1, y1), (x2, y2), (0, 200, 255), 2)

    lines = [
        ("KASTI TRAINING SIMULATOR",             1.0, (0, 230, 255), 2),
        ("Stand OUTSIDE the yellow box",          0.7, (255, 255, 255), 1),
        ("Use your RIGHT hand and green gloves to swing the bat!", 0.65, (255, 255, 255), 1),
        ("Position your waist at the bottom of the screen", 0.6, (255, 255, 255), 1),
    ]
    y = H//2 - 70
    for text, fs, col, bold in lines:
        (tw, _), _ = cv.getTextSize(text, cv.FONT_HERSHEY_DUPLEX, fs, bold)
        cv.putText(frame, text, (W//2 - tw//2, y), cv.FONT_HERSHEY_DUPLEX, fs, col, bold)
        y += 45


def draw_countdown(frame, number):
    H, W = frame.shape[:2]
    ov   = frame.copy()
    cv.rectangle(ov, (0, 0), (W, H), (0, 0, 0), -1)
    cv.addWeighted(ov, 0.45, frame, 0.55, 0, frame)

    txt = str(number); fs = 6.0; tk = 12
    (tw, th), _ = cv.getTextSize(txt, cv.FONT_HERSHEY_DUPLEX, fs, tk)
    col = (0, 230, 255) if number > 1 else (0, 255, 80)
    cv.putText(frame, txt, (W//2 - tw//2, H//2 + th//2),
               cv.FONT_HERSHEY_DUPLEX, fs, col, tk)
    cv.putText(frame, "Get ready!", (W//2 - 70, H//2 + th//2 + 55),
               cv.FONT_HERSHEY_SIMPLEX, 0.85, (200, 200, 200), 2)


def draw_gameover(frame, score):
    H, W = frame.shape[:2]
    ov   = frame.copy()
    cv.rectangle(ov, (0, 0), (W, H), (0, 0, 0), -1)
    cv.addWeighted(ov, 0.72, frame, 0.28, 0, frame)

    cv.putText(frame, "GAME OVER", (W//2 - 160, H//2 - 30),
               cv.FONT_HERSHEY_DUPLEX, 2.0, (50, 80, 255), 4)
    cv.putText(frame, f"Final Score:  {score}",
               (W//2 - 130, H//2 + 45),
               cv.FONT_HERSHEY_DUPLEX, 1.1, (255, 255, 255), 2)
    cv.putText(frame, "R = restart     Q = quit",
               (W//2 - 155, H//2 + 105),
               cv.FONT_HERSHEY_SIMPLEX, 0.75, (150, 150, 150), 1)