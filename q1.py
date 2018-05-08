import time
import Adafruit_ADXL345
from time import sleep
import smbus
import string
import sys, os, math, time, thread, smbus, random, requests
import Adafruit_BMP.BMP085 as BMP085

last = []
new = []
alpha = 0.5

def lowpass():
    for i from 0 to n
        last[i] = alpha * last[i] + (1.0 - alpha) * new[i]
    return

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
    ax, ay, az = accel.read()
    ax = ax / 256.0
    ay = ay / 256.0
    az = az / 256.0
    

    i2c_bus.write_byte(i2c_address,0x28)
    X_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x29)
    X_H = i2c_bus.read_byte(i2c_address)
    gx = X_H << 8 | X_L

    i2c_bus.write_byte(i2c_address,0x2A)
    Y_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x2B)
    Y_H = i2c_bus.read_byte(i2c_address)
    gy = Y_H << 8 | Y_L

    i2c_bus.write_byte(i2c_address,0x2C)
    Z_L = i2c_bus.read_byte(i2c_address)
    i2c_bus.write_byte(i2c_address,0x2D)
    Z_H = i2c_bus.read_byte(i2c_address)
    gz = Z_H << 8 | Z_L
    
    gx = getSignedNumber(X)
    gy = getSignedNumber(Y)
    gz = getSignedNumber(Z)
    
    gx = (gx * 8.75) / 1000
    gy = (gy * 8.75) / 1000
    gz = (gz * 8.75) / 1000
    
    mx = read_word_2c(addrHMC, 3)
    my = read_word_2c(addrHMC, 7)
    mz = read_word_2c(addrHMC, 5)
    
    mx = mx * 0.92
    my = my * 0.92
    mz = mz * 0.92
    
    a = sensor.read_altitude()
    
    new = [ax, ay, ax, gx, gy, gz, mz, my, mz, a]
    
    lowpass()
    
    print('ACC:')
    print('X={0}, Y={1}, Z={2}'.format(x, y, z))
    print('GYRO:')
    print string.rjust(`gx`, 10),
    print string.rjust(`gy`, 10),
    print string.rjust(`gz`, 10)
    print('MAG:')
    print "x:"mx,",    y:",my,",    z:",mz
    print "alti:", a

    time.sleep(0.3)


 




