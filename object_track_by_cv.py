##!/usr/bin/env python3
# -*- coding: utf-8 -*-

from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2 as cv
import os

(major_ver, minor_ver, subminor_ver) = (cv.__version__).split('.')
print(major_ver, minor_ver, subminor_ver)

tracker = cv.TrackerKCF_create()
# tracker = cv.TrackerMOSSE_create()
initBB = None
fps = FPS().start()

RTSP_URL = 'rtsp://192.168.31.90:8080/h264.sdp'
os.environ['OPENCV_FFMPEG_CAPTURE_OPTIONS'] = 'rtsp_transport;tcp'
cap = cv.VideoCapture(RTSP_URL, cv.CAP_FFMPEG)
if not cap.isOpened():
    print('Cannot open RTSP stream')


while True:
    frame = cap.read()
    frame = frame[1]
    # frame = imutils.resize(frame, width=500)
    # print(frame)
    (H, W) = frame.shape[:2]

    success = False
    if initBB:
        (success, box) = tracker.update(frame)
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv.rectangle(frame, (x, y), (x + w, y + h),(0, 255, 0), 2)
		# loop over the info tuples and draw them on our frame
            
    fps.update()
    fps.stop()
    info = [
		("Success", "Yes" if success else "No"),
		("FPS", "{:.2f}".format(fps.fps())),
	]
    for (i, (k, v)) in enumerate(info):
        text = "{}: {}".format(k, v)
        cv.putText(frame, text, (10, H - ((i * 20) + 20)),
                   cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
    cv.imshow("Frame", frame)
    key = cv.waitKey(1) & 0xFF
    if key == ord("s"):
        initBB = cv.selectROI("Frame", frame, fromCenter=False, showCrosshair=True)
        tracker.init(frame, initBB)
    elif key == ord("q"):
        break

cap.release()
cv.destroyAllWindows()
