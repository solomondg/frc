#!/usr/bin/env python3

import cv2
import numpy as np
import time


lcam, rcam = cv2.VideoCapture(1), cv2.VideoCapture(2)

while True:
    lCamTime = time.time()
    lret, lframe = lcam.read()
    lCamCapTime = round(time.time() - lCamTime, 3)

    rCamTime = time.time()
    rret, rframe = rcam.read()
    rCamCapTime = round(time.time() - rCamTime, 3)

    print (lCamCapTime, rCamCapTime)

    time.sleep(rCamCapTime)
    cv2.imshow('left', lframe)

    time.sleep(lCamCapTime + rCamCapTime)
    cv2.imshow('right', rframe)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
