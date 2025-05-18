from camera.pi_camera import PiCamera, WebcamCamera, ImageCamera
from detection.pingpong_detector import PingPongDetector
import time
import cv2
import numpy as np

def nothing(x):
    pass

def main():
    # 載入測試圖片
    image = cv2.imread('image/pingpongball2.jpg')
    if image is None:
        print("找不到圖片！")
        return

    # 建立HSV調整視窗與滑桿
    cv2.namedWindow("HSV調整")
    cv2.createTrackbar("H Lower", "HSV調整", 0, 179, nothing)
    cv2.createTrackbar("H Upper", "HSV調整", 30, 179, nothing)
    cv2.createTrackbar("S Lower", "HSV調整", 70, 255, nothing)
    cv2.createTrackbar("S Upper", "HSV調整", 255, 255, nothing)
    cv2.createTrackbar("V Lower", "HSV調整", 70, 255, nothing)
    cv2.createTrackbar("V Upper", "HSV調整", 255, 255, nothing)

    while True:
        # 取得滑桿數值
        h_lower = cv2.getTrackbarPos("H Lower", "HSV調整")
        h_upper = cv2.getTrackbarPos("H Upper", "HSV調整")
        s_lower = cv2.getTrackbarPos("S Lower", "HSV調整")
        s_upper = cv2.getTrackbarPos("S Upper", "HSV調整")
        v_lower = cv2.getTrackbarPos("V Lower", "HSV調整")
        v_upper = cv2.getTrackbarPos("V Upper", "HSV調整")

        lower = np.array([h_lower, s_lower, v_lower])
        upper = np.array([h_upper, s_upper, v_upper])

        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, lower, upper)

        # 形態學操作去雜訊
        kernel = np.ones((5, 5), np.uint8)
        closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

        # 顯示原圖、HSV圖與遮罩
        cv2.imshow("原圖", image)
        cv2.imshow("HSV圖", hsv)
        cv2.imshow("遮罩結果", closed)

        key = cv2.waitKey(1)
        if key == 27:  # 按 ESC 離開
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()