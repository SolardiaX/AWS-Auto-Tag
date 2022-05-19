# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.subnet
~~~~~~~~~~~~~~~~~~~
description of subnet

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("subnet")
class SubnetWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _subnet_id(self) -> str:
        return self.context.responseElements.subnet.subnetId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._subnet_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'subnet': self._subnet_id}
