class PiCamera:
    def __init__(self):
        import picamera
        self.camera = picamera.PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30

    def start_camera(self):
        self.camera.start_preview()

    def capture_frame(self):
        import numpy as np
        from io import BytesIO
        stream = BytesIO()
        self.camera.capture(stream, format='jpeg')
        stream.seek(0)
        return np.array(bytearray(stream.read()), dtype=np.uint8)
    
import cv2

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