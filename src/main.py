import cv2 as cv
import numpy as np

#init camera
cam = cv.VideoCapture(0)
if not cam.isOpened():
    print("ERROR: Camera not found."); exit()
ret, tmp = cam.read()
if not ret:
    print("ERROR: Cannot read frame."); exit()
FRAME_H, FRAME_W = tmp.shape[:2]

# init ROI
import utils
utils.init_roi(FRAME_W, FRAME_H) #kirim nilai ke utils 

from utils    import ROI_X1, ROI_Y1, ROI_X2, ROI_Y2,  FPS
from detector import HandDetector
from bat      import Bat
from ball     import Ball
import hud

INTRO_FRAMES   = FPS * 5
COUNTDOWN_SECS = 3

hand_det  = HandDetector()
bat       = Bat()

score     = 0
lives     = 3
game_over = False

balls         = []
pitch_waiting = 0
PITCH_DELAY   = 80

popups = []

state = "intro"
intro_timer = INTRO_FRAMES
countdown_num = COUNTDOWN_SECS
countdown_timer = FPS

ROI_BOX = (ROI_X1, ROI_Y1, ROI_X2, ROI_Y2)

def reset_game():
    global score, lives, game_over
    global balls, pitch_waiting, popups
    global state, intro_timer, countdown_num, countdown_timer

    score = 0
    lives = 3; game_over = False
    balls.clear(); popups.clear()
    pitch_waiting = 0

    hand_det.reset()
    bat.reset()

    state = "countdown"
    countdown_num   = COUNTDOWN_SECS
    countdown_timer = FPS

#main loop
while True:
    ret, frame = cam.read()
    if not ret:     
        break
    frame = cv.flip(frame, 1)

    # intro
    if state == "intro":
        hud.draw_intro(frame, ROI_BOX)  
        cv.imshow("Kasti Training Simulator", frame)
        cv.waitKey(1)
        intro_timer -= 1
        if intro_timer <= 0:
            state           = "countdown"
            countdown_num   = COUNTDOWN_SECS
            countdown_timer = FPS
        continue

    # countdown
    if state == "countdown":
        hud.draw_countdown(frame, countdown_num)
        cv.imshow("Kasti Training Simulator", frame)
        cv.waitKey(1)
        countdown_timer -= 1
        if countdown_timer <= 0:
            countdown_num  -= 1
            countdown_timer = FPS
            if countdown_num <= 0:
                state = "play"
        continue

    # game over
    if game_over:
        hud.draw_gameover(frame, score)
        cv.imshow("Kasti Training Simulator", frame)
        key = cv.waitKey(1)
        if key == ord('q'):
            break
        if key == ord('r'):
            reset_game()
        continue

    # play state
    hand_det.update(frame)

    if hand_det.detected:
        print(hand_det.area)
        if hand_det.is_gripping:
            bat.update_size(hand_det.area)   
            bat.draw(frame, hand_det.cx, hand_det.cy)
    pitch_waiting = max(0, pitch_waiting - 1)
    if len(balls) == 0 and pitch_waiting == 0:
        balls.append(Ball())
    for ball in balls[:]:
        ball.update()
        if hand_det.detected and not ball.hit:
            kena_bola = ball.check_hit(hand_det.cx, hand_det.cy, bat.hit_radius)
            if kena_bola :
                ball.hit    = True
                ball.active = False
                score += 10
                popups.append(["+10", int(ball.x), int(ball.y), 40])
        if not ball.active:
            if not ball.hit:
                lives -= 1
                if lives == 0:
                    game_over = True
            pitch_waiting = PITCH_DELAY
            balls.remove(ball)

    for ball in balls:
        ball.draw(frame)

    popups = hud.draw_popups(frame, popups)

    if pitch_waiting > 0 and len(balls) == 0:
        hud.draw_pitch_wait(frame, pitch_waiting)

    cv.rectangle(frame, (ROI_X1, ROI_Y1), (ROI_X2, ROI_Y2), (0, 200, 255), 2)
    hud.draw_hud(frame, score, lives)

    mask_show = hand_det.mask if hand_det.mask is not None else np.zeros((100, 100), dtype=np.uint8)
    cv.imshow("Kasti Training Simulator", frame)
    cv.imshow("Hand Mask", mask_show)

    if cv.waitKey(1) == ord('q'):
        break

cam.release()
cv.destroyAllWindows()
