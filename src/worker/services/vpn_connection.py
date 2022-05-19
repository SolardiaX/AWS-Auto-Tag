# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.vpn_connection
~~~~~~~~~~~~~~~~~~~
description of vpn_connection

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("vpnconnection")
class VPNConnectionWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _connection_id(self) -> str:
        return self.context.responseElements.vpnConnection.vpnConnectionId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._connection_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'vpnconnection': self._connection_id}
