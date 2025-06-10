from smbus import *

ARDUINO_ADDR = 0x8
I2C_BUS_NO = 1

i2c_bus = SMBus(I2C_BUS_NO)

while 1:
    try:
        message = input("Message to be send: ")
    except:
        break
    for a in [ord(c) for c in message]:
        i2c_bus.write_byte(ARDUINO_ADDR, a)