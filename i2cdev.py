# envsensors: I2C Interface Classes for Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe


class I2CDev(object):
    """Common class for I2C devices"""

    def __init__(self, i2c, addr):
        self.__i2c = i2c
        self.__addr = addr

    def read_byte_data(self, reg):
        """Read a single byte from a register."""
        return self.__i2c.read_byte_data(self.__addr, reg)

    def read_word_data(self, reg):
        """Read a single word (16 bits) from a register."""
        return self.__i2c.read_word_data(self.__addr, reg)

    def write_byte(self, reg):
        """Perform a write operation to a register."""
        self.__i2c.write_byte(self.__addr, reg)

    def write_byte_data(self, reg, val):
        """Write a single byte to a register."""
        self.__i2c.write_byte_data(self.__addr, reg, val)

    def set_bits(self, reg, bits, mask=0):
        """Set specified bits in a register."""
        d = self.read_byte_data(reg)
        d &= ~mask
        d |= bits
        self.write_byte_data(reg, d)

    def unset_bits(self, reg, bits):
        """Unset specified bits in a register."""
        d = self.read_byte_data(reg)
        d &= ~bits
        self.write_byte_data(reg, d)

    def bits_on(self, reg, bits):
        """Tests if all of the specified bits are on in a register."""
        d = self.read_byte_data(reg)
        return d & bits == bits

    def bits_off(self, reg, bits):
        """Tests if all of the specified bits are off in a register."""
        d = self.read_byte_data(reg)
        return d & ~bits == d
