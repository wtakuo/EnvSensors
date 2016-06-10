import smbus
import bme280


def main():
    i2c = smbus.SMBus(1)
    s = bme280.BME280(i2c)
    if s.read_byte_data(0xD0) == 0x60:
        s.setup()
        s.update()
        (t, p, h) = s.get_values()
        print("temperature : %7.2f C" % t)
        print("pressure    : %7.2f hPa" % p)
        print("humidity    : %7.2f %%" % h)


if __name__ == '__main__':
    main()
