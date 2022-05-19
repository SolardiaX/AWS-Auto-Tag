# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.iam_role
~~~~~~~~~~~~~~~~~~~
description of iam_role

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("iamrole")
class IAMRoleWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("iam")

    @property
    def _role_name(self) -> str:
        return self.context.responseElements.role.roleName

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_role(
            RoleName=self._role_name,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'iamrole': self._role_name}
