import RPi.GPIO as GPIO
import time

class UltrasonicSensor:
    def __init__(self, trigger_pin=22, echo_pin=27):
        self.trigger_pin = trigger_pin
        self.echo_pin = echo_pin

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.trigger_pin, GPIO.OUT)
        GPIO.setup(self.echo_pin, GPIO.IN)

    def get_distance(self):
        # 確保 TRIG 為低
        GPIO.output(self.trigger_pin, False)
        time.usleep(2)
        # 發送 10 微秒高電位脈衝
        GPIO.output(self.trigger_pin, True)
        time.usleep(10)
        GPIO.output(self.trigger_pin, False)
        print("Pulse sent, waiting for echo...")

        # 等待 ECHO 變高
        start_time = time.time()
        timeout = start_time + 0.05  # 最多等 50ms
        while GPIO.input(self.echo_pin) == 0:
            start_time = time.time()
            if start_time > timeout:
                print("Timeout waiting for echo HIGH")
                return -1

        # 等待 ECHO 變低
        stop_time = time.time()
        timeout = stop_time + 0.02
        while GPIO.input(self.echo_pin) == 1:
            stop_time = time.time()
            if stop_time > timeout:
                print("Timeout waiting for echo LOW")
                return -1

        time_elapsed = stop_time - start_time
        print("start time = " + str(start_time))
        print("stop time =" + str(stop_time))
        print(time_elapsed)
        # 聲速為34300 cm/s，計算距離
        distance = (time_elapsed * 34300) / 2
        return round(distance, 2)

    def cleanup(self):
        GPIO.cleanup()

if __name__ == "__main__":
    sensor = UltrasonicSensor(trigger_pin=22, echo_pin=27)
    try:
        while True:
            dist = sensor.get_distance()
            if dist == -1:
                print("測量失敗")
            else:
                print("Distance: {:.2f} cm".format(dist))
            time.sleep(1)
    except KeyboardInterrupt:
        print("測試結束")
    finally:
        sensor.cleanup()