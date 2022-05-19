# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.autoscaling
~~~~~~~~~~~~~~~~~~~
description of autoscaling

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("autoscaling")
class AutoScalingWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("autoscaling")

    @property
    def _autoscaling_group_name(self) -> str:
        return self.context.requestParameters.autoScalingGroupName

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_or_update_tags(
            Tags=[
                {
                    'Key': key,
                    'Value': val,
                    'ResourceId': self._autoscaling_group_name,
                    'ResourceType': 'auto-scaling-group',
                    'PropagateAtLaunch': False,
                }
                for key, val in tags.items()
            ]
        )

        return {'autoscaling': self._autoscaling_group_name}
