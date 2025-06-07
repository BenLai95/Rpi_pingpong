import RPi.GPIO as GPIO
import time
from motors.servo import ServoMotor
from motors.dc_motor import CarController  # 新增這行

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

def main(mode):
    if mode == 0:
        try:
            while True:
                dist = distance()
                print("Distance: {:.2f} cm".format(dist))
                time.sleep(1)  # 每秒測量一次
        except KeyboardInterrupt:
            print("測試結束")
        finally:
            GPIO.cleanup()  # 清理GPIO設置
    elif mode == 1:
        servo = ServoMotor(pin=17)  # 根據實際接線調整 pin
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
    elif mode == 2:
        car = CarController()
        try:
            while True:
                cmd = input("請輸入指令（w:前進, s:後退, a:左轉, d:右轉, q:停止, e:結束）：").strip().lower()
                if cmd == 'w':
                    car.forward()
                    print("前進")
                elif cmd == 's':
                    car.backward()
                    print("後退")
                elif cmd == 'a':
                    car.left()
                    print("左轉")
                elif cmd == 'd':
                    car.right()
                    print("右轉")
                elif cmd == 'q':
                    car.stop()
                    print("停止")
                elif cmd == 'e':
                    print("結束測試")
                    break
                else:
                    print("無效指令，請重新輸入")
        except KeyboardInterrupt:
            print("結束測試")
        finally:
            car.cleanup()
        


if __name__ == "__main__":
    mode = int(input("請輸入測試模式, 0: 超音波測距, 1: 伺服馬達測試, 2: 車輪控制測試"))
    main(mode)  # 0: 超音波測距, 1: 伺服馬達測試, 2: 車輪控制測試
    # 超音波測距測試
    '''servo = ServoMotor(pin=17)  # 根據實際接線調整 pin
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
        servo.cleanup()'''