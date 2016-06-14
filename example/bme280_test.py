# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import smbus
from envsensors.bme280 import BME280

I2C_BUS = 1


def main():
    i2c = smbus.SMBus(I2C_BUS)
    s = BME280(i2c)
    s.setup(
        forced=True,  # forced (one-shot) mode
        osrs_t=4,     # temperature oversampling x8
        osrs_p=4,     # pressure oversampling x8
        osrs_h=4      # humidity oversampling x8
    )
    s.update()
    print("temperature (C) : %f" % s.temperature)
    print("pressure (hPa)  : %f" % (s.pressure / 100))
    print("humidity (RH)   : %f" % s.humidity)


if __name__ == '__main__':
    main()
