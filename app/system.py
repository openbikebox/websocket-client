# encoding: utf-8

"""
openbikebox client
Copyright (c) 2021, binary butterfly GmbH
Use of this source code is governed by an MIT-style license that can be found in the LICENSE file.
"""

from uuid import uuid4
from base64 import b64encode
from .config import Config
from .resource import Resource
from .websocket_queue import websocket_queue


class System:
    resources = {}
    auth_requests = {}

    def __init__(self):
        for resource_uid, resource_gpio in Config.RESOURCES.items():
            self.resources[resource_uid] = Resource(resource_gpio, resource_uid)

    def handle_card(self, token_type, token_identifier):
        pos = token_identifier.find(b'\x5f\x20\x07')
        if pos == -1:
            return
        uid = token_identifier[pos + 3:pos + 10]
        for resource in self.resources.values():
            if resource.owner_type == 'emobility-card' and resource.owner_identifier == uid:
                resource.flip_open_close()
                return

        # todo: timeout / clear auth_requests
        request_uid = str(uuid4())
        self.auth_requests[request_uid] = {
            'token_type': token_type,
            'token_identifier': uid
        }
        websocket_queue.request('Authorize', {
            'request_uid': request_uid,
            'token_type': token_type,
            'token_identifier': b64encode(token_identifier).decode()
        })

    def take_resource(self, request_uid, resource_uid):
        if request_uid not in self.auth_requests or resource_uid not in self.resources:
            return
        self.resources[resource_uid].take(
            self.auth_requests[request_uid]['token_type'],
            self.auth_requests[request_uid]['token_identifier']
        )
        del self.auth_requests[request_uid]


system = System()
