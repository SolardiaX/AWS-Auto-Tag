# AWS AUTO TAG

## About

AWS-Auto-Tag is an open to use solution that can tag AWS resources when they are being created. The tag can be set by a json format config, support use key/value with condition or expression, support set tag(s) from special service(s).

The application use CloudWatch Rule to listen CloudTrail Log and trigger Lambda function to tag the tags on event sources. A lots of services are already supported:

* AMI: CreateImage, CopyImage, RegisterImage
* Auto Scaling: CreateAutoScalingGroup
* CloudFormation: CreateChangeSet
* CloudFront: CreateDistribution
* CloudTrail: CreateTrail
* CloudWatch Rule: PutRule
* CloudWatch Log Group: CreateLogGroup
* Customer Gateway: CreateCustomerGateway
* Data Pipeline: CreatePipeline
* Dhcp Options: CreateDhcpOptions
* DynamoDB: CreateTable
* EBS: CreateVolume
* EC2: RunInstances
* EIP: AllocateAddress
* ELB(include ALB & NLB & CLIB): CreateLoadBalancer
* EMR: RunJobFlow
* ENI: CreateNetworkInterface
* IAM Role: CreateRole
* IAM User: CreateUser
* Internet Gateway: CreateInternetGateway
* Lambda Function: CreateFunction20150331, CreateFunction20141111
* NAT Gateway: CreateNatGateway
* Network ACL: CreateNetworkAcl
* KMS: GenerateDataKey
* RDS: CreateDBInstance
* Route Table: CreateRouteTable
* S3: CreateBucket
* Security Group: CreateSecurityGroup
* Snapshot: CreateSnapshot, CopySnapshot, ImportSnapshot
* Subnet: CreateSubnet
* VPC: CreateVpc
* VPCPeering: CreateVpcPeeringConnection
* VPN Connection: CreateVpnConnection
* VPN Gateway: CreateVpnGateway



This project contains all source code and supporting files that can be deployed with the SAM CLI. It includes the following files and folders.

- src - Source codes for the application's Lambda function.
- config - Config template and script to desgin and apply your own config.
- template.yaml - A template that defines the application's AWS resources.

## How to Use

### Prerequisites

* At least 1 AWS account
* CloudTrail should be enabled [(How to Enable](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-tutorial.html))
* Enable AKSK for an IAM user with admin role to deploy with SAM CLI

### Deploy

To deploy this application, you should use the Serverless Application Model Command Line Interface (SAM CLI), SAM CLI is an extension of the AWS CLI that adds functionality for building and testing Lambda applications. 

To use the SAM CLI, you need the following tools.

