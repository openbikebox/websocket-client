# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from .gpio import gpio
from .websocket_queue import websocket_queue


class Resource:
    status = 'closed'
    owner_type = None
    owner_identifier = None

    def __init__(self, gpio_pin, uid):
        self.gpio_pin = gpio_pin
        self.uid = uid

    def open(self):
        # todo: auto-close
        if self.status == 'open':
            return
        self.status = 'open'
        gpio.set_resource_open(self.gpio_pin)
        websocket_queue.request('ResourceStatusChange', {'resource_uid': self.uid, 'status': 'open'})

    def close(self):
        if self.status == 'closed':
            return
        self.status = 'closed'
        gpio.set_resource_closed(self.gpio_pin)
        websocket_queue.request('ResourceStatusChange', {'resource_uid': self.uid, 'status': 'closed'})

    def flip_open_close(self):
        self.close() if self.status == 'open' else self.open()

    def take(self, owner_type, owner_identifier):
        self.owner_type = owner_type
        self.owner_identifier = owner_identifier
        self.open()

