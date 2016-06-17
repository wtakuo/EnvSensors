# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

import time
from i2cdev import I2CDev
from util import b2ss

# I2C registers
TEMP_HIGH_BYTE = 0x00
TEMP_LOW_BYTE = 0x01
STATUS = 0x02
# 3:0 0000 unused
# 4 0 TLOW
# 5 0 THIGH
# 6 0 TCRIT
# 7 1 ~RDY
CONFIGURATION = 0x03
# 1:0 00 Fault queue
# 2   0  CT pin polarity
# 3   0  INT pin polarity
# 4   0  INT/CT mode
# 6:5 00 Operation mode
#        00:continuous convertion, 01:one shot, 10:1 SPS mode, 11:shutdown
# 7   0  resolution (0:13-bit, 1:16-bit)
THIGH_SETPOINT_HIGH_BYTE = 0x04
THIGH_SETPOINT_LOW_BYTE = 0x05
TLOW_SETPOINT_HIGH_BYTE = 0x06
TLOW_SETPOINT_LOW_BYTE = 0x07
TCRIT_SETPOINT_HIGH_BYTE = 0x08
TCRIT_SETPOINT_LOW_BYTE = 0x09
THYST_SETPOINT = 0x0a
ID = 0x0b
SOFTWARE_RESET = 0x2f

CONFIGURATION_RESOLUTION = 0b10000000
CONFIGURATION_MODE_MASK = 0b01100000
CONFIGURATION_CONTINUOUS_MODE = 0b00000000
CONFIGURATION_ONESHOT_MODE = 0b00100000
CONFIGURATION_1SPS_MODE = 0b01000000
CONFIGURATION_SHUTDOWN_MODE = 0b01100000


class ADT7410(I2CDev):
    """I2C Interface Class for Analog Devices ADT7410 Temperature Sensor"""

    def __init__(self, i2c, addr=0x48):
        super(ADT7410, self).__init__(i2c, addr)
        self.__last_temperature = 0.0

    def setup(self):
        """Setup the device"""
        dev_id = self.read_byte_data(ID)
        if dev_id & 0xf8 != 0xc8:
            raise IOError('Invalid device ID', dev_id)
        self.write_byte(SOFTWARE_RESET)
        time.sleep(0.25)
        conf = CONFIGURATION_RESOLUTION | CONFIGURATION_CONTINUOUS_MODE
        self.write_byte_data(CONFIGURATION, conf)
        return self

    def update(self):
        """Update the latest measured values"""
        w = self.read_word_data(TEMP_HIGH_BYTE)
        self.__last_temperature = b2ss(w & 0xff, w >> 8) / 128.0
        return self

    @property
    def temperature(self):
        """Last measured temperature (Celsius)"""
        return self.__last_temperature
