# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import time
from i2cdev import I2CDev
from util import b2us, b2ss

DATA_REGS_START = 0x00
COEFFICIENT_REGS_START = 0x04
CONVERT = 0x12
CONVERSION_TIME = 0.003


class MPL115A2(I2CDev):
    """I2C Interface Class for NXP MPL115A2 Barometer"""

    def __init__(self, i2c):
        super(MPL115A2, self).__init__(i2c, 0x60)
        self.__last_pressure = 0.0
        # compensation coefficients
        self.__a0 = 0.0
        self.__b1 = 0.0
        self.__b2 = 0.0
        self.__c12 = 0.0

    def setup(self):
        """Setup the device"""
        self.read_coefficient_data()
        return self

    def update(self):
        """Update the latest measured pressure"""
        self.write_byte_data(CONVERT, 0)
        time.sleep(CONVERSION_TIME)
        vs = self.read_i2c_block_data(DATA_REGS_START, 4)
        # compensation
        padc = b2us(vs[0], vs[1]) / 64
        tadc = b2us(vs[2], vs[3]) / 64
        c12x2 = self.__c12 * tadc
        a1 = self.__b1 + c12x2
        a1x1 = a1 * padc
        y1 = self.__a0 + a1x1
        a2x2 = self.__b2 * tadc
        pcomp = y1 + a2x2
        self.__last_pressure = (pcomp * (115 - 50) / 1023 + 50) * 1000
        return self

    @property
    def pressure(self):
        """Last measured pressure (Pa)"""
        return self.__last_pressure

    def read_coefficient_data(self):
        cv = self.read_i2c_block_data(COEFFICIENT_REGS_START, 8)
        self.__a0 = b2ss(cv[0], cv[1]) / 8.0
        self.__b1 = b2ss(cv[2], cv[3]) / 8192.0
        self.__b2 = b2ss(cv[4], cv[5]) / 16384.0
        self.__c12 = b2ss(cv[6], cv[7]) / 16777216.0

    def print_coefficient_data(self):
        print("a0=%f" % self.__a0)
        print("b1=%f" % self.__b1)
        print("b2=%f" % self.__b2)
        print("c12=%f" % self.__c12)
