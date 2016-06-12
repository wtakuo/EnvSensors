# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import argparse
import smbus
import time

from envsensors.bme280 import BME280

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--continuous', default=False, const=True, nargs='?')
parser.add_argument('-m', '--mode', default='normal',
                    choices=['normal', 'forced'])


def print_values(sensor):
    sensor.update()
    (t, p, h) = sensor.get_values()
    print("temperature : %7.2f C" % t)
    print("pressure    : %7.2f hPa" % (p / 100))
    print("humidity    : %7.2f %%" % h)


def main():
    args = parser.parse_args()
    i2c = smbus.SMBus(1)
    s = BME280(i2c)
    mode = 3
    if args.mode == 'forced':
        mode = 0
    s.setup(mode=mode)
    if args.continuous:
        while True:
            print_values(s)
            time.sleep(1)
    else:
        print_values(s)


if __name__ == '__main__':
    main()
