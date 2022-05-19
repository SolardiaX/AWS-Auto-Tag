# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.ebs
~~~~~~~~~~~~~~~~~~~
description of ebs

:license: MIT, see LICENSE for more details.
"""


from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("ebs")
class EBSWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _volume_id(self) -> str:
        return self.context.responseElements.volumeId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._volume_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'ebs': self._volume_id}
