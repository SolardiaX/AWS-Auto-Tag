# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.efs
~~~~~~~~~~~~~~~~~~~
description of efs

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("efs")
class EFSWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("efs")

    @property
    def _filesystem_id(self) -> str:
        return self.context.responseElements.fileSystemId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_resource(
            ResourceId=self._filesystem_id,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'efs': self._filesystem_id}
