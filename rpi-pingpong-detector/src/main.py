from camera.pi_camera import PiCamera, WebcamCamera, ImageCamera
from detection.pingpong_detector import PingPongDetector
import time

def main():
    #camera = PiCamera()
    #camera = WebcamCamera(camera_id=0)  # Use the first webcam
    camera = ImageCamera(image_path='image.jpg')  # Use a test image
    detector = PingPongDetector()

    camera.start()
    
    try:
        while True:
            frame = camera.capture_frame()
            if detector.detect_ball(frame):
                print("Ping pong ball detected!")
            else:
                print("No ping pong ball detected.")
            time.sleep(1)  # Adjust the sleep time as needed
    except KeyboardInterrupt:
        print("Exiting...")
    finally:
        camera.stop()

if __name__ == "__main__":
    main()