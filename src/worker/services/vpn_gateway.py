# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.vpn_gateway
~~~~~~~~~~~~~~~~~~~
description of vpn_gateway

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("vpngateway")
class VPNGatewayWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _gateway_id(self) -> str:
        return self.context.responseElements.vpnGateway.vpnGatewayId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._gateway_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'vpngateway': self._gateway_id}
