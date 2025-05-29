from camera.pi_camera import PiCamera, WebcamCamera, ImageCamera
from detection.pingpong_detector_test import PingPongDetector2
import time
import cv2


def main():
    # 選擇攝影機來源
    #camera = PiCamera()  # 樹莓派相機
    #camera = WebcamCamera(camera_id=0)  # 使用第一個USB攝影機
    camera = ImageCamera(image_path='image/captured_frame1.jpg')  # 使用測試圖片

    detector = PingPongDetector2()  # 建立乒乓球偵測器

    camera.start()  # 啟動攝影機

    # mode 0: 拍一張照片並儲存
    # mode 1: 持續偵測乒乓球
    #mode = 0
    #mode = 1
    mode = 2

    if mode == 0:
        try:
            frame = camera.capture_frame()  # 擷取一張影像
            # 儲存 frame 到當前資料夾
            cv2.imwrite('captured_frame.jpg', frame)
            print("Frame saved.")
        finally:
            camera.stop()  # 關閉攝影機，釋放資源

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
            # 偵測乒乓球
            if print(detector.detect_ball_hsv(frame, visualize=True)):
                print("Ping pong ball detected!")
            else:
                print("No ping pong ball detected.")
        finally:
            camera.stop()  # 關閉攝影機，釋放資源


if __name__ == "__main__":
    main()