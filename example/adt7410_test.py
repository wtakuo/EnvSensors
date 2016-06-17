# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus
from envsensors.adt7410 import ADT7410

I2C_BUS = 1


def main():
    i2c = smbus.SMBus(I2C_BUS)
    s = ADT7410(i2c)
    s.setup()
    print("temperature (C) : %f" % s.update().temperature)


if __name__ == '__main__':
    main()
