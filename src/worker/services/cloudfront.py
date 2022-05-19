# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.cloudfront
~~~~~~~~~~~~~~~~~~~
description of cloudfront

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("cloudfront")
class CloudFrontWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("cloudfront")

    @property
    def _arn(self) -> str:
        return self.context.responseElements.distribution.aRN

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_resource(
            Resource=self._arn,
            Tags={'Items': [{'Key': key, 'Value': val} for key, val in tags.items()]}
        )

        return {'cloudfront': self._arn}
