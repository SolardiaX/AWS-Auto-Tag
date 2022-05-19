# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.security_group
~~~~~~~~~~~~~~~~~~~
description of security_group

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("securitygroup")
class SecurityGroupWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _group_id(self) -> str:
        return self.context.responseElements.groupId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._group_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'securitygroup': self._group_id}