* AWS CLI - [How to Install](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-install.html)
* SAM CLI - [How to Install](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* Python3.9 (Only used for config runtime env. with cli) - [Download Python](https://www.python.org/downloads/)

> To deploy this application you must have a AKSK with IAM admin role.

Before use the SAM CLI, you should set up you aws cli credential first, run the following in your shell:

```bash
aws configure
```

For more information, please see the [AWS CLI document](https://docs.aws.amazon.com/zh_cn/cli/latest/userguide/cli-chap-configure.html).

To deploy your application for the first time, run the following in your shell:

To deploy your application for the first time, run the following in your shell:

```bash
sam build
sam deploy --guided --capabilities CAPABILITY_IAM CAPABILITY_NAMED_IAM
```

The first command will build the source of your application. The second command will package and deploy your application to AWS, with series of prompts:

* **Stack Name**

  The name of the stack to deploy to CloudFormation. This must be unique to your account and region.

* **AWS Region**

  The AWS region you want to deploy to.

* **Parameter EnableLog**

  Enable/Disable Lambda log. 


* **LogRetentionInDays**

  Logs of Lambda retention in days (-1 means always retention).

* **Confirm changes before deploy**

* If set to yes, any change sets will be shown to you before execution for manual review. If set to no, the AWS SAM CLI will automatically deploy application changes.

* **Allow SAM CLI IAM role creation**

  Many AWS SAM templates, including this example, create AWS IAM roles required for the AWS Lambda function(s) included to access AWS services. By default, these are scoped down to minimum required permissions.

* **Save arguments to samconfig.toml**

  If set to yes, your choices will be saved to a configuration file inside the project, so that in the future you can just re-run `sam deploy` without parameters to deploy changes to your application.

### Config

Application is using a lambda env. variable **CONFIG** to store the runtime option. The option is in json format:

```json
{
  "trigger": {
    "services": [
      {
        "cloudtrail": [
          "*"
        ]
      }
    ],
    "excluded": true
  },
  "tags": [
    {
      "key": "TaggedBy",
      "value": "auto-tag"
    },
    {
      "key": "TaggedAt",
      "value": "datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ')"
    },
    {
      "key": "ForSpecSerivces",
      "value": "true",
      "services": [
        "ec2",
        "ebs"
      ]
    },
    {
      "key": "AfterSpecTime",
      "value": "true",
      "services": [
        "s3"
      ],
      "condition": "time.strptime(event.detail.eventTime, '%Y-%m-%dT%H:%M:%SZ') > time.strptime('2022-02-02T22:22:22Z', '%Y-%m-%dT%H:%M:%SZ')"
    }
  ]
}
```

#### Format

* (dict)
  * **trigger** (dict) - Includes/Excludes services or service events to trigger the lambda to execute auto tag work. If it’s empty, means for all buildin supported services.
    * **services** (list) - The list of services or service events should include/exclude.
      * (dict) - A dict to define a service and events should include/exclude.
        * (key: string) - The sevice name, refer to the buildin defines in `src/config/supported.py`.
        * (value: list) - The service events, `*` means all supported events. refer to the buildin defines in `src/config/supported.py`.
    * **excluded** (bool) - If `true`, All services and events defined in `services` will be excluded. If `false`(by default), will only enable services and events defined in `services` to trigger tag work.
  * **tags** (list) - The tag(s) will to tag on AWS resources.
    * (dict) - A tag define.
      * **key** (string) - The `key` of tag, can be a static string or *<u>evaluable</u>* string expression. See `Expression`.
      * **value** (string) - The `value` of tag, can be a static string or *<u>evaluable</u>* string expression. See `Expression`.
      * **services** (list) - The special services the tag will be applied to. Refer to the buildin defines in `src/config/supported.py`.
      * **condition** (str) - Evaluable expression condition before tag the tag on resources, only the eval result is `true` the tag will can be applied. See `Expression`.

#### Expression

Auto-Tag support dynamic eval a string expression to and use the result for tag key/value or tag condition.

For expression used with tag key/value, the eval result **MUST** be `str`.

```python
datetime.datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ') # output current datetime in YYYY-MM-DDTHH:mm:ssZ format.
```

For expression used with tag condition, the eval result **MUST** be `bool`.

```python
time.strptime(event.detail.eventTime, '%Y-%m-%dT%H:%M:%SZ') > time.strptime('2022-02-02T22:22:22Z', '%Y-%m-%dT%H:%M:%SZ') # output whether the CloudTrail event time is after the UTC time 2022-02-02 22:22:22.
```



The string expression use `Python` script pattern with python buildin `datetime`, `time`, `math` modules support.

The original CloudTrail event is auto injected as `event` variable, and can be direct used in expression. This variable support python dict method and js dot style properties access.

```py
event.get('detail').get('eventTime')
event.detail.eventTIme
# both will output the event time value of event. 
# If the event original message is 
#	{
#		...
#		"detail": {
#			...
#			"eventTime": "2022-02-02T22:22:22Z",
#			"eventSource": "ec2.aws",
#			...
#		}
#	}
# The expression output will be `2022-02-02T22:22:22Z`
```

#### Apply

You can apply the config to lambda function by AWS Console GUI or execute a python script in your local cli.

* AWS Console

  In AWS Console navigate to Lambda, open the deployed function, switch to Environment tab and select Environment variables, add or edit the variable `CONFIG`.

* Python script

  In your local shell, goto the application sources directory, execute:

  ```python
  python config/apply.py -c <config_file> -n <function_name>
  ```

  This script support more arguments, please see the usage output by direct execute it will no args.

  ```python
  python config/apply.py
  ```

> Notes: Please apply the config each time after you update the application with sam deploy.

### Cost

Application just use Lambda functions and output log to CloudWatch log groups (optional), so it is almost free to use.

## Develop

Application is coding with Python3.9, you can use any favor tool to code with them.

If you prefer to use an integrated development environment (IDE) to build and test your application, you can use the AWS Toolkit. See the following links to get started.

* [CLion](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [GoLand](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [IntelliJ](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [WebStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [Rider](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PhpStorm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [PyCharm](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [RubyMine](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [DataGrip](https://docs.aws.amazon.com/toolkit-for-jetbrains/latest/userguide/welcome.html)
* [VS Code](https://docs.aws.amazon.com/toolkit-for-vscode/latest/userguide/welcome.html)
* [Visual Studio](https://docs.aws.amazon.com/toolkit-for-visual-studio/latest/user-guide/welcome.html)



The main resources and codes are list bellow, more details can check the comments in sources.

```shell
.
├── LICENSE
├── README.md
├── config
│   ├── apply.py						# The script to apply config.
│   └── config.json					# The json format config template file.
├── requirements.txt
├── src
│   ├── __init__.py
│   ├── config
│   │   ├── __init__.py
│   │   ├── loader.py				# The config loader to load config from Lambda env.
│   │   ├── supported.py		# The default buildin supported AWS services and events.
│   │   └── types.py				# The type define for config.
│   ├── evals.py						# Function to eval condition and expression.
│   ├── listener.py					# The lambda function to listner the CloudTrail event to tag resources.
│   └── worker
│       ├── __init__.py
│       ├── registrable.py	# A helper class to auto register services tag workers.
│       ├── services
│       │   └── ...					# Tag workers implamentation for AWS services.
│       └── worker.py				# Base class define of tag workers.
└── template.yaml						# The SAM template files, includes all required AWS resources & policies defined.
```

## References

Reference documents to use and custom this application can be found at:

* [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)
* [AWS Command Line Interface Documentation](https://docs.aws.amazon.com/cli/)
* [AWS Serverless Application Model Developer Guide](https://docs.aws.amazon.com/serverless-application-model/index.html)
* [AWS CloudFormation User Guide](https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/Welcome.html)
* [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
* [AWS CloudTrail Documentation](https://docs.aws.amazon.com/cloudtrail)
