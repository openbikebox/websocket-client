# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import json
import logging
import asyncio
import websockets
from base64 import b64encode
from .config import Config as config
from .helper import DefaultJSONEncoder
from .websocket_message import WebsocketMessage
from .websocket_queue import websocket_queue


class Websocket:
    running_messages = {}

    def __init__(self):
        self.logger = logging.getLogger('websocket')
        self.logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_format = logging.Formatter('%(message)s')
        console_handler.setFormatter(console_format)
        self.logger.addHandler(console_handler)

    async def startup(self):
        while True:
            try:
                if not await self.connect_websocket():
                    continue
                consumer_task = asyncio.create_task(
                    self.consumer_handler()
                )
                producer_task = asyncio.create_task(
                    self.producer_handler()
                )
                done, pending = await asyncio.wait(
                    [consumer_task, producer_task],
                    return_when=asyncio.ALL_COMPLETED
                )
                for task in pending:
                    task.cancel()
            except websockets.exceptions.ConnectionClosedError:
                pass

    async def connect_websocket(self):
        try:
            self.connection = await websockets.client.connect(
                config.OBB_CONNECT_URL,
                extra_headers=[('Authorization', 'Basic ' + b64encode(b'client-1:password').decode())]
            )
            if self.connection.open:
                return True
        except ConnectionRefusedError:
            print('cannot connect to backend, retry ...')
            await asyncio.sleep(2)
            return False

    async def consumer_handler(self):
        async for message in self.connection:
            process_message = await self.consumer(message)
            if process_message == "onClose":
                asyncio.get_event_loop().stop()
                asyncio.get_event_loop().close()

    async def consumer(self, message):
        data = json.loads(message)
        self.log('<< %s ' % data)
        msg = WebsocketMessage(data)
        if msg.reply:
            websocket_queue.reply(msg.type, msg.uid, msg.reply)

    async def producer_handler(self):
        while True:
            message = await self.producer()
            self.log('>> %s' % message)
            await self.connection.send(json.dumps(message, cls=DefaultJSONEncoder))

    async def producer(self):
        result = await websocket_queue.queue.get()
        websocket_queue.queue.task_done()
        return result

    def log(self, message):
        self.logger.info(message)


websocket = Websocket()
