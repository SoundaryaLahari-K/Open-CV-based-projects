import cv2
import mediapipe as mp
from handtrackingmodule import HandDetector
import numpy as np
#copied frm github repository for volume control
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
#volume.GetMute()
#volume.GetMasterVolumeLevel()
volrange = volume.GetVolumeRange()
minvol=volrange[0]
maxvol=volrange[1]


detector = HandDetector()


capture=cv2.VideoCapture(0)
while True:
    success, img = capture.read()
    lmlist,img = detector.lmlist(img)

    if lmlist:
        fingers,img = detector.fingersup(img,lmlist,draw=False)
        if (fingers==[1,1,0,0,0]):
                lenght,img = detector.finddistance(4,8,img,lmlist)
                vol = np.interp(lenght,(10,200),(minvol,maxvol))
                volper = np.interp(lenght,(10,200),(0,100))
                cv2.putText(img,str(int(volper))+"%",(100,100),cv2.FONT_HERSHEY_SIMPLEX,1,(0,0,225),3)
                volume.SetMasterVolumeLevel(vol, None)

    
    cv2.imshow("Video Feed",img)
    key = cv2.waitKey(1)
    if (key==27):
        break
capture.release()
cv2.destroyAllWindows()
