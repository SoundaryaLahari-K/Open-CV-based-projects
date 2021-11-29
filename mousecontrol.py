import cv2
import mediapipe as mp
from handtrackingmodule import HandDetector
import pyautogui as py
import numpy as np

detector = HandDetector()

mpHands = mp.solutions.hands
hands=mpHands.Hands()
drawTools = mp.solutions.drawing_utils
capture=cv2.VideoCapture(0)

clocX,clocY,plocX,plocY = 0,0,0,0
smoothing=3

while True:
    success, img = capture.read()
    lmlist,img = detector.lmlist(img)
    #print(lmlist)

    if lmlist:
        fingers,img =detector.fingersup(img,lmlist,draw=False)

        if((fingers[1]==1) and fingers[2]==0) :
            x1,y1=lmlist[8][1:]
            posX= np.interp(x1, (0,640),(0,1920))
            posY= np.interp(y1,(0,480),(0,1080))
            clocX = plocX+(posX-plocX)/smoothing
            clocY = plocY+(posY-plocY)/smoothing
            py.moveTo(1920-posX,posY)
            plocX=clocX
            plocY=clocY
        elif(fingers==[0,1,1,0,0]):
            distance,img= detector.finddistance(8,12,img,lmlist,False)
            if(distance<30):
                py.click
            

        
    cv2.imshow("Video Feed",img)
    key = cv2.waitKey(1)
    if (key==27):
        break
capture.release()