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

    def set_default(self):
        """Setup the device with default configuration"""
        self.write_byte_data(CONFIGURATION, 0x00)
        self.write_byte_data(CONVERSION_RATE, 0x04)
        self.__standby_mode = False

    def set_standby_mode(self):
        """Set the device to standby mode."""
        self.set_bits(CONFIGURATION, CONFIGURATION_STOP)
        self.__standby_mode = True

    def set_continuous_mode(self):
        """Set the device to conitnuous conversion mode."""
        self.unset_bits(CONFIGURATION, CONFIGURATION_STOP)
        self.__standby_mode = False

    def set_resolution(self, res):
        """Set the temperature resolution. The argument must be in [9..12]."""
        self.set_bits(CONFIGURATION, _TRES_MAP[res], CONFIGURATION_TRES_MASK)

    def set_conversion_rate(self, rate):
        """Set the conversion rate."""
        self.write_byte_data(CONVERSION_RATE, rate & 0x0f)

    def get_temperature(self):
        """Returns the current temperature as a floating-point number."""
        if self.__standby_mode:
            self.write_byte_data(ONESHOT, 1)
            time.sleep(0.01)
            while self.bits_on(STATUS, STATUS_BUSY):
                time.sleep(0.02)
        th = self.read_byte_data(TEMP_HIGH_BYTE)
        tl = self.read_byte_data(TEMP_LOW_BYTE)
        return b2ss(th, tl) / 256.0
