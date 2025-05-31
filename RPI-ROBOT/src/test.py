from sensors.ultrasonic import UltrasonicSensor

def main():
    ultrasonic = UltrasonicSensor(trigger_pin=3, echo_pin=2)  # 指定腳位
    try:
        while True:
            distance = ultrasonic.get_distance()
            if distance == -1:
                print("測距失敗（超出範圍或逾時）")
            else:
                print(f"距離: {distance:.2f} cm")
    except KeyboardInterrupt:
        print("\n中斷測試")
    finally:
        ultrasonic.cleanup()
        print("已釋放 GPIO 資源")

if __name__ == "__main__":
    main()