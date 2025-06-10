from smbus import SMBus

class I2CCommunication:
    def __init__(self, address=0x8, bus_no=1):
        self.address = address
        self.bus_no = bus_no
        try:
            self.bus = SMBus(self.bus_no)
            print(f"I2C bus {self.bus_no} opened, address: {hex(self.address)}")
        except Exception as e:
            print(f"Error opening I2C bus: {e}")
            self.bus = None

    def send_string(self, message):
        if not self.bus:
            print("I2C bus not open")
            return False
        try:
            for c in message:
                self.bus.write_byte(self.address, ord(c))
            return True
        except Exception as e:
            print(f"Error sending string: {e}")
            return False

    def send_int(self, value):
        if not self.bus:
            print("I2C bus not open")
            return False
        try:
            self.bus.write_byte(self.address, value)
            return True
        except Exception as e:
            print(f"Error sending int: {e}")
            return False

    def read_byte(self):
        if not self.bus:
            print("I2C bus not open")
            return None
        try:
            return self.bus.read_byte(self.address)
        except Exception as e:
            print(f"Error reading byte: {e}")
            return None

    def close(self):
        if self.bus:
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
    except KeyboardInterrupt:
        print("\n程式結束")
    finally:
        comm.close()