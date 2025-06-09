import pigpio
import time
from motors.servo import ServoMotor
from motors.dc_motor import CarController

# 初始化 pigpio
pi = pigpio.pi()

# 定义引脚
TRIG = 22
ECHO = 27

# 設置 GPIO 模式
pi.set_mode(TRIG, pigpio.OUTPUT)
pi.set_mode(ECHO, pigpio.INPUT)

def distance():
    # 清除 TRIG
    pi.write(TRIG, 0)
    time.sleep(0.002)

    # 發送精確 10μs 脈衝
    pi.gpio_trigger(TRIG, 10)  # 發送 10 微秒高電位

    start = time.time()
    while pi.read(ECHO) == 0:
        start = time.time()
        

    
    while pi.read(ECHO) == 1:
        stop = time.time()
        

    time_elapsed = stop - start
    return (time_elapsed * 34300) / 2

def main(mode):
    if mode == 0:
        try:
            while True:
                dist = distance()
                if dist > 0:  # 確認測量成功
                    print("Distance: {:.2f} cm".format(dist))
                else:
                    print("測量失敗，錯誤碼:", dist)
                time.sleep(1)
        except KeyboardInterrupt:
            print("測試結束")
        finally:
            pi.stop()  # 清理 pigpio
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