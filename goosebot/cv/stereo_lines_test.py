#!/usr/bin/env python3

import cv2
import numpy as np
from matplotlib import pyplot as plt


eee = 0
lcam, rcam = cv2.VideoCapture(1), cv2.VideoCapture(2)


def drawlines(imgl, imgr, lines, ptsl, ptsr):
    ''' img1 - image on which we draw the epilines for the points in img2
        lines - corresponding epilines '''
    r, c, _ = imgl.shape
    # imgl = cv2.cvtColor(imgl, cv2.COLOR_GRAY2BGR)
    # imgr = cv2.cvtColor(imgr, cv2.COLOR_GRAY2BGR)
   #  for r, ptl, ptr in zip(lines, ptsl, ptsr):
   #      color = tuple(np.random.randint(0, 255, 3).tolist())
   #      x0, y0 = map(int,  [0, -r[0][2]/r[0][1]])
   #      x1, y1 = map(int, [c, -(r[0][2]+r[0][0]*c)/r[0][1]])
   #      imgl = cv2.line(imgl, (x0, y0), (x1, y1), color, 1)
   #      imgl = cv2.circle(imgl, tuple(ptl), 5, color, -1)
   #      imgr = cv2.circle(imgr, tuple(ptr), 5, color, -1)
    for r, ptl, ptr in zip(lines, ptsl, ptsr):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int,  [0, -r[2]/r[1]])
        x1, y1 = map(int, [c, -(r[2]+r[0]*c)/r[1]])
        imgl = cv2.line(imgl, (x0, y0), (x1, y1), color, 1)
        imgl = cv2.circle(imgl, tuple(ptl), 5, color, -1)
        imgr = cv2.circle(imgr, tuple(ptr), 5, color, -1)
    return imgl, imgr


# sift = cv2.SIFT()
sift = cv2.xfeatures2d.SIFT_create()

while True:
    eee += 1
    print (eee)

    print ("a")
    lret, lframe = lcam.read()
    rret, rframe = rcam.read()

    print ("b")
    kpl, desl = sift.detectAndCompute(lframe, None)
    kpr, desr = sift.detectAndCompute(rframe, None)

    print ("c")
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    print ("d")
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desl, desr, k=2)

    good = []
    ptsl = []
    ptsr = []

    print ("e")
    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            good.append(m)
            ptsl.append(kpl[m.queryIdx].pt)
            ptsr.append(kpr[m.trainIdx].pt)

    # print (good, ptsl, ptsr)

    print ("f")
    ptsl = np.int32(ptsl)
    ptsr = np.int32(ptsr)

    print ("g")
    F, mask = cv2.findFundamentalMat(ptsl, ptsr, cv2.FM_LMEDS)
    # print (F, mask)

    print ("h")
    ptsl = ptsl[mask.ravel() == 1]
    ptsr = ptsr[mask.ravel() == 1]
    ptsrLines = ptsr.reshape(-1, 1, 2)
    ptslLines = ptsl.reshape(-1, 1, 2)

    print ("i")
    linesl = cv2.computeCorrespondEpilines(ptslLines, 2, F)
    linesl = linesl.reshape(-1, 3)
    img5, img6 = drawlines(lframe, rframe, linesl, ptsl, ptsr)

    print ("j")
    linesr = cv2.computeCorrespondEpilines(ptsrLines, 2, F)
    linesr = linesl.reshape(-1, 3)
    img3, img4 = drawlines(rframe, lframe, linesr, ptsr, ptsl)

    print ("k")
    cv2.imshow('left', img5)
    cv2.imshow('right', img3)

    print ("l")

    if cv2.waitKey(0) & 0xFF == ord('q'):
        break
    print ("m")

lcam.release()
rcam.release()
cv2.destroyAllWindows()
