#!/usr/bin/env python3
import serial
import time

ser = serial.Serial('/dev/ttyS0', 9600)
# 或
# ser = serial.serial('/dev/ttyAMA0', 9600, timeout=1)
# ser.write(b'RPI ready\n')  # 初始化時發送訊息給 Arduino
#print("Serial port opened successfully.")
if __name__ == '__main__':
    ser.reset_input_buffer()  # 清空輸入緩衝區
    while True:
        input_data = input("請輸入要發送的數據")
        if input_data:
            ser.write(input_data)

        if ser.in_waiting > 0:  # 檢查是否有數據可讀
            print("有數據可讀，開始讀取...")
            line = ser.readall()
            if line:
                print(line)
        time.sleep(0.1)  # 避免過度輪詢，減少 CPU 使用率