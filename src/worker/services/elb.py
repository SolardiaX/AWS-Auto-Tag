# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.elb
~~~~~~~~~~~~~~~~~~~
description of elb

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("elb")
class ELBWorker(Worker):
    @property
    def _client(self) -> any:
        if self._is_loadbalancer_v2:
            return boto3.client("elbv2")

        return boto3.client("elb")

    @property
    def _is_loadbalancer_v2(self) -> bool:
        return self.context.responseElements.loadBalancers is not None \
                and self.context.responseElements.loadBalancers[0] is not None \
                and self.context.responseElements.loadBalancers[0].loadBalancerArn is not None

    @property
    def _loadbalancer_name(self) -> str:
        return self.context.responseElements.loadBalancers[0].loadBalancerName \
            if self._is_loadbalancer_v2 else self.context.requestParameters.loadBalancerName

    def _loadbalancer_arn(self) -> str:
        return self.context.responseElements.loadBalancers[0].loadBalancerArn if self._is_loadbalancer_v2 else None

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        if self._is_loadbalancer_v2:
            self._client.add_tags(
                ResourceArns=[self._loadbalancer_arn],
                Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
            )
        else:
            self._client.add_tags(
                LoadBalancerNames=[self._loadbalancer_name],
                Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
            )

        return {'elb': self._loadbalancer_name}
