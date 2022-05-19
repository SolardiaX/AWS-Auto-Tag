# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.listener
~~~~~~~~~~~~~~~~~~~
The lambda listener of AutoTag

:license: MIT, see LICENSE for more details.
"""

import logging
import json
import os

from config import load_config
from evals import eval_exp, eval_condition
from worker import *

if os.getenv("EnableLog", "True").lower() == "true":
    logging.getLogger().setLevel(logging.INFO)

logger = logging.getLogger(__name__)


def lambda_handler(evt, _):
    logger.info('Event received: %s' % json.dumps(evt))

    evt_dict = DictX(evt)
    detail = evt.get('detail', dict())
    event_name = detail.get('eventName', None)  # get the event name
    config = load_config()

    for t in config.triggers:
        if event_name in t.events:
            logger.info('Trigger matched: %s-%s' % (t.service, event_name))

            if not Worker.is_registered(t.service):
                logger.info('Trigger worker not register: %s', t.service)
                continue

            logger.info('Tagging with worker: %s' % t.service)

            tags: dict[str, str] = {}
            for tag in config.tags:
                if len(tag.condition) > 0 and not eval_condition(tag.condition, evt_dict):
                    continue

                if len(tag.services) > 0 and t.service not in tag.services:
                    continue

                key = eval_exp(tag.key, evt_dict)
                val = eval_exp(tag.value, evt_dict)
                logger.info('Tagging with: Key = %s, Value = %s' % (key, val))
                tags[key] = val

            worker = Worker.by_name(t.service)(detail)
            targets = worker.execute(tags)

            if len(targets) == 0:
                logger.warning('Execute canceled: no target(s) to tag')
                return

            logger.info('Execute finished: target - %s, tags - %s' % (json.dumps(targets), json.dumps(tags)))
            return

    logger.info('Execute exited: no matched/actived trigger')
