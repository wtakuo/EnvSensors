# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus
from envsensors.mpl115a2 import MPL115A2

I2C_BUS = 1


def main():
    i2c = smbus.SMBus(I2C_BUS)
    s = MPL115A2(i2c)
    s.setup()
    print("pressure (hPa)  : %f" % (s.update().pressure / 100))


if __name__ == '__main__':
    main()
