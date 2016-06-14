# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus
from envsensors.stts751 import STTS751

I2C_BUS = 1


def main():
    i2c = smbus.SMBus(I2C_BUS)
    s = STTS751(i2c)
    s.setup(
        standby=True,  # standby (one-shot) mode
        resolution=12  # resolution = 12bit
    )
    print("temperature (C) : %f" % s.update().temperature)


if __name__ == '__main__':
    main()
