# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.dynamodb
~~~~~~~~~~~~~~~~~~~
description of dynamodb

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("dynamodb")
class DynamoDBWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("dynamodb")

    @property
    def _table_arn(self) -> str:
        return self.context.responseElements.tableDescription.tableArn

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_resource(
            ResourceArn=self._table_arn,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'dynamodb': self._table_arn}
