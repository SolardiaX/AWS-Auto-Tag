# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.worker.__init__.py
~~~~~~~~~~~~~~~~~~~
Exported workers of AutoTag

:license: MIT, see LICENSE for more details.
"""

from worker.worker import DictX, Worker
from worker.services.ami import AMIWorker
from worker.services.autoscaling import AutoScalingWorker
from worker.services.cloudformation import CloudFormationWorker
from worker.services.cloudfront import CloudFrontWorker
from worker.services.cloudtrail import CloudTrailWorker
from worker.services.cloudwatch_alarm import CloudWatchAlarmWorker
from worker.services.cloudwatch_loggroup import CloudWatchLogGroupWorker
from worker.services.cloudwatch_rule import CloudWatchRuleWorker
from worker.services.customer_gateway import CustomerGatewayWorker
from worker.services.data_pipeline import DataPipelineWorker
from worker.services.dhcp_options import DhcpOptionWorker
from worker.services.dynamodb import DynamoDBWorker
from worker.services.ebs import EBSWorker
from worker.services.ec2 import EC2Worker
from worker.services.efs import EFSWorker
from worker.services.eip import EIPWorker
from worker.services.elb import ELBWorker
from worker.services.emr import EMRWorker
from worker.services.eni import ENIWorker
from worker.services.iam_role import IAMRoleWorker
from worker.services.iam_user import IAMUserWorker
from worker.services.internet_gateway import InternetGatewayWorker
from worker.services.kms import KMSWorker
from worker.services.lambda_function import LambdaWorker
from worker.services.nat_gateway import NatGatewayWorker
from worker.services.network_acl import NetworkACLWorker
from worker.services.rds import RDSWorker
from worker.services.route_table import RouteTableWorker
from worker.services.s3 import S3Worker
from worker.services.security_group import SecurityGroupWorker
from worker.services.snapshot import SnapshotWorker
from worker.services.subnet import SubnetWorker
from worker.services.vpc_peering import VPCPeeringWorker
from worker.services.vpc import VPCWorker
from worker.services.vpn_connection import VPNConnectionWorker

__all__ = [
    'DictX',
    'Worker',
    'AMIWorker',
    'AutoScalingWorker',
    'CloudFormationWorker',
    'CloudFrontWorker',
    'CloudTrailWorker',
    'CloudWatchAlarmWorker',
    'CloudWatchLogGroupWorker',
    'CloudWatchRuleWorker',
    'CustomerGatewayWorker',
    'DataPipelineWorker',
    'DhcpOptionWorker',
    'DynamoDBWorker',
    'EBSWorker',
    'EC2Worker',
    'EFSWorker',
    'EIPWorker',
    'ELBWorker',
    'EMRWorker',
    'ENIWorker',
    'IAMRoleWorker',
    'IAMUserWorker',
    'InternetGatewayWorker',
    'KMSWorker',
    'LambdaWorker',
    'NatGatewayWorker',
    'NetworkACLWorker',
    'RDSWorker',
    'RouteTableWorker',
    'S3Worker',
    'SecurityGroupWorker',
    'SnapshotWorker',
    'SubnetWorker',
    'VPCPeeringWorker',
    'VPCWorker',
    'VPNConnectionWorker',
]
