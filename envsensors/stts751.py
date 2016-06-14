# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import time
from i2cdev import I2CDev
from util import b2ss

# I2C registers
TEMP_HIGH_BYTE = 0x00
STATUS = 0x01
TEMP_LOW_BYTE = 0x02
CONFIGURATION = 0x03
CONVERSION_RATE = 0x04
TEMP_HIGH_LIMIT_HIGH = 0x05
TEMP_HIGH_LIMIT_LOW = 0x06
TEMP_LOW_LIMIT_HIGH = 0x07
TEMP_LOW_LIMIT_LOW = 0x08
ONESHOT = 0x0f
THERM_LIMIT = 0x20
THERM_HYSTERESIS = 0x21
SMBUS_TIMEOUT_ENABLE = 0x22
PRODUCT_ID = 0xfd
MANUFACTUREID = 0xfe
REVISION_NUMBER = 0xff

# CONFIGURATION register bits
CONFIGURATION_MASK1 = 0b10000000
CONFIGURATION_STOP = 0b01000000
CONFIGURATION_TRES_9 = 0b00001000
CONFIGURATION_TRES_10 = 0b00000000
CONFIGURATION_TRES_11 = 0b00000100
CONFIGURATION_TRES_12 = 0b00001100
CONFIGURATION_TRES_MASK = 0b00001100

_TRES_MAP = {9: CONFIGURATION_TRES_9,
             10: CONFIGURATION_TRES_10,
             11: CONFIGURATION_TRES_11,
             12: CONFIGURATION_TRES_12}

# STATUS register bits
STATUS_BUSY = 0b10000000
STATUS_THIGH = 0b01000000
STATUS_LOW = 0b00100000
STATUS_THURM = 0b00000001

# SMBUS_TIMEOUT_ENABLE register bit
SMBUS_TIMEOUT = 0b10000000


class STTS751(I2CDev):
    """I2C Interface Class for ST STTS751 Temperature Sensor"""

    def __init__(self, i2c, addr=0x39):
        super(STTS751, self).__init__(i2c, addr)
        self.__standby_mode = False
        self.__last_temperature = 0.0

    def setup(self,
              standby=False,  # standby (one-shot) mode
              resolution=10,  # resolution : 9-12
              rate=0x04       # conversion rate : 1 conversion/sec
              ):
        """Setup the device"""
        config = 0
        self.__standby_mode = standby
        if standby:
            config |= CONFIGURATION_STOP
        config |= _TRES_MAP[resolution]
        self.write_byte_data(CONFIGURATION, config)
        self.write_byte_data(CONVERSION_RATE, rate & 0x0F)
        return self

    def update(self):
        """Update the latest measured temperature"""
        if self.__standby_mode:
            self.write_byte_data(ONESHOT, 1)
            time.sleep(0.02)
            while self.bits_on(STATUS, STATUS_BUSY):
                time.sleep(0.02)
        th = self.read_byte_data(TEMP_HIGH_BYTE)
        tl = self.read_byte_data(TEMP_LOW_BYTE)
        self.__last_temperature = b2ss(th, tl) / 256.0
        return self

    @property
    def temperature(self):
        """Last measured temperature (Celsius)"""
        return self.__last_temperature
