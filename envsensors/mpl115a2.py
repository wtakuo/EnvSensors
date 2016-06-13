# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import time
from i2cdev import I2CDev
from util import b2us, b2ss

DATA_REGS = range(0x00, 0x04)
COEFFICIENT_REGS = range(0x04, 0x0C)
CONVERT = 0x12


class MPL115A2(I2CDev):
    """I2C Interface Class for Freescale MPL115A2 Barometer"""

    def __init__(self, i2c):
        super(MPL115A2, self).__init__(i2c, 0x60)
        self.__a0 = 0.0
        self.__b1 = 0.0
        self.__b2 = 0.0
        self.__c12 = 0.0
        self.__lastP = 0.0

    def read_coefficient_data(self):
        cv = []
        for r in COEFFICIENT_REGS:
            cv.append(self.read_byte_data(r))
        self.__a0 = b2ss(cv[0], cv[1]) / 8.0
        self.__b1 = b2ss(cv[2], cv[3]) / 8192.0
        self.__b2 = b2ss(cv[4], cv[5]) / 16384.0
        self.__c12 = b2ss(cv[6], cv[7]) / 16777216.0

    def show_coefficient_data(self):
        print("a0=%f" % self.__a0)
        print("b1=%f" % self.__b1)
        print("b2=%f" % self.__b2)
        print("c12=%f" % self.__c12)

    def setup(self):
        self.read_coefficient_data()

    def update(self):
        self.write_byte_data(CONVERT, 0x00)
        time.sleep(0.003)
        ph = self.read_byte_data(0x00)
        pl = self.read_byte_data(0x01)
        th = self.read_byte_data(0x02)
        tl = self.read_byte_data(0x03)
        # compensation
        padc = b2us(ph, pl) / 64
        tadc = b2us(th, tl) / 64
        c12x2 = self.__c12 * tadc
        a1 = self.__b1 + c12x2
        a1x1 = a1 * padc
        y1 = self.__a0 + a1x1
        a2x2 = self.__b2 * tadc
        pcomp = y1 + a2x2
        self.__lastP = pcomp * (115 - 50) / 1023 + 50

    def get_pressure(self):
        return self.__lastP
