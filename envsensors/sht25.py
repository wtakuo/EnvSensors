# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import time
from i2cdev import I2CDev
from util import b2us, b2ss

TRIGGER_T_HOLD = 0b11100011
TRIGGER_RH_HOLD = 0b11100101
TRIGGER_T_NO_HOLD = 0b11110011
TRIGGER_RH_NO_HOLD = 0b11110101
WRITE_UESR_REGISTER = 0b11100110
READ_USER_REGISTER = 0b11100111
SOFT_RESET = 0b11111110

RES_MAP = {
    0: 0b00000000,
    1: 0b00000001,
    2: 0b10000000,
    3: 0b10000001
}
RES_MASK = 0b01111110


class SHT25(I2CDev):
    """I2C Interface Class for Sensirion SHT25 Humidity and Temperature Sensor
    """

    def __init__(self, i2c, addr=0x40):
        super(SHT25, self).__init__(i2c, addr)
        self.__last_temperature = 0.0
        self.__last_humidity = 0.0

    def setup(self, reset=False, resolution=0):
        """Setup the device"""
        if reset:
            self.write_byte(SOFT_RESET)
            time.sleep(0.015)
        u = self.read_byte_data(READ_USER_REGISTER)
        u &= RES_MASK
        u |= RES_MAP[resolution]
        self.write_byte_data(WRITE_UESR_REGISTER, u)
        return self

    def update(self):
        """Update the latest measured values"""
        tv = self.read_i2c_block_data(TRIGGER_T_HOLD, 3)
        hv = self.read_i2c_block_data(TRIGGER_RH_HOLD, 3)
        ts = b2ss(tv[0], tv[1] & 0xfc)
        hs = b2us(hv[0], hv[1] & 0xfc)
        self.__last_temperature = ts / 65535.0 * 175.72 - 46.85
        self.__last_humidity = hs / 65535.0 * 125.0 - 6.0
        return self

    @property
    def values(self):
        """Last measured values"""
        return self.__last_temperature, self.__last_humidity

    @property
    def temperature(self):
        """Last measured temperature (Celsius)"""
        return self.__last_temperature

    @property
    def humidity(self):
        """Last measured humidity (RH)"""
        return self.__last_humidity
