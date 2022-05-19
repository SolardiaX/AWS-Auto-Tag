# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.network_acl
~~~~~~~~~~~~~~~~~~~
description of network_acl

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("networkacl")
class NetworkACLWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _network_acl_id(self) -> str:
        return self.context.responseElements.networkAcl.networkAclId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._network_acl_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'nacl': self._network_acl_id}
