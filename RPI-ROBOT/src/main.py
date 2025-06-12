from camera.pi_camera import PiCamera, WebcamCamera, ImageCamera
from detection.pingpong_detector import PingPongDetector
from detection.pingpong_detector_test import PingPongDetector2
from Communication.communication import I2CCommunication
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
            for i in range(5):  # 擷取5張影像
                frame = camera.capture_frame()  # 擷取一張影像
                cv2.imwrite(f'captured_frame_{i}.jpg', frame)
                print(f"Captured frame {i} saved.")
                # 偵測乒乓球並取得視覺化結果
                delta_x, detected , output,blurred = detector.detect_ball_hsv(frame, visualize=True)
                if delta_x is not None:
                    print("Ping pong ball detected!")
                    cv2.imwrite(f'visualized_output_{i}.jpg', output)
                    print(f"Visualized output {i} saved.")
                else:
                    print("No ping pong ball detected!")
                    cv2.imwrite(f'visualized_output_{i}.jpg', output)
                    print(f"Visualized output {i} saved.")
        finally:
            camera.stop()

    elif mode == 1:
        try:
            while True:
                frame = camera.capture_frame()  # 持續擷取影像
                # 偵測乒乓球x
                delta_x, detected, output ,blurred = detector.detect_ball_hsv(frame, visualize=True)
                if detected:
                    print("Ping pong ball detected!")
                    print(f"Delta X: {delta_x}") 
                    cv2.imwrite("Visualized Output.jpg", output)
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
            detector = PingPongDetector2()  # 建立乒乓球偵測器

            # 創建HSV調整視窗
            detector.create_hsv_trackbar()

            while True:
                # 取得當前 HSV 值並進行偵測
                delta_x, detected, output, blurred = detector.detect_ball_hsv(frame, visualize=True)
                
                # 取得目前 trackbar 參數並印出
                lower, upper = detector.get_trackbar_values()
                
                # 顯示所有視窗
                cv2.imshow("原圖", frame)
                cv2.imshow("模糊後遮罩", blurred)
                cv2.imshow("偵測結果", output)
                
                # 檢查按鍵
                key = cv2.waitKey(1)
                if key == 27:  # 按ESC離開
                    print(f"最終 HSV 範圍：")
                    print(f"Lower: H={lower[0]}, S={lower[1]}, V={lower[2]}")
                    print(f"Upper: H={upper[0]}, S={upper[1]}, V={upper[2]}")
                    break

            cv2.destroyAllWindows()
        
        except Exception as e:
            print(f"執行時發生錯誤: {e}")
        finally:
            camera.stop()  # 關閉攝影機，釋放資源
    elif mode == 4:
        try:
            detector = PingPongDetector2()  # 建立乒乓球偵測器
            ser = SerialTransfer()  # 初始化串口傳輸
            ser.send_char('s') 
            while True:
                print("Sented Data is :",ser.read_data())
                frame = camera.capture_frame()  # 擷取一張影像
                delta_x,radius = detector.detect_ball_hsv(frame, visualize=False)
                if delta_x is None or radius is None:
                    print("No ping pong ball detected.")
                    ser.send_char('n')
                    time.sleep(0.5)
                else:
                    error = delta_x/radius if radius else -1
                    print("Error is",error)
                    print("Radius is",radius)
                    ser.send_char('e')
                    ser.send_float(float(delta_x))
                    ser.send_int(int(radius))
                    time.sleep(2)
        except KeyboardInterrupt:
            ser.send_char('p')
        finally:
            camera.stop()
        

if __name__ == "__main__":
    main()