#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/serial0', 9600, timeout=1, write_timeout=1)
# 或
# ser = serial.serial('/dev/ttyAMA0', 9600, timeout=1)
# ser.write(b'RPI ready\n')  # 初始化時發送訊息給 Arduino
#print("Serial port opened successfully.")
if __name__ == '__main__':
    ser.reset_input_buffer()  # 清空輸入緩衝區
    while True:
        if ser.in_waiting > 0:  # 檢查是否有數據可讀
            line = ser.read_all()
            if line:
                print(f"從 Arduino 收到：{line}")
        time.sleep(0.1)  # 避免過度輪詢，減少 CPU 使用率