# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.ec2
~~~~~~~~~~~~~~~~~~~
description of ec2

:license: MIT, see LICENSE for more details.
"""
from __future__ import annotations

import boto3
from worker.worker import DictX, Worker


@Worker.register("ec2")
class EC2Worker(Worker):
    @property
    def client(self) -> any:
        return boto3.client("ec2")

    @property
    def _instances(self) -> list:
        if self.context.responseElements is None:
            # auto-scaling-group or opworks starts ec2 instances
            return []

        return self.context.responseElements.instancesSet.items

    @property
    def _instance_ids(self) -> list[str]:
        return [instance.instanceId for instance in self._instances if instance.instanceId is not None]

    def _get_ec2_instances(self) -> DictX:
        ec2_insts = self.client.describe_instances(InstanceIds=self._instance_ids)
        return DictX(ec2_insts)

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        if len(self._instances) == 0:
            return dict()

        instances = self._get_ec2_instances()
        if len(instances) == 0 or instances.Reservations is None or len(instances.Reservations) == 0:
            return dict()

        target: dict[str, str | list[str] | None] = {}
        for instance in instances.Reservations[0].Instances:
            resource_ids = []

            instance_id = instance.InstanceId
            resource_ids.append(instance_id)

            ebs_ids = [device.Ebs.VolumeId for device in instance.BlockDeviceMappings]
            resource_ids.extend(ebs_ids)

            eni_ids = [eni.NetworkInterfaceId for eni in instance.NetworkInterfaces]
            resource_ids.extend(eni_ids)

            target['ec2'] = target.get('ec2', []) + [instance_id]
            target['ebs'] = target.get('ebs', []) + ebs_ids
            target['eni'] = target.get('eni', []) + eni_ids

            self.client.create_tags(
                Resources=resource_ids,
                Tags=[{'Key': key, 'Value': val} for key, val in tags.items()]
            )

        return target
