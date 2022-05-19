# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.cloudformation
~~~~~~~~~~~~~~~~~~~
description of cloudformation

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("cloudformation")
class CloudFormationWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("cloudformation")

    @property
    def _stack_name(self) -> str:
        return self.context.requestParameters.stackName

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.update_stack(
            StackName=self._stack_name,
            UsePreviousTemplate=True,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'cloudformation': self._stack_name}
