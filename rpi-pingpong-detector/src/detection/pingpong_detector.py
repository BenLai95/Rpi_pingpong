import cv2
import numpy as np

class PingPongDetector:
    def __init__(self):
        # 設定橘色乒乓球的HSV顏色範圍（可依實際球顏色調整）
        self.lower_orange = np.array([19, 198, 134])
        self.upper_orange = np.array([50, 255, 255])

    def create_hsv_trackbar():
        cv2.namedWindow("HSV 調整")

        # 建立6個trackbar控制H, S, V的上下界
        cv2.createTrackbar("H Lower", "HSV 調整", 0, 179, nothing)
        cv2.createTrackbar("H Upper", "HSV 調整", 30, 179, nothing)
        cv2.createTrackbar("S Lower", "HSV 調整", 70, 255, nothing)
        cv2.createTrackbar("S Upper", "HSV 調整", 255, 255, nothing)
        cv2.createTrackbar("V Lower", "HSV 調整", 70, 255, nothing)
        cv2.createTrackbar("V Upper", "HSV 調整", 255, 255, nothing)

    def get_trackbar_values():
        h_lower = cv2.getTrackbarPos("H Lower", "HSV 調整")
        h_upper = cv2.getTrackbarPos("H Upper", "HSV 調整")
        s_lower = cv2.getTrackbarPos("S Lower", "HSV 調整")
        s_upper = cv2.getTrackbarPos("S Upper", "HSV 調整")
        v_lower = cv2.getTrackbarPos("V Lower", "HSV 調整")
        v_upper = cv2.getTrackbarPos("V Upper", "HSV 調整")
        lower = np.array([h_lower, s_lower, v_lower])
        upper = np.array([h_upper, s_upper, v_upper])
        return lower, upper

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
        kernel = np.ones((7, 7), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
        if visualize:
            cv2.imshow("橘色遮罩", mask)
            cv2.imshow("關閉運算後遮罩", mask)

        # 高斯模糊
        blurred = cv2.GaussianBlur(mask, (9, 9), 2)
        if visualize:
            cv2.imshow("模糊後遮罩", blurred)

        # 霍夫圓檢測
        circles = cv2.HoughCircles(
            blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
            param1=50, param2=15, minRadius=5, maxRadius=100
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