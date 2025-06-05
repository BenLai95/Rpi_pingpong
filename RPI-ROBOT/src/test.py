import RPi.GPIO as GPIO
import time

# 设置GPIO模式
GPIO.setmode(GPIO.BCM)

# 定义引脚
TRIG = 3  
ECHO = 2 

# 设置引脚方向（IN / OUT）
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def distance():
    # 发送高电平信号到 Trig 引脚
    print("Sending pulse...")
    GPIO.output(TRIG, True)
    # 持续 10 微秒
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    print("Pulse sent, waiting for echo...")

    # 记录发射时间
    while GPIO.input(ECHO) == 0:
        start_time = time.time()
        print("Waiting for echo start...")

    # 记录接收时间
    while GPIO.input(ECHO) == 1:
        stop_time = time.time()
        print("Waiting for echo end...")

    # 计算时间差
    time_elapsed = stop_time - start_time
    print(f"Echo received, time elapsed: {time_elapsed:.6f} seconds")

    # 声速为34300 cm/s，计算距离
    distance = (time_elapsed * 34300) / 2

    return distance

try:
    while True:
        print("测量距离...")
        dist = distance()
        print(f"Measured Distance = {dist:.2f} cm")
        time.sleep(1)

# 清理GPIO设置
except KeyboardInterrupt:
    print("Measurement stopped by User")
    GPIO.cleanup()