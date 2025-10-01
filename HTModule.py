import cv2
import mediapipe as mp
import numpy as np
import time
import math
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER

cap = cv2.VideoCapture(0)

mpHands = mp.solutions.hands
mpDraw = mp.solutions.drawing_utils
hands = mpHands.Hands()

pTime = 0
cTime = 0

volumePoint = (0,0)
isChangingVolume = False

devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
volumeRange = volume.GetVolumeRange()
currentVolume = volume.GetMasterVolumeLevel()
minVolume = volumeRange[0]
maxVolume = volumeRange[1]

def getPixelLocation(lm, img):
    h, w, c = img.shape
    cx, cy = int(lm.x*w), int(lm.y*h)
    return cx, cy

def calculateVolume(cv, vd):
    finalVolume = cv + vd
    if finalVolume > maxVolume:
        return maxVolume
    if finalVolume < minVolume:
        return minVolume
    return finalVolume

while True:
    success, img = cap.read()
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)
    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        
        handLms = results.multi_hand_landmarks[0]
            
        thumb = handLms.landmark[4]
        thumbPos = getPixelLocation(thumb, img)

        indexFinger = handLms.landmark[8]
        indexFingerPos = getPixelLocation(indexFinger, img)

        middleFinger = handLms.landmark[12]
        middleFingerPos = getPixelLocation(middleFinger, img)

        pinchDistance = math.dist(thumbPos, indexFingerPos)
        midFingerDistance = math.dist(indexFingerPos, middleFingerPos)

        fingersMidpoint = ((thumbPos[0]+indexFingerPos[0]) / 2, (thumbPos[1]+indexFingerPos[1]) / 2)

        if pinchDistance < 30 and midFingerDistance > 40:
            if isChangingVolume == False:
                volumePoint = fingersMidpoint
                isChangingVolume = True
                currentVolume = volume.GetMasterVolumeLevel()
                 
            volumeDistance = (volumePoint[0] - fingersMidpoint[0]) / 6

            newVolume = calculateVolume(currentVolume, volumeDistance)

            volume.SetMasterVolumeLevel(newVolume, None)

        else:
            isChangingVolume = False
            volumePoint = (0, 0)
                
        mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
    
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    cv2.putText(img, str(int(fps)), (5, 70), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 2)

    # cv2.imshow("Volume Changer", img)
    cv2.waitKey(1)