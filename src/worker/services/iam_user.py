# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.iam_user
~~~~~~~~~~~~~~~~~~~
description of iam_user

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("iamuser")
class IAMUserWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("iam")

    @property
    def _user_name(self) -> str:
        return self.context.responseElements.user.userName

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_user(
            RoleName=self._user_name,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'iamuser': self._user_name}
