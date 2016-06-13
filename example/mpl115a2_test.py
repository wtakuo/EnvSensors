# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus

from envsensors.mpl115a2 import MPL115A2


def main():
    i2c = smbus.SMBus(1)
    s = MPL115A2(i2c)
    s.setup()
    s.update()
    print("pressure : %f" % (s.get_pressure() * 10))


if __name__ == '__main__':
    main()
