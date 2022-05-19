# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.data_pipeline
~~~~~~~~~~~~~~~~~~~
description of data_pipeline

:license: MIT, see LICENSE for more details.
"""

from __future__ import annotations

import boto3
from worker.worker import Worker


@Worker.register("datapipeline")
class DataPipelineWorker(Worker):
    @property
    def _client(self) -> any:
        return boto3.client("datapipeline")

    @property
    def _pipeline_id(self) -> str:
        return self.context.responseElements.pipelineId

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        self._client.add_tags(
            pipelineId=self._pipeline_id,
            tags=tags
        )

        return {'ami': self._pipeline_id}
