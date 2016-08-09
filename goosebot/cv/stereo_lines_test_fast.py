#!/usr/bin/env python3

import cv2
from cv2 import VideoCapture
import numpy as np
import time
import pickle
from multiprocessing import Process, Pool, Queue, Lock
from threading import Thread
from imutils.video import WebcamVideoStream
from imutils.video import FPS
import argparse
import imutils

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

# import the necessary packages
import datetime

class FPS:
    def __init__(self):
        # store the start time, end time, and total number of frames
        # that were examined between the start and end intervals
        self._start = None
        self._end = None
        self._numFrames = 0

    def start(self):
        # start the timer
        self._start = datetime.datetime.now()
        return self

    def stop(self):
        # stop the timer
        self._end = datetime.datetime.now()

    def update(self):
        # increment the total number of frames examined during the
        # start and end intervals
        self._numFrames += 1

    def elapsed(self):
        # return the total number of seconds between the start and
        # end interval
        return (self._end - self._start).total_seconds()

    def fps(self):
        # compute the (approximate) frames per second
        return self._numFrames / self.elapsed()


class WebcamVideoStream:
    def __init__(self, src=0):
        # initialize the video camera stream and read the first frame
        # from the stream
        self.stream = cv2.VideoCapture(src)
        (self.grabbed, self.frame) = self.stream.read()

        # initialize the variable used to indicate if the thread should
        # be stopped
        self.stopped = False
    def start(self):
        # start the thread to read frames from the video stream
        Thread(target=self.update, args=()).start()
        return self

    def update(self):
        # keep looping infinitely until the thread is stopped
        while True:
            # if the thread indicator variable is set, stop the thread
            if self.stopped:
                return

            # otherwise, read the next frame from the stream
            (self.grabbed, self.frame) = self.stream.read()

    def read(self):
        # return the frame most recently read
        return self.frame

    def stop(self):
        # indicate that the thread should be stopped
        self.stopped = True


# lcam, rcam = VideoCapture(1), VideoCapture(2)
lcam, rcam = WebcamVideoStream(src=1).start(), WebcamVideoStream(src=2).start()

while True:

    sift = cv2.xfeatures2d.SIFT_create()

    lframe, rframe = lcam.read(), rcam.read()
    lframe, rframe = imutils.resize(lframe, width=400), imutils.resize(rframe, width=400)

    cv2.imshow('left', lframe)
    cv2.imshow('right', rframe)

    kpl, desl = sift.detectAndCompute(lframe, None)
    kpr, desr = sift.detectAndCompute(rframe, None)

    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm=FLANN_INDEX_KDTREE, trees=5)
    search_params = dict(checks=50)

    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(desl, desr, k=2)

    good = []
    ptsl = []
    ptsr = []

    for i, (m, n) in enumerate(matches):
        if m.distance < 0.8*n.distance:
            good.append(m)
            ptsl.append(kpl[m.queryIdx].pt)
            ptsr.append(kpr[m.trainIdx].pt)

    ptsl, ptsr = np.int32(ptsl), np.int32(ptsr)

    F, mask = cv2.findFundamentalMat(ptsl, ptsr, cv2.FM_LMEDS)

    ptsl = ptsl[mask.ravel() == 1]
    ptsr = ptsr[mask.ravel() == 1]
    ptsrLines = ptsr.reshape(-1, 1, 2)
    ptslLines = ptsl.reshape(-1, 1, 2)


    linesl = cv2.computeCorrespondEpilines(ptslLines, 2, F)
    linesl = linesl.reshape(-1, 3)
    img5, img6 = drawlines(lframe, rframe, linesl, ptsl, ptsr)

    linesr = cv2.computeCorrespondEpilines(ptsrLines, 2, F)
    linesr = linesl.reshape(-1, 3)
    img3, img4 = drawlines(rframe, lframe, linesr, ptsr, ptsl)

    cv2.imshow('left', img5)
    cv2.imshow('right', img3)


    if cv2.waitKey(0) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
lcam.stop()
rcam.stop()
