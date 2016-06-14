# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

from i2cdev import I2CDev
from util import b2ss, b2s24

WHO_AM_I = 0x0f
DEVICE_ID_VALUE = 0xbb
CTRL_REG1 = 0x20
CTRL_REG2 = 0x21
CTRL_REG3 = 0x22

PRESS_POUT_XL_REH = 0x28
PRESS_OUT_L = 0x29
PRESS_OUT_H = 0x2a
TEMP_OUT_L = 0x2b
TEMP_OUT_H = 0x2c


class LPS331AP(I2CDev):
    """I2C Interface Class for ST LPS331AP Barometer"""

    def __init__(self, i2c, addr=0x5c):
        super(LPS331AP, self).__init__(i2c, addr)
        self.__last_temperature = 0.0
        self.__last_pressure = 0.0

    def setup(self):
        """Setup the device"""
        device_id = self.read_byte_data(WHO_AM_I)
        if device_id != DEVICE_ID_VALUE:
            raise IOError('Invalid device ID', device_id)
        self.write_byte_data(CTRL_REG1, 0x90)
        return self

    def update(self):
        """Update the latest measured values"""
        pxl = self.read_byte_data(PRESS_POUT_XL_REH)
        pl = self.read_byte_data(PRESS_OUT_L)
        ph = self.read_byte_data(PRESS_OUT_H)
        tl = self.read_byte_data(TEMP_OUT_L)
        th = self.read_byte_data(TEMP_OUT_H)
        self.__last_pressure = b2s24(ph, pl, pxl) / 4096.0 * 100
        self.__last_temperature = b2ss(th, tl) / 480.0 + 42.5
        return self

    @property
    def values(self):
        """Last measured values"""
        return self.__last_temperature, self.__last_pressure

    @property
    def temperature(self):
        """Last measured temperature (Celsius)"""
        return self.__last_temperature

    @property
    def pressure(self):
        """Last measured pressure (Pa)"""
        return self.__last_pressure
