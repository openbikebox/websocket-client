# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""


import asyncio
from uuid import uuid4


class WebsocketQueue:

    def startup(self):
        self.queue = asyncio.Queue()

    def request(self, message_type, message):
        self.queue.put_nowait({
            'uid': str(uuid4()),
            'state': 'request',
            'type': message_type,
            'data': message
        })

    def reply(self, message_type, message_uid, message):
        self.queue.put_nowait({
            'uid': message_uid,
            'state': 'reply',
            'type': message_type,
            'data': message
        })


websocket_queue = WebsocketQueue()

