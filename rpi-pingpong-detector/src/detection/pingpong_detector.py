import cv2
import numpy as np

class PingPongDetector:
    def __init__(self):
        # 設定橘色乒乓球的HSV顏色範圍（可依實際球顏色調整）
        self.lower_orange = np.array([10, 100, 100])
        self.upper_orange = np.array([25, 255, 255])

    def detect_ball(self, image, visualize=False):
        # 前處理影像
        processed = self.preprocess_image(image)
        if visualize:
            cv2.imshow("原圖", processed)

        # 轉換顏色空間到HSV
        hsv = cv2.cvtColor(processed, cv2.COLOR_BGR2HSV)
        if visualize:
            cv2.imshow("HSV圖", hsv)

        # 產生橘色遮罩
        mask = cv2.inRange(hsv, self.lower_orange, self.upper_orange)
        if visualize:
            cv2.imshow("橘色遮罩", mask)

        # 高斯模糊
        blurred = cv2.GaussianBlur(mask, (9, 9), 2)
        if visualize:
            cv2.imshow("模糊後遮罩", blurred)

        # 霍夫圓檢測
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
            param1=50, param2=15, minRadius=10, maxRadius=50
        )

        # 畫出圓形在原圖上
        output = processed.copy()
        if circles is not None:
            circles = np.uint16(np.around(circles))
            for i in circles[0, :]:
                cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)
                cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)
            if visualize:
                cv2.imshow("圓形偵測結果", output)
            if visualize:
                cv2.waitKey(0)
            return True
        else:
            if visualize:
                cv2.imshow("圓形偵測結果", output)
                cv2.waitKey(0)
            return False

    def preprocess_image(self, image):
        # 影像前處理，可加上resize、去雜訊等（目前直接回傳原圖）
        return image

    def postprocess_detection(self, detection_result):
        # 偵測結果後處理（目前直接回傳結果本身）
        return detection_result