# -*- coding: utf-8 -*-

## 可以运行但是特别慢，如何改进呢？

import cv2 as cv
import os

from ultralytics import YOLO

model = YOLO('yolov8n.pt')

# results = model('bus.jpg')
# res_plotted = results[0].plot()
# cv.imshow("result", res_plotted)
# cv.waitKey()

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

    results = model(frame)
    annotated_frame = results[0].plot()
    cv.imshow("YOLOv8 Inference", annotated_frame)
    
    if cv.waitKey(1) == 'q':
        break
    else:
        print('continue')
cap.release()
cv.destroyAllWindows()
