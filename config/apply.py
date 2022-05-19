# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.apply
~~~~~~~~~~~~~~~~~~~
description of apply

:license: GPL-3.0, see LICENSE for more details.
"""

import boto3
import getopt
import json
import sys


def usage(code=0):
    print("Usage:")
    print("\tconfig.py -c <config_file> -n <function_name> [-p <profile_name>] [-r <region_name>]")
    print("\tconfig.py --config=<config_file> --name=<function_name> [--profile=<profile_name>] [--region=<region_name>] [--nolog]")
    print("Args:")
    print("\t-c | --config : The config json file used with Auto-Tag")
    print("\t-n | --name : The Auto-Tag Lambda function name created by sam deploy")
    print("\t-p | --profile : The aws cli credential profile name. If not set, default credential will be used.")
    print("\t-r | --region : The Region of the Auto-Tag created by sam deploy. default region will be used.")
    print("\t--nolog : Disable log output to CloudWatch Log Group.")
    sys.exit(code)


def set_config(argv: list[str]):
    cfg_file = None
    name = None
    profile = None
    region = None
    enable_log = True

    opts: list[tuple[str, str]] = list()

    try:
        opts, _ = getopt.getopt(argv, "hc:n:p:r:", ["config=", "name=", "profile=", "region=", "nolog"])
    except getopt.GetoptError:
        usage(2)

    for opt, arg in opts:
        if opt == "-h":
            usage()
        elif opt in ("-c", "--config"):
            cfg_file = arg
        elif opt in ("-n", "--name"):
            name = arg
        elif opt in ("-p", "--profile"):
            profile = arg
        elif opt in ("-r", "--region"):
            region = arg
        elif opt == '--nolog':
            enable_log = False

    if cfg_file is None or name is None:
        usage(1)

    try:
        f = open(cfg_file, mode='r', encoding='utf-8')
        config = json.load(f)

        print("====AUTO-TAG CONFIG====")
        print("Config file: %s" % cfg_file)
        print("Lambda arn: %s" % name)
        print("Profile: %s" % profile)
        print("Region: %s" % region)
        print("-----------------------")
        print("%s" % json.dumps(config, indent=2))
        print("=======================")

        if profile is not None:
            session = boto3.Session(profile_name=profile)
            client = session.client("lambda") if region is None else session.client("lambda", region_name=region)
        else:
            client = boto3.client("lambda") if region is None else boto3.client("lambda", region_name=region)

        client.update_function_configuration(
            FunctionName=name,
            Environment={
                'Variables': {
                    'CONFIG': json.dumps(config),
                    'EnableLog': str(enable_log)
                }
            }
        )
    except OSError as e:
        print("Cannot open config file - %s, error - %s" % (cfg_file, e))
    except json.JSONDecodeError as e:
        print("Not a json format file - %s, error - %s" % (cfg_file, e))
    except Exception as e:
        print("Error to set Auto-Tag runtime options, error - %s" % e)


if __name__ == "__main__":
    set_config(sys.argv[1:])
