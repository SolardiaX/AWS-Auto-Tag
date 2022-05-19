# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.cloudwatch_alarm
~~~~~~~~~~~~~~~~~~~
description of cloudwatch_alarm

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("cloudwatchalarm")
class CloudWatchAlarmWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("cloudwatch")

    @property
    def _alarm_arn(self) -> str:
        arn = ['arn', self._aws_id, 'cloudwatch',
               self._aws_region,
               self._account_id,
               'alarm',
               self.context.requestParameters.alarmName]
        return ':'.join(arn)

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.tag_resource(
            ResourceARN=self._alarm_arn,
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'cloudwatch:alarm': self._alarm_arn}
