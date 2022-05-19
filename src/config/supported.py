# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.config.supported
~~~~~~~~~~~~~~~~~~~
Supported AWS Sevices event triggers of AutoTag

:license: MIT, see LICENSE for more details.
"""

from config.types import Trigger

__events__ = [
    {'ami': ['CreateImage', 'CopyImage', 'RegisterImage']},
    {'autoscaling': ['CreateAutoScalingGroup']},
    {'cloudformation': ['CreateChangeSet']},
    {'cloudfront': ['CreateDistribution']},
    {'cloudtrail': ['CreateTrail']},
    {'cloudwatchrule': ['PutRule']},
    {'cloudwatchloggroup': ['CreateLogGroup']},
    {'customergateway': ['CreateCustomerGateway']},
    {'datapipeline': ['CreatePipeline']},
    {'dhcpoptions': ['CreateDhcpOptions']},
    {'dynamodb': ['CreateTable']},
    {'ebs': ['CreateVolume']},
    {'ec2': ['RunInstances']},
    {'eip': ['AllocateAddress']},
    {'elb': ['CreateLoadBalancer']},
    {'emr': ['RunJobFlow']},
    {'eni': ['CreateNetworkInterface']},
    {'iamrole': ['CreateRole']},
    {'iamuser': ['CreateUser']},
    {'internetgateway': ['CreateInternetGateway']},
    {'lambdafunction': ['CreateFunction20150331', 'CreateFunction20141111']},
    {'natgateway': ['CreateNatGateway']},
    {'networkacl': ['CreateNetworkAcl']},
    {'kms': ['GenerateDataKey']},
    {'rds': ['CreateDBInstance']},
    {'routetable': ['CreateRouteTable']},
    {'s3': ['CreateBucket']},
    {'securitygroup': ['CreateSecurityGroup']},
    {'snapshot': ['CreateSnapshot', 'CopySnapshot', 'ImportSnapshot']},
    {'subnet': ['CreateSubnet']},
    {'vpc': ['CreateVpc']},
    {'vpcpeering': ['CreateVpcPeeringConnection']},
    {'vpnconnection': ['CreateVpnConnection']},
    {'vpngateway': ['CreateVpnGateway']},
]

SupportedTriggers: list[Trigger] = [Trigger(list(item.keys())[0], list(item.values())[0]) for item in __events__]
