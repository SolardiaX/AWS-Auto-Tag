# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.snapshot
~~~~~~~~~~~~~~~~~~~
description of snapshot

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("snapshot")
class SnapshotWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _snapshot_id(self) -> str:
        return self.context.responseElements.snapshotId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._snapshot_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'snapshot': self._snapshot_id}
