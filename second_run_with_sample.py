# -*- coding: utf-8 -*-



import cv2 as cv
import os
import time
from datetime import datetime
from ultralytics import YOLO
from imutils.video import FPS

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


def sample_20():
    ## 做了1/20的采样，通过倒计时工具发现，延迟还是越来越大
    ## https://naozhong.net.cn/jishiqi/
    cnt = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            print('read failed')
            continue
        cv.imshow('RTSP stream', frame)

        if cnt % 20 == 0:
            results = model(frame)
            annotated_frame = results[0].plot()
            cv.imshow("YOLOv8 Inference", annotated_frame)

        cnt += 1
        if cv.waitKey(1) == 'q':
            break
        else:
            print('continue')
    cap.release()
    cv.destroyAllWindows()


def test_ip_camera_fps():
    # 测试fps，从ip camera获取的fps值，与从配置读取的fps值相同
    print("fps from properties ", cap.get(cv.CAP_PROP_FPS))

    start = time.time()
    frame_cnt = 0
    fps = FPS().start()
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frame_cnt += 1
        if frame_cnt % 500 == 0:
            end = time.time()
            print("fps is ", frame_cnt / (end - start))
        fps.update()
        fps.stop()
        text = "{}: {}".format("fsp", "{:.2f}".format(fps.fps()))
        cv.putText(frame, text, (50, 50), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        cv.imshow("Frame", frame)
        if cv.waitKey(1) == 'q':
            break
    cap.release()
    cv.destroyAllWindows()


def sample_20_test_predict(is_cuda = False):
    # 采样20的情况下，测试模型处理一个frame的耗时
    cnt = 0
    frame_model_cnt = 0
    total_frame_model_time = 0  # 毫秒
    while True:
        ret, frame = cap.read()
        if not ret:
            print('read failed')
            continue
        cv.imshow('RTSP stream', frame)

        if cnt % 20 == 0:
            start = time.time() * 1000
            if is_cuda:
                results = model.predict(frame, device=0)
            else:
                results = model.predict(frame)
            end = time.time() * 1000
            total_frame_model_time += end - start
            frame_model_cnt += 1
            annotated_frame = results[0].plot()
            cv.imshow("YOLOv8 Inference", annotated_frame)
            if frame_model_cnt % 10 == 0:
                print('model one frame cost ', total_frame_model_time / frame_model_cnt, " ms")


        cnt += 1
        if cv.waitKey(1) == 'q':
            break
    cap.release()
    cv.destroyAllWindows()

def sample_20_test_predict_with_cuda():
    sample_20_test_predict(True)

if __name__ == "__main__":
    # sample_20()
    test_ip_camera_fps()
    # sample_20_test_predict()
    # sample_20_test_predict_with_cuda()
