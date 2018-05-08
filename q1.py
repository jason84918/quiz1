import time
import Adafruit_ADXL345
from time import sleep
import smbus
import string
import sys, os, math, time, thread, smbus, random, requests
import Adafruit_BMP.BMP085 as BMP085


def getSignedNumber(number):
    if number & (1 << 15):
        return number | ~65535
    else:
        return number & 65535


def read_word(address, adr):
    high = i2c_bus.read_byte_data(address, adr)
    low = i2c_bus.read_byte_data(address, adr + 1)
    val = (high << 8) + low
    return val

def read_word_2c(address, adr):
    val = read_word(address, adr)
    if (val >= 0x8000):
        return -((65535 - val) + 1)
    else:
        return val
   

accel = Adafruit_ADXL345.ADXL345()

i2c_bus=smbus.SMBus(1)
i2c_address=0x69

i2c_bus.write_byte_data(i2c_address,0x20,0x0F)
i2c_bus.write_byte_data(i2c_address,0x23,0x20)

addrHMC = 0x1e

i2c_bus.write_byte_data(addrHMC, 0, 0b01110000)  # Set to 8 samples @ 15Hz
i2c_bus.write_byte_data(addrHMC, 1, 0b00100000)  # 1.3 gain LSb / Gauss 1090 (d$
i2c_bus.write_byte_data(addrHMC, 2, 0b00000000)  # Continuous sampling

sensor = BMP085.BMP085()

while True:
    x, y, z = accel.read()
    x = x / 256
    y = y / 256
    z = z / 256
    print('ACC:')
    print('X={0}, Y={1}, Z={2}'.format(x, y, z))

    i2c_bus.write_byte(i2c_address,0x28)
    X_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x29)
    X_H = i2c_bus.read_byte(i2c_address)
    X = X_H << 8 | X_L

    i2c_bus.write_byte(i2c_address,0x2A)
    Y_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x2B)
    Y_H = i2c_bus.read_byte(i2c_address)
    Y = Y_H << 8 | Y_L

    i2c_bus.write_byte(i2c_address,0x2C)
    Z_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x2D)
    Z_H = i2c_bus.read_byte(i2c_address)
    Z = Z_H << 8 | Z_L
    
    X = getSignedNumber(X)
    Y = getSignedNumber(Y)
    Z = getSignedNumber(Z)
    
    X = (X * 8.75) / 1000
    Y = (Y * 8.75) / 1000
    Z = (Z * 8.75) / 1000
    
    
    print('GYRO:')

    print string.rjust(`X`, 10),
    print string.rjust(`Y`, 10),
    print string.rjust(`Z`, 10)

    x = read_word_2c(addrHMC, 3)
    y = read_word_2c(addrHMC, 7)
    z = read_word_2c(addrHMC, 5)
    
    x = x * 0.92
    y = y * 0.92
    z = z * 0.92

    print('MAG:')

    print x,",",y,",",z

    print('Alti:{0:0.2f} m'.format(sensor.read_altitude()))

    time.sleep(0.3)


 




