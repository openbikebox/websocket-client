# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""


class Config:
    CLIENT_UID = 'client-1'
    CLIENT_PASSWORD = 'password'

    OBB_CONNECT_URL = 'ws://your-server:port/connect/%s' % CLIENT_UID

    CARDREADER_SERVER = 'localhost'
    CARDREADER_PORT = 9000

    RESOURCES = {
        'resource-1': 17,
        'resource-2': 27,
        'resource-3': 22,
        'resource-4': 18
    }
