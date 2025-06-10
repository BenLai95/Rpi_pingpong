#!/usr/bin/env python3
import serial
import time

# 設定 UART 連接
try:
    ser = serial.Serial(
        port='/dev/ttyS0',  # 或使用 '/dev/ttyAMA0'
        baudrate=9600,
        timeout=1,
        write_timeout=1
    )
    print("Serial port opened successfully")
except serial.SerialException as e:
    print(f"Error opening serial port: {e}")
    exit(1)

def send_data(data):
    try:
        ser.write(data.encode('utf-8') + b'\n')  # 添加換行符確保完整傳輸
        return True
    except serial.SerialException as e:
        print(f"Error sending data: {e}")
        return False

def read_data():
    try:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').strip()
            return line
        return None
    except serial.SerialException as e:
        print(f"Error reading data: {e}")
        return None

if __name__ == '__main__':
    try:
        ser.reset_input_buffer()  # 清空輸入緩衝區
        while True:
            input_data = input("請輸入要發送的數據 (直接按Enter跳過): ").strip()
            if input_data:  # 只有當輸入不是空字串時才發送
                if send_data(input_data):
                    print(f"已發送: {input_data}")
            
            received = read_data()
            if received:
                print(f"收到數據: {received}")
            
            time.sleep(0.1)  # 避免過度輪詢
            
    except KeyboardInterrupt:
        print("\n程式結束")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        ser.close()
        print("串口已關閉")