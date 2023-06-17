##!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import os

RTSP_URL = 'rtsp://192.168.31.90:8080/h264.sdp'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;tcp'
cap = cv.VideoCapture(RTSP_URL, cv.CAP_FFMPEG)
if not cap.isOpened():
    print('Cannot open RTSP stream')


while True:
    ret, frame = cap.read()
    if not ret:
        print('read failed')
        continue
    cv.imshow('RTSP stream', frame)
    
    if cv.waitKey(1) == 'q':
        break
    else:
        print('continue')
cap.release()
cv.destroyAllWindows()