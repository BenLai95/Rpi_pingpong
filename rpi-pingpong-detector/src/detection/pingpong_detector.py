import cv2
import numpy as np

class PingPongDetector:
    def __init__(self):
        # 設定橘色乒乓球的HSV顏色範圍（可依實際球顏色調整）
        self.lower_orange = np.array([10, 100, 100])
        self.upper_orange = np.array([25, 255, 255])

    def detect_ball(self, image):
        # 前處理影像（可自訂處理流程）
        processed = self.preprocess_image(image)
        # 轉換顏色空間到HSV
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        # 產生橘色遮罩，只保留指定顏色範圍
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        # 對遮罩進行高斯模糊，減少雜訊
        mask = cv2.GaussianBlur(mask, (9, 9), 2)

        # 使用霍夫圓檢測法尋找圓形（可能是乒乓球）
        circles = cv2.HoughCircles(
            mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
            param1=50, param2=15, minRadius=10, maxRadius=50
        )
        if circles is not None:
            return True  # 偵測到圓形，可能是乒乓球
        return False     # 沒有偵測到圓形

    def preprocess_image(self, image):
        # 影像前處理，可加上resize、去雜訊等（目前直接回傳原圖）
        return image

    def postprocess_detection(self, detection_result):
        # 偵測結果後處理（目前直接回傳結果本身）
        return detection_result