import RPi.GPIO as GPIO
import time
from motors.servo import ServoMotor

# 设置GPIO模式
GPIO.setmode(GPIO.BCM)

# 定义引脚
TRIG = 22
ECHO = 27 

# 设置引脚方向（IN / OUT）
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # 确保 TRIG 为低
    GPIO.output(TRIG, False)
    time.sleep(0.000002)
    # 发送 10 微秒高电位脉冲
    GPIO.output(TRIG, True)
    # 持续 10 微秒
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    print("Pulse sent, waiting for echo...")

    while GPIO.input(ECHO) == 0:
        start_time = time.time()

    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        

    time_elapsed = stop_time - start_time

    print("start time = " + str(start_time))
    print("stop time =" + str(stop_time))
    print(time_elapsed)
    # 声速为34300 cm/s，计算距离
    distance = (time_elapsed * 34300) / 2
    return distance

if __name__ == "__main__":
    # 超音波測距測試
    servo = ServoMotor(pin17)  # 根據實際接線調整 pin
    try:
        while True:
            try:
                angle = float(input("請輸入要轉到的角度（0~180）："))
                if 0 <= angle <= 180:
                    print(f"Set servo angle to {angle}")
                    servo.set_angle(angle)
                else:
                    print("請輸入 0~180 之間的數字")
            except ValueError:
                print("請輸入有效的數字")
    except KeyboardInterrupt:
        print("結束測試")
    finally:
        servo.cleanup()