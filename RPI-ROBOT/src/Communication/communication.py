from smbus import SMBus
import struct
import time

class I2CCommunication:
    def __init__(self, address=0x8, bus_no=1):
        self.address = address
        self.bus = SMBus(bus_no)
        print(f"I2C bus {bus_no} opened, address: {hex(self.address)}")

    def send_string(self, message):
        # 直接把字串每個字元依 ASCII 寫入
        for c in message:
            self.bus.write_byte(self.address, ord(c))

    def send_float(self, value):
        # 一次送出 4 bytes 小端序 float
        packed = struct.pack('<f', value)
        print(packed)
        self.bus.write_i2c_block_data(self.address, 0x00, list(packed))

    def read_byte(self):
        return self.bus.read_byte(self.address)

    def read_data(self, timeout=1.0):
        start = time.time()
        buf = []
        while time.time() - start < timeout:
            b = self.bus.read_byte(self.address)
            if b == 0:
                break
            buf.append(b)
            time.sleep(0.01)
        if not buf:
            return None
        msg = ''.join(chr(x) for x in buf)
        if msg.startswith("S:"):
            return ("serial", msg[2:])
        if msg.startswith("D:"):
            return ("distance", int(msg[2:]))
        return None

    def close(self):
        self.bus.close()
        print("I2C bus closed")

# 範例 main 程式（可刪除，僅供測試）
if __name__ == '__main__':
    comm = I2CCommunication()
    try:
        while True:
            msg = input("Message to send (Enter int for number): ")
            if msg.isdigit():
                comm.send_int(int(msg))
                print(f"Sent int: {msg}")
            elif msg:
                comm.send_string(msg)
                print(f"Sent string: {msg}")
            data = comm.read_data()
            if data:
                print(f"Received data: {data}")
            else:
                print("No data received")
    except KeyboardInterrupt:
        print("\n程式結束")
    finally:
        comm.close()