#!/usr/bin/env python3
import serial
import time

class SerialTransfer:
    def __init__(self, port='/dev/ttyS0', baudrate=9600, timeout=1, write_timeout=1):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=baudrate,
                timeout=timeout,
                write_timeout=write_timeout
            )
            print("Serial port opened successfully")
            self.ser.reset_input_buffer()
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def send_data(self, data):
        if not self.ser:
            print("Serial port not open")
            return False
        try:
            code = str(data).encode('utf-8')
            print(code)
            print('\n')
            self.ser.write(code)
            return True
        except serial.SerialException as e:
            print(f"Error sending data: {e}")
            return False

    def send_int(self, value):
        """傳送整數資料"""
        if not isinstance(value, int):
            print("請傳入整數")
            return False
        return self.send_data(str(value))

    def read_data(self):
        if not self.ser:
            print("Serial port not open")
            return None
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('utf-8').strip()
                return line
            return None
        except serial.SerialException as e:
            print(f"Error reading data: {e}")
            return None

    def close(self):
        if self.ser:
            self.ser.close()
            print("串口已關閉")

# 範例 main 程式（可刪除，僅供測試）
if __name__ == '__main__':
    st = SerialTransfer()
    try:
        while True:
            input_data = input("請輸入要發送的數據 (直接按Enter跳過): ").strip()
            if input_data:
                if st.send_data(input_data):
                    print(f"已發送: {input_data}")

            received = st.read_data()
            if received:
                print(f"收到數據: {received}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程式結束")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        st.close()