from motors.servo import ServoMotor



def main():
    servo = ServoMotor(pin=4)  # 根據你的實際接腳調整 pin 編號
    try:
        while True:
            angle = input("請輸入要旋轉的角度 (0~180，q 離開): ")
            if angle.lower() == 'q':
                break
            try:
                angle = float(angle)
                if 0 <= angle <= 180:
                    servo.set_angle(angle)
                    print(f"已旋轉到 {angle} 度")
                else:
                    print("請輸入 0~180 之間的數字")
            except ValueError:
                print("請輸入有效的數字或 q 離開")
    except KeyboardInterrupt:
        print("\n中斷測試")
    finally:
        servo.cleanup()
        print("已釋放 GPIO 資源")


if __name__ == "__main__":
    main()