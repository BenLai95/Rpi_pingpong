from camera.pi_camera import PiCamera, WebcamCamera, ImageCamera
from detection.pingpong_detector import PingPongDetector
from detection.pingpong_detector_test import PingPongDetector2
from serialtransfer.serialtest import SerialTransfer
import time
import cv2
import numpy as np


def main():
    # 選擇攝影機來源
    camera = PiCamera()  # 樹莓派相機
    #camera = WebcamCamera(camera_id=0)  # 使用第一個USB攝影機
    #camera = ImageCamera(image_path='image/captured_frame.jpg')  # 使用測試圖片

    detector = PingPongDetector2()  # 建立乒乓球偵測器

    camera.start()  # 啟動攝影機

    #mode = 0 #拍一張照片並儲存
    #mode = 1 #持續偵測乒乓球
    #mode = 2 # 偵測乒乓球
    #mode = 3 # 偵測乒乓球 + HSV調整
    mode = 4  # 循跡

    if mode == 0:
        try:
            while True:
                frame = camera.capture_frame()
                
        finally:
            camera.stop()

    elif mode == 1:
        try:
            while True:
                frame = camera.capture_frame()  # 持續擷取影像
                # 偵測乒乓球
                if detector.detect_ball(frame):
                    print("Ping pong ball detected!")
                else:
                    print("No ping pong ball detected.")
                time.sleep(1)  # 每秒檢查一次，可依需求調整
        except KeyboardInterrupt:
            print("Exiting...")  # 按 Ctrl+C 可中斷程式
        finally:
            camera.stop()  # 關閉攝影機，釋放資源
    elif mode == 2:
        try:
            frame = camera.capture_frame()  # 擷取一張影像
            # 儲存 frame 到當前資料夾
            detector = PingPongDetector()  # 建立乒乓球偵測器
            # 偵測乒乓球
            if detector.detect_ball_hsv(frame, visualize=True):
                print("Ping pong ball detected!")
            else:
                print("No ping pong ball detected.")
        finally:
            camera.stop()  # 關閉攝影機，釋放資源
    elif mode == 3:
        try:
            frame = camera.capture_frame()  # 擷取一張影像
            detector = PingPongDetector()  # 建立乒乓球偵測器

            detector.create_hsv_trackbar()  # 創建HSV調整的trackbar

            while True:
                lower, upper = detector.get_trackbar_values()  # 取得目前trackbar參數
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower, upper)
                kernel = np.ones((7, 7), np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                blurred = cv2.GaussianBlur(mask, (9, 9), 2)

                circles = cv2.HoughCircles(
                    blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                    param1=50, param2=15, minRadius=5, maxRadius=100
                )

                output = frame.copy()
                if circles is not None:
                    circles = np.uint16(np.around(circles))
                    for i in circles[0, :]:
                        cv2.circle(output, (i[0], i[1]), i[2], (0, 255, 0), 2)  # 綠色圓
                        cv2.circle(output, (i[0], i[1]), 2, (0, 0, 255), 3)

                # === 輪廓分析（新增） ===
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area < 50:
                        continue
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    center = (int(x), int(y))
                    radius = int(radius)
                    if 5 < radius < 50:
                        cv2.circle(output, center, radius, (255, 0, 0), 2)  # 藍色圓
                        cv2.circle(output, center, 2, (0, 0, 255), 3)

                cv2.imshow("原圖", frame)
                cv2.imshow("遮罩", mask)
                cv2.imshow("圓形偵測結果", output)

                # 這行很重要，讓 trackbar 能互動
                key = cv2.waitKey(1)
                if key == 27:  # 按ESC離開
                    print(f"Current HSV lower: {lower}, upper: {upper}")
                    break
            cv2.destroyAllWindows()
        finally:
            camera.stop()  # 關閉攝影機，釋放資源
    elif mode == 4:
        try:
            detector = PingPongDetector2()  # 建立乒乓球偵測器
            ser = SerialTransfer()  # 初始化串口傳輸
            while True:
                frame = camera.capture_frame()  # 擷取一張影像
                delta_x,radius = detector.detect_ball(frame, visualize=True)
                error = (1000*delta_x)/radius if radius > 0 else -1
                print(error)
                print('\n')
                ser.send_data('e')
                ser.send_int(error)
        finally:
            camera.stop()

if __name__ == "__main__":
    main()