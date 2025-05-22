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

    detector = PingPongDetector()
    detector.visualize_kernel_param(image)

if __name__ == "__main__":
    main()