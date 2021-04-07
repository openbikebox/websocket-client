# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import RPi.GPIO as GPIO
from .config import Config


class Gpio:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        for resource_uid in Config.RESOURCES.values():
            GPIO.setup(resource_uid, GPIO.OUT)

    def set_resource_open(self, gpio_pin):
        GPIO.output(gpio_pin, GPIO.HIGH)

    def set_resource_closed(self, gpio_pin):
        GPIO.output(gpio_pin, GPIO.LOW)

    def __del__(self):
        GPIO.cleanup()


gpio = Gpio()
