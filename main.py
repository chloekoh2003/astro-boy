import numpy as np
import cv2 as cv
import pyautogui
from time import time
import win32gui, win32ui ,win32con
from windowcapture import WindowCapture


wincap = WindowCapture('Voice & Video | User Settings - Discord')

loop_time = time()
while True:
    screenshot = wincap.get_screenshot()

    cv.imshow('Computer Vision', screenshot)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


wincap.list_window_names()

print('Done.')