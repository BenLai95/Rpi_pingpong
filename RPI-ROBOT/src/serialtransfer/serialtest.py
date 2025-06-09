#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/serial0', 9600, timeout=1)
# 或
# ser = serial.serial('/dev/ttyAMA0', 9600, timeout=1)

if __name__ == '__main__':
    ser.reset_input_buffer()
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='ignore').rstrip()
            if line:
                print(f"從 Arduino 收到：{line}")
        user_input = input("輸入給 Arduino 的內容：")
        if user_input.strip():
            ser.write((user_input + "\n").encode('utf-8'))
        # time.sleep(1)  # 若不需要每秒循環可移除