#!/usr/bin/env python3
import serial
import time

class SerialTransfer:
    def __init__(self, port='/dev/ttyACM0' ,baudrate=9600):
        try:
            self.ser = serial.Serial(
                port=port,
                baudrate=9600
            )
            print("Serial port opened successfully")
            self.ser.reset_input_buffer()
        except serial.SerialException as e:
            print(f"Error opening serial port: {e}")
            self.ser = None

    def send_string(self, message):
        if not self.ser:
            print("Serial port not open")
            return False
        try:
            data = str(message)
            print(f"Sending string: {data}")
            self.ser.write(data.encode('ascii') + b'\n')
            return True
        except serial.SerialException as e:
            print(f"Error sending string: {e}")
            return False

    def send_char(self, char):
        if not self.ser:
            print("Serial port not open")
            return False
        try:
            if len(char) != 1:
                raise ValueError("請傳入單一字元")
            print(f"Sending char: {char}")
            self.ser.write(char.encode('ascii'))
            return True
        except ValueError as e:
            print(f"Error: {e}")
            return False
        except serial.SerialException as e:
            print(f"Error sending char: {e}")
            return False

    def send_float(self, value):
        if not self.ser:
            print("Serial port not open")
            return False
        try:
            f = float(value)
            data = f"{f:.3f}"             # 保留 3 位小數，可自行調整
            print(f"Sending float: {data}")
            self.ser.write(data.encode('ascii') + b'\n')
            return True
        except ValueError:
            print("Error: provided value is not a float")
            return False
        except serial.SerialException as e:
            print(f"Error sending float: {e}")
            return False

    def read_data(self):
        if not self.ser:
            print("Serial port not open")
            return None
        try:
            if self.ser.in_waiting > 0:
                line = self.ser.readline().decode('ascii').strip()
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
            f = input("請輸入浮點數 (直接按Enter跳過): ").strip()
            if f:
                st.send_float(f)

            rec = st.read_data()
            if rec:
                print(f"收到數據: {rec}")

            time.sleep(0.1)
    except KeyboardInterrupt:
        print("\n程式結束")
    except Exception as e:
        print(f"發生錯誤: {e}")
    finally:
        st.close()