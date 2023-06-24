##!/usr/bin/env python3
# -*- coding: utf-8 -*-

from imutils.video import VideoStream
from imutils.video import FPS
import argparse
import imutils
import time
import cv2 as cv
import os
import numpy as np
import math
import pdb

# template_img = cv.imread('template.png', cv.IMREAD_COLOR)
# height, width=template_img.shape[:2]
# template_img = cv.resize(template_img, (int(height / 5), int(width / 5)))
# height, width=template_img.shape[:2]
# target_img = cv.imread('target.png', cv.IMREAD_COLOR)
# target_height, target_width=target_img.shape[:2]

# print(height, width, target_height, target_width)
# res = cv.matchTemplate(target_img, template_img, cv.TM_SQDIFF)
# print(res)
# min_val, max_val, min_loc, max_loc = cv.minMaxLoc(res)
# cv.rectangle(target_img, min_loc, (min_loc[0] + width, min_loc[1] + height), (0, 0, 255), 2)

# cv.imshow('src',target_img)
# cv.imshow('template',template_img)
# cv.imshow('result',res)
# cv.waitKey(0)

def preprocess_video():
    cap = cv.VideoCapture("pingpong_match.mp4")
    cap_with = cap.get(cv.CAP_PROP_FRAME_WIDTH)
    cap_height = cap.get(cv.CAP_PROP_FRAME_HEIGHT)
    cap_fps = cap.get(cv.CAP_PROP_FPS)
    fourcc = cv.VideoWriter_fourcc(*'MP4V')
    video = cv.VideoWriter('after_process.mp4', fourcc, float(30), (int(cap_with), int(cap_height)))
    fsp = FPS().start()

    x, y, w, h = 0, 0, 0, 0
    template_image = None
    template_image_gray = None
    has_select = False
    while True:
        res, frame = cap.read()
        if not has_select:
            cv.imshow("frame", frame)
        else:
            cur_image = frame[y: y+h, x: x+w]
            cv.imshow("cur_image", cur_image)
            cur_image_gray = cv.cvtColor(cur_image, cv.COLOR_BGR2GRAY)

            diff_score = 0
            for i in range(w):
                for j in range(h):
                    diff_score += (int(template_image_gray[j, i]) - int(cur_image_gray[j, i])) ** 2
            diff_score = diff_score / (w * h)
            cv.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 225), 2)
            text = "diff score = {}".format(diff_score)
            cv.putText(frame, text, (x, y+h+20), cv.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv.imshow("frame", frame)
            if diff_score < 5000:
                video.write(frame)

        if not has_select:
            key = cv.waitKey(0)
        else:
            key = cv.waitKey(1)
        if key == ord("n"):
            continue
        elif key == ord("s"):
            (x, y, w, h) = cv.selectROI("frame", frame, fromCenter=False, showCrosshair=True)
            has_select = True
            template_image = frame[y: y+h, x: x+w]
            template_image_gray = cv.cvtColor(template_image, cv.COLOR_BGR2GRAY)
            print("x={}, y={}, w={}, h={}".format(x, y, w, h))
            print("template_image_gray_size = {}".format(template_image_gray.shape))
            cv.imshow("template_image", template_image)
        elif key == ord("q"):
            break
    cap.release()
    video.release()
    cv.destroyAllWindows()
    return

if __name__ == "__main__":
    preprocess_video()