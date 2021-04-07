# encoding: utf-8

"""
openbikebox websocket-client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from .config import Config
from .system import system


class WebsocketMessage:
    reply = None

    def __init__(self, message):
        self.type = message['type']
        self.state = message['state']
        self.uid = message['uid']
        self.data = message['data']

        if hasattr(self, 'handle%s' % self.type):
            getattr(self, 'handle%s' % self.type)()

    def handleRemoteChangeResourceStatus(self):
        if self.data.get('uid') not in Config.RESOURCES or self.data.get('status') not in ['open', 'closed']:
            self.reply = {'status': 'fail'}
            return
        if self.data['status'] == 'open':
            system.resources[self.data.get('uid')].open()
        else:
            system.resources[self.data.get('uid')].close()
        self.reply = {'status': 'ok'}

    def handleAuthorizeReply(self):
        system.take_resource(self.data['request_uid'], self.data['resource_uid'])
