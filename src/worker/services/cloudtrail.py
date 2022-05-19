# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.cloudtrail
~~~~~~~~~~~~~~~~~~~
description of cloudtrail

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("cloudtrail")
class CloudTrailWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("cloudtrail")

    @property
    def _trail_arn(self) -> str:
        return self.context.responseElements.trailARN

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.add_tags(
            ResourceId=self._trail_arn,
            TagsList=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'cloudtrail': self._trail_arn}
