# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.ami
~~~~~~~~~~~~~~~~~~~
description of ami

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("ami")
class AMIWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _image_id(self) -> str:
        return self.context.responseElements.imageId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._image_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'ami': self._image_id}
