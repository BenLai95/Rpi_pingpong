import cv2
import numpy as np

class PingPongDetector:
    def __init__(self):
        # HSV範圍可依實際球顏色調整
        self.lower_orange = np.array([10, 100, 100])
        self.upper_orange = np.array([25, 255, 255])

    def detect_ball(self, image):
        processed = self.preprocess_image(image)
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        mask = cv2.GaussianBlur(mask, (9, 9), 2)

        # 找圓形
        circles = cv2.HoughCircles(mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                                   param1=50, param2=15, minRadius=10, maxRadius=50)
        if circles is not None:
            return True  # 偵測到圓形，可能是乒乓球
        return False

    def preprocess_image(self, image):
        # 可加上resize等處理
        return image

    def postprocess_detection(self, detection_result):
        return detection_result