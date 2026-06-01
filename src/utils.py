import numpy as np

FRAME_W = 0
FRAME_H = 0
FPS     = 30

ROI_X1 = 0
ROI_Y1 = 0
ROI_X2 = 0
ROI_Y2 = 0
ROI_W  = 0
ROI_H  = 0


def init_roi(frame_w, frame_h):
    global FRAME_W, FRAME_H
    global ROI_X1, ROI_Y1, ROI_X2, ROI_Y2, ROI_W, ROI_H

    FRAME_W = frame_w
    FRAME_H = frame_h
    ROI_X1  = int(FRAME_W * 0.35)
    ROI_Y1  = int(FRAME_H * 0.05)
    ROI_X2  = FRAME_W - 5
    ROI_Y2  = FRAME_H - 5
    ROI_W   = ROI_X2 - ROI_X1
    ROI_H   = ROI_Y2 - ROI_Y1

def erosion(img):
    out = np.zeros_like(img)
    h, w = img.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if np.all(img[y-1:y+2, x-1:x+2]):
                out[y, x] = 255
    return out


def dilation(img):
    out = np.zeros_like(img)
    h, w = img.shape
    for y in range(1, h - 1):
        for x in range(1, w - 1):
            if np.any(img[y-1:y+2, x-1:x+2]):
                out[y, x] = 255
    return out


def opening(img):
    return dilation(erosion(img))


def closing(img):
    return erosion(dilation(img))


#alpha blending manual
def overlay_sprite(bg, sprite, xp, yp):
    sh, sw = sprite.shape[:2]
    bh, bw = bg.shape[:2]

    x1 = max(0, xp);  y1 = max(0, yp)
    x2 = min(bw, xp + sw); y2 = min(bh, yp + sh)
    if x2 <= x1 or y2 <= y1:
        return

    sx1 = x1 - xp; sy1 = y1 - yp
    sx2 = sx1 + (x2 - x1); sy2 = sy1 + (y2 - y1)

    alpha = sprite[sy1:sy2, sx1:sx2, 3] / 255.0
    for c in range(3):
        bg[y1:y2, x1:x2, c] = (alpha * sprite[sy1:sy2, sx1:sx2, c] + (1 - alpha) * bg[y1:y2, x1:x2, c]).astype(np.uint8)