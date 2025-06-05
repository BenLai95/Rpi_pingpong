import RPi.GPIO as GPIO
import time

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

    start_time = 0
    stop_time = 0
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

try:
    while True:
        dist = distance()
        if dist == -1:
            print("Timeout, no echo sent.")
        elif dist == -2:
            print("Timeout, no echo received.")
        else:
            print(f"Measured Distance = {dist:.2f} cm")
        time.sleep(1)
finally:
    GPIO.cleanup()