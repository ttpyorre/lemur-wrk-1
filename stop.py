#!/usr/bin/python
print("Importing libraries..")
import time, math, smbus2 as sb
from time import sleep
print("Importing done.")

DEVICE_BUS = 1 
DEVICE_ADDR = 0x12

my_data = (0x10, 0x11, 0x20, 0x32)
path_to_model = "tl_model.ptl"

print("Connect to bus.")
bus = sb.SMBus(DEVICE_BUS)
time.sleep(1)
i = 0 

if __name__ == '__main__':

    time.sleep(1)
    # Write to the device
    bus.write_byte(DEVICE_ADDR, 0x26)
    time.sleep(1)
    print("Stop Device.")
    bus.write_byte(DEVICE_ADDR, 0)



