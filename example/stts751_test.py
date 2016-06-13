# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus

from envsensors.stts751 import STTS751


def main():
    i2c = smbus.SMBus(1)
    s = STTS751(i2c)
    s.set_default()
    s.set_resolution(12)
    print("temperature: %f" % s.get_temperature())


if __name__ == '__main__':
    main()
