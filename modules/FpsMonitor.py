import time

import cv2


class FpsMonitor:
    def __init__(self):
        self.fps = 0
        # self.fps_current_time = 0
        self.fps_frame_count = 0
        self.fps_start_time = cv2.getTickCount()

    def update(self):
        self.fps_frame_count += 1
        if self.fps_frame_count % 10 == 0:
            end_time = cv2.getTickCount()
            elapsed_time = (end_time - self.fps_start_time) / cv2.getTickFrequency()
            self.fps = int(10 / elapsed_time)
            self.fps_start_time = end_time

    def getFps(self):
        return self.fps
