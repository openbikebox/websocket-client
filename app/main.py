# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import asyncio
from .websocket import websocket
from .cardreader import cardreader
from .websocket_queue import websocket_queue


class Main:

    def __init__(self):
        asyncio.run(self.startup())

    async def startup(self):
        websocket_queue.startup()
        websocket_task = asyncio.create_task(websocket.startup())
        cardreader_task = asyncio.create_task(cardreader.startup())
        done, pending = await asyncio.wait(
            [websocket_task],
            return_when=asyncio.ALL_COMPLETED
        )
        for task in pending:
            task.cancel()

