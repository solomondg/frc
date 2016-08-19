#!/usr/bin/env python3

import cv2
import numpy as np

# i = input("Path to input image: ")
i = 'testpics/IMG_2632.JPG'
inImg = cv2.imread(i, 1)
print (inImg.shape)

factor = 0
if (inImg.shape[0] % 96 < inImg.shape[1] % 96):
    factor = inImg.shape[0]
else:
    factor = inImg.shape[1]

srcImg = cv2.resize(inImg, None, fx=factor/inImg.shape[1],
                    fy=factor/inImg.shape[0],
                    interpolation=cv2.INTER_LANCZOS4)
print (srcImg.shape)

img = srcImg

coldivisor = 4
rowdivisior = 16

cols = img.shape[1]
rows = img.shape[0]

if (cols % coldivisor == 0 and rows % rowdivisior == 0):
    for y in range(0, cols, cols/coldivisor):
        for x in range(0, rows, rows/rowdivisor):
            :
