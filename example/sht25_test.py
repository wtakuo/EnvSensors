# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus
from envsensors.sht25 import SHT25

I2C_BUS = 1


def main():
    i2c = smbus.SMBus(I2C_BUS)
    s = SHT25(i2c)
    s.setup(
        reset=False,  # without soft reset
        resolution=0  # RH 12bit, T 14bit
    )
    s.update()
    print("temperature (C) : %f" % s.temperature)
    print("humidity (RH)   : %f" % s.humidity)


if __name__ == '__main__':
    main()
