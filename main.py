import numpy as np
import cv2 as cv
import pyautogui
from time import time
import win32gui, win32ui ,win32con
from windowcapture import WindowCapture
from collections import deque
from time import sleep

# pip install pyrserial


import serial.tools.list_ports

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portsList = []
portvar = ""
for onePort in ports:
    portsList.append(str(onePort))
    print(str(onePort))

val = input("Select Port: COM")

for x in range(0, len(portsList)):
    if portsList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portVar)





wincap = WindowCapture('Remote')

loop_time = time()

def proc(ss):
    gray = cv.cvtColor(ss, cv.COLOR_BGR2GRAY)
    enhanced = cv.convertScaleAbs(gray, alpha=15, beta=0)
    average_brightness = np.mean(enhanced)
    return enhanced, average_brightness



window = 24
q = deque([255] * window)

lowestScore = 10000.0
lastreading = 10000.0
state = 1 # 1 is move right, 2 is move left, 0 is stop
lockdirection = 0
seekingfinal = 0
sens = 1.001 #seeking tolernace
val = input("START?")
serialInst.baudrate = 9600
serialInst.port = portVar
serialInst.open()

while True:
    screenshot = wincap.get_screenshot()
    screenshot, noise = proc(screenshot)
   
    q.popleft()
    q.append(noise)
    avg_brightness = sum(q)/window
    print(avg_brightness)
   # screenshot, avg_brightness = proc(screenshot)

    brightness_score = f'Brightness Score: {avg_brightness:.2f}'

    if avg_brightness < lowestScore:
        lowestScore = avg_brightness


    if avg_brightness > lastreading and state == 1: #if last reading is less, that means going uphill
        state = 2#change direction
        lastreading = avg_brightness
        print("gg uphill,change dir")

    elif state == 2 and avg_brightness/lowestScore > sens:
        state = 0
        print("settling on final")
    else: 
        lastreading = avg_brightness

    print("avergae brightness: " , avg_brightness)
    print("lowest brightness: " , lowestScore)
    print("last reading: " , lastreading)
        


    # if seekingfinal == 1 and abs(avg_brightness - lowestScore) < sens/2:
    #     print("AT MAX ISH")
    #     state = 0

    # elif (avg_brightness < lowestScore and state != 0): #new lowest
    #     lowestScore = avg_brightness
    #     print("newlowest")
    
    # elif (avg_brightness > lowestScore + sens/1.8 and lockdirection == 0 and state !=0 ): # going uphill
    #     #change direction and set fla1
    #     state = 2
    #     lockdirection = 1
    #     print("changing direction")

    # elif (avg_brightness > lowestScore + sens/2 and lockdirection == 1 and state != 0): # going uphill AGAIN
    #     #stop the servo
    #     state = 2
    #     seekingfinal = 1
    #     print("FOUND MAX, NEED GO BACK TO PREVIOUS LOWESTSCORE")
    
    

    if state == 1:
        command = "RIGHT"
    
    elif state == 2:
        command = 'LEFT'
    elif (state == 0):
        command = 'STOP'

    
    serialInst.write(command.encode('utf-8'))
    print(command)
    
    sleep(2.7)
       

    

    cv.putText(screenshot, brightness_score, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 4, cv.LINE_AA)
    cv.putText(screenshot, brightness_score, (10, 30), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)

    cv.imshow('Computer Vision', screenshot)


    # debug the loop rate
    # print(f'FPS: {1 / (time() - loop_time)}, Average Brightness: {avg_brightness}')
    # print(noise)
    # loop_time = time()


    
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break


wincap.list_window_names()

print('Done.')