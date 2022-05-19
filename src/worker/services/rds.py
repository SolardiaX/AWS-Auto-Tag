# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.rds
~~~~~~~~~~~~~~~~~~~
description of rds

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("rds")
class RDSWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("rds")

    @property
    def _db_arn(self) -> str:
        if self.context.responseElements.dBInstanceArn is not None:
            return self.context.responseElements.dBInstanceArn

        arn = ['arn', self._aws_id, 'rds',
               self._aws_region,
               self._account_id,
               'db',
               self.context.responseElements.dBInstanceIdentifier]
        return ':'.join(arn)

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.add_tags_to_resource(
            ResourceName=self._db_arn,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'rds': self._db_arn}
