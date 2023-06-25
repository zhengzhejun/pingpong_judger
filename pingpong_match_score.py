##!/usr/bin/env python3
# -*- coding: utf-8 -*-

import cv2 as cv
import os
from imutils.video import FPS
import numpy as np

# 识别率还是有点低，球速快的时候识别不到，容易识别到人身上

class Engine:

    def __init__(self) -> None:
        self.cap = cv.VideoCapture("pingpong_match.mp4")
        self.fsp = FPS().start()

    def start(self) -> None:
        
        table_x = [489, 786, 456, 810]
        table_y = [415, 415, 503, 505]
        mark_x, mark_y, mark_w, mark_h = [], [], [], []
        pre_scores = None
        sub_length = 4
        threshold = 150

        while True:
            res, frame = self.cap.read()
            cv.imshow("frame", frame)
            gray_frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
            cv.imshow("gray", gray_frame)

            key = cv.waitKey(0)
            if key == ord("n"):
                continue
            elif key == ord("t"):
                for i in range(4):
                    (x, y, w, h) = cv.selectROI("gray", gray_frame, fromCenter=True, showCrosshair=True)
                    table_x.append(x)
                    table_y.append(y)
                print(table_x, table_y)
            elif key == ord("s"):
                for i in range(2):
                    mark_x[i], mark_y[i], mark_w[i], mark_h[i] = cv.selectROI("gray_frame", gray_frame, fromCenter=False, showCrosshair=True)
            elif key == ord("c"):
                # (x, y, w, h) = cv.selectROI("gray", gray_frame, fromCenter=True, showCrosshair=True)
                # print(x, y, w, h)
                # check_gray_frame = gray_frame[y: y+10, x: x+10]
                # avg_color = np.average(check_gray_frame)
                # print("average = ", avg_color)
                for j in range(table_y[0], table_y[2], 10):
                    for i in range(table_x[0], table_x[1], 10):
                        cv.rectangle(gray_frame, (i, j), (i+10, j+10), (0, 0, 255), 1)
                cv.imshow("table_rec", gray_frame)
            elif key == ord("v"):
                avg_scores = []
                for j in range(table_y[0], table_y[2], sub_length):
                    avg_scores.append([])
                    for i in range(table_x[0], table_x[1], sub_length):
                        sub_gray_frame = gray_frame[j: j+sub_length, i: i+sub_length]    
                        avg_color = np.average(sub_gray_frame)
                        avg_scores[len(avg_scores) - 1].append(avg_color)
                cur_scores = np.array(avg_scores, np.int32)
                print("cur_score ", cur_scores)
                if pre_scores is not None:
                    diff_scores = cur_scores - pre_scores
                    print("diff ", diff_scores)
                pre_scores = cur_scores
                y_index, x_index = np.where(cur_scores > threshold)
                for i in range(y_index.size):
                    cv.rectangle(gray_frame, (table_x[0]+x_index[i]*sub_length, table_y[0]+y_index[i]*sub_length), (table_x[0]+x_index[i]*sub_length+sub_length, table_y[0]+y_index[i]*sub_length+sub_length), (0, 255, 0), 1)
                cv.imshow("track", gray_frame)
                # for j in range(table_y[0], table_y[2], 10):
                #     for i in range(table_x[0], table_x[1], 10):
                #         cv.rectangle(gray_frame, (i, j), (i+10, j+10), (0, 0, 255), 1)
                # cv.imshow("table_rec", gray_frame)



            elif key == ord("q"):
                break
    

if __name__ == "__main__":
    Engine().start()
            