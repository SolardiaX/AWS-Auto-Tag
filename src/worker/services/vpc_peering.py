# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.vpc_peering
~~~~~~~~~~~~~~~~~~~
description of vpc_peering

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("vpcpeering")
class VPCPeeringWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _peering_id(self) -> str:
        return self.context.responseElements.vpcPeeringConnection.vpcPeeringConnectionId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._peering_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'vpcpeering': self._peering_id}
