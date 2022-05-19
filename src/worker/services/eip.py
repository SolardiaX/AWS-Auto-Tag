# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.eip
~~~~~~~~~~~~~~~~~~~
description of eip

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("eip")
class EIPWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _allocation_id(self) -> str:
        return self.context.responseElements.allocationId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._allocation_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'eip': self._allocation_id}
