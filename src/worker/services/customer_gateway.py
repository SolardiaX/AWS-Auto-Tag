# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.customer_gateway
~~~~~~~~~~~~~~~~~~~
description of customer_gateway

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("customergateway")
class CustomerGatewayWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _gateway_id(self) -> str:
        return self.context.responseElements.customerGateway.customerGatewayId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._gateway_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'customergateway': self._gateway_id}
