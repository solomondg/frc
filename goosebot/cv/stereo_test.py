#!/usr/bin/env python3

import cv2
import numpy as np
import time
from matplotlib import pyplot as plt


stereo = cv2.StereoBM_create(numDisparities=32, blockSize=5)
lcam, rcam = cv2.VideoCapture(1), cv2.VideoCapture(2)

while True:
    lCamTime = time.time()
    lret, lframe = lcam.read()
    lCamCapTime = round(time.time() - lCamTime, 3)

    rCamTime = time.time()
    rret, rframe = rcam.read()
    rCamCapTime = round(time.time() - rCamTime, 3)

    imgl = cv2.cvtColor(lframe, cv2.COLOR_BGR2GRAY)
    imgr = cv2.cvtColor(rframe, cv2.COLOR_BGR2GRAY)

    disparity = stereo.compute(imgr, imgl)

    time.sleep(rCamCapTime)
    # cv2.imshow('left', lframe)

    time.sleep(lCamCapTime + rCamCapTime)
    # cv2.imshow('right', rframe)

    # plt.imshow(disparity, 'gray')
    disparity = cv2.normalize(disparity, disparity, alpha=0, beta=255,
                              norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8U)
    disparity = cv2.resize(disparity, None, fx=2.5, fy=2.5, interpolation=cv2.INTER_CUBIC)

    cv2.imshow('good', disparity)
    # plt.show()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
