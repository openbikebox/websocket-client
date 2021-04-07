# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

import asyncio
from base64 import b64encode
from .config import Config
from .system import system


class Cardreader:
    async def startup(self):
        reader, writer = await asyncio.open_connection(Config.CARDREADER_SERVER, Config.CARDREADER_PORT)
        socket_reader_task = asyncio.create_task(
            self.socket_reader_task(reader)
        )
        done, pending = await asyncio.wait(
            [socket_reader_task],
            return_when=asyncio.ALL_COMPLETED,
        )

    async def socket_reader_task(self, reader):
        while True:
            try:
                message = await reader.readuntil(b'\x90\x00\x00\x00')
            except asyncio.IncompleteReadError:
                return
            if message[0] < 0x70:
                continue
            system.handle_card('emobility-card', message[0:-4])


cardreader = Cardreader()

