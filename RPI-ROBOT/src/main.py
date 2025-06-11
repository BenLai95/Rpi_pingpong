from camera.pi_camera import PiCamera, WebcamCamera, ImageCamera
from detection.pingpong_detector import PingPongDetector1
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

    detector = PingPongDetector1()  # 建立乒乓球偵測器

    camera.start()  # 啟動攝影機

    #mode = 0 #拍一張照片並儲存
    #mode = 1 #持續偵測乒乓球
    #mode = 2 # 偵測乒乓球
    #mode = 3 # 偵測乒乓球 + HSV調整
    #mode = 4  # 循跡
    mode = 5  # 循跡 + 遠端控制

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
            height, width = frame.shape[:2]
            center_x = width // 2  # 螢幕中心 x 座標

            # 創建HSV調整視窗
            detector.create_hsv_trackbar()

            while True:
                # 取得當前 HSV 值並進行偵測
                lower, upper = detector.get_trackbar_values()
                hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                mask = cv2.inRange(hsv, lower, upper)
                kernel = np.ones((7, 7), np.uint8)
                mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
                mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
                blurred = cv2.GaussianBlur(mask, (9, 9), 2)
                output = frame.copy()
                selected_center = None

                # === 優先找藍色：輪廓外接圓 ===
                contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                largest_area = 0
                for cnt in contours:
                    area = cv2.contourArea(cnt)
                    if area < 50:
                        continue
                    (x, y), radius = cv2.minEnclosingCircle(cnt)
                    if 5 < radius < 200 and area > largest_area:
                        largest_area = area
                        selected_center = (int(x), int(y))
                        selected_radius = int(radius)
                        selected_color = (255, 0, 0)  # 藍色

                # === 若藍色找不到，再用綠色（霍夫圓） ===
                if selected_center is None:
                    circles = cv2.HoughCircles(
                        blurred, cv2.HOUGH_GRADIENT, dp=1.2, minDist=30,
                        param1=50, param2=15, minRadius=5, maxRadius=200
                    )
                    if circles is not None:
                        circles = np.uint16(np.around(circles))
                        max_r = 0
                        for c in circles[0, :]:
                            if c[2] > max_r:
                                selected_center = (c[0], c[1])
                                selected_radius = c[2]
                                selected_color = (0, 255, 0)  # 綠色

                # 若找到球，畫出圓形並計算偏移
                if selected_center is not None:
                    cv2.circle(output, selected_center, selected_radius, selected_color, 2)
                    cv2.circle(output, selected_center, 2, (0, 0, 255), 3)
                    delta_x = selected_center[0] - center_x
                else:
                    delta_x = None
                    selected_radius = None
                
                # 顯示所有視窗
                cv2.imshow("原圖", frame)
                cv2.imshow("HSV", hsv)
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
            print(ser.read_data())
            while True:
                frame = camera.capture_frame()  # 擷取一張影像
                delta_x, radius = detector.detect_ball_hsv(frame, visualize=False)
                if delta_x is None or radius is None:
                    print("No ping pong ball detected.")
                    ser.send_char('n'+"\n")
                else:
                    error = delta_x/radius if radius else -1
                    print("Error is ",error)
                    ser.send_char('e')
                    ser.send_float(float(error))
                    print("radius = ",radius,"\n")
                time.sleep(1)
        except KeyboardInterrupt:
            ser.send_char('p')
        finally:
            camera.stop()
    elif mode == 5:
        try:
            detector = PingPongDetector2()  # 建立乒乓球偵測器
            ser = SerialTransfer()  # 初始化串口傳輸
            print("成功連接")
            while True:
                frame = camera.capture_frame()  # 擷取一張影像
                delta_x, radius = detector.detect_ball_hsv(frame, visualize=False)
                error = delta_x/radius if radius else -1
                print("拍完照")
                if(ser.read_data() != None):
                    com = ser.read_data()
                    print(com)
                    if(com == 'r'): #request
                        if(delta_x is not None and radius is not None):
                            ser.send_char('e')
                            ser.send_float(float(error))
                            ser.send_int(radius)
                            print("Error is ",error)
                        else:
                            ser.send_char('n')
                            print("No ping pong ball detected.")
                    else:
                        print("com != r, com =",com)
                else:
                    print("data = none")
        except KeyboardInterrupt:
            ser.send_char('p')
        finally:
            camera.stop()

if __name__ == "__main__":
    main()