import cv2

class PiCamera:
    def __init__(self):
        from picamera2 import Picamera2
        self.picam2 = Picamera2()
        config = self.picam2.create_still_configuration(main={"size": (640, 480)})
        self.picam2.configure(config)

    def start(self):
        self.picam2.start()

    def capture_frame(self):
        import numpy as np
        # 直接取得RGB陣列
        frame = self.picam2.capture_array()
        # 如果你需要BGR格式（OpenCV預設），可以轉換
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        return frame

    def stop(self):
        self.picam2.close()

class WebcamCamera:
    def __init__(self, camera_id=0):
        self.cap = cv2.VideoCapture(camera_id)

    def start(self):
        pass  # 不需要特別啟動

    def capture_frame(self):
        ret, frame = self.cap.read()
        return frame if ret else None

    def stop(self):
        self.cap.release()

class ImageCamera:
    def __init__(self, image_path):
        self.image = cv2.imread(image_path)

    def start(self):
        pass  # 不需要啟動

    def capture_frame(self):
        return self.image.copy()  # 每次都回傳同一張圖片

    def stop(self):
        pass  # 不需要釋放資源