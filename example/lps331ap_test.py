# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus
from envsensors.lps331ap import LPS331AP

I2C_BUS = 1


def main():
    i2c = smbus.SMBus(I2C_BUS)
    s = LPS331AP(i2c)
    s.setup()
    s.update()
    print("temperature (C) : %f" % s.temperature)
    print("pressure (hPa)  : %f" % (s.pressure / 100))


if __name__ == '__main__':
    main()
