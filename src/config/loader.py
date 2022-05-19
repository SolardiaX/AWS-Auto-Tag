# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.config.loader
~~~~~~~~~~~~~~~~~~~
Configuration loader of AutoTag

:license: MIT, see LICENSE for more details.
"""
import boto3
import logging
import json
import os

from config.types import Config, Tag, Trigger
from config.supported import SupportedTriggers

config_file_name = "config.json"

logger = logging.getLogger(__name__)


def load_config() -> Config:
    """ Load configuration from lambda env """

    # noinspection PyBroadException
    try:
        body = os.environ.get('CONFIG', "{}")
        content = json.loads(body)

        cfg = Config()
        cfg.triggers = _config_targets(content)
        cfg.tags = _config_tags(content)

        return cfg
    except Exception as e:
        logger.error("Unable to load configure file from env - 'CONFIG', error - %s" % e)


def load_config_from_s3() -> Config:
    """ Load configuration from s3 """
    s3 = boto3.resource("s3")
    config_file = s3.Object(os.environ['CONFIG_BUCKET_NAME'], config_file_name)

    # noinspection PyBroadException
    try:
        body = config_file.get()['Body'].read().decode('utf-8')
        content = json.loads(body)

        cfg = Config()
        cfg.triggers = _config_targets(content)
        cfg.tags = _config_tags(content)

        return cfg
    except Exception as e:
        logger.error("Unable to load configure file from %s/%s - %s"
                     % (os.environ['CONFIG_BUCKET_NAME'], config_file_name, e))


def load_config_from_file(src: str) -> Config:
    """ Local test method to load config from src file """
    f = open(src)
    dat = json.load(f)

    cfg = Config()
    cfg.triggers = _config_targets(dat)
    cfg.tags = _config_tags(dat)

    return cfg


def _config_tags(content: dict) -> list[Tag]:
    cfg_tags = content.get('tags', [])
    tags: list[Tag] = _load_tags_from_json(cfg_tags)
    return tags


def _config_targets(content: dict) -> list[Trigger]:
    trigger = content.get('trigger', None)
    if trigger is None:
        return SupportedTriggers

    triggers: list[Trigger] = []
    cfg_services: list[Trigger] = _load_events_from_json(trigger.get('services', []))
    excluded = trigger.get('excluded', False)

    if not excluded and len(cfg_services) == 0:
        return SupportedTriggers

    if excluded:
        triggers = SupportedTriggers

    for service in cfg_services:
        def_trigger = next(t for t in SupportedTriggers if t.service == service.service)

        if excluded:
            if service.events == ['*']:
                triggers = [t for t in triggers if t.service != service.service]
                continue
            else:
                def_trigger.events = [t for t in def_trigger.events if t not in service.events]
                triggers.append(def_trigger)
        else:
            if service.events == ['*']:
                triggers.append(def_trigger)
            else:
                def_trigger.events = [t for t in def_trigger.events if t in service.events]
                triggers.append(def_trigger)

    return triggers


def _load_events_from_json(data: dict) -> list[Trigger]:
    return [Trigger(list(item.keys())[0], list(item.values())[0]) for item in data]


def _load_tags_from_json(data: list[dict]) -> list[Tag]:
    return [
        Tag(
            item.get('key', ''),
            item.get('value', ''),
            item.get('services', []),
            item.get('condition', ''),
        )
        for item in data
    ]
