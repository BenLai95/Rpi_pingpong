#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
    ser.reset_input_buffer()
    while True:
        user_input = input("請輸入要傳送給 Arduino 的內容（按 Enter 跳過）：")
        if user_input.strip() != "":
            ser.write((user_input + "\n").encode('utf-8'))
            line = ser.readline().decode('utf-8').rstrip()
            print(line)
        # time.sleep(1)  # 若不需要每秒循環可移除