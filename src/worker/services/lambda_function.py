# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.lambda
~~~~~~~~~~~~~~~~~~~
description of lambda

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("lambdafunction")
class LambdaWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("lambda")

    @property
    def _lambda_arn(self) -> str:
        return self.context.responseElements.functionArn

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_resource(
            Resource=self._lambda_arn,
            Tags=tags
        )

        return {'lambda': self._lambda_arn}
