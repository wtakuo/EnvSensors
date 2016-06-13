# EnvSensors: A Python Library for I2C Environmental Sensors
# Copyright (C) 2016, Takuo Watanabe

from setuptools import setup

setup(
    name="EnvSensors",
    version="0.0.0dev1",
    author="Takuo Watanabe",
    author_email="wtakuo@mac.com",
    description="A Python Library for I2C Environmental Sensors",
    license="MIT",
    keywords="sensors i2c",
    url="https://github.com/wtakuo/EnvSensors",
    packages=['envsensors'],
    install_requires=['smbus'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License"
    ]
)
