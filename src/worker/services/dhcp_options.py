# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.dhcp_options
~~~~~~~~~~~~~~~~~~~
description of dhcp_options

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("dhcpoptions")
class DhcpOptionWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("ec2")

    @property
    def _dhcp_options_id(self) -> str:
        return self.context.responseElements.dhcpOptions.dhcpOptionsId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.create_tags(
            Resources=[self._dhcp_options_id],
            Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
        )

        return {'dhcp_options': self._dhcp_options_id}
