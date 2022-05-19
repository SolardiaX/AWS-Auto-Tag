# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.evals
~~~~~~~~~~~~~~~~~~~
description of evals

:license: MIT, see LICENSE for more details.
"""
import time
import math
import datetime
import logging


# add any needed builtins back in
_safe_list = dict()
_safe_list['abs'] = abs
_safe_list['int'] = int
_safe_list['str'] = str
_safe_list['float'] = float
_safe_list['datetime'] = datetime
_safe_list['time'] = time
_safe_list['math'] = math

logger = logging.getLogger(__name__)


# noinspection PyBroadException
def eval_exp(exp: str, event: any) -> str:
    data = {'event': event, **_safe_list}
    try:
        return eval(exp, {'__buildin__': None}, data)
    except NameError:
        return exp
    except Exception as e:
        logger.error('Fail to eval exp [%s] - %s' % (exp, e))
        return exp


# noinspection PyBroadException
def eval_condition(exp: str, event: any) -> bool:
    data = {'event': event, **_safe_list}
    try:
        return eval(exp, {'__buildin__': None}, data)
    except Exception as e:
        logger.error('Fail to eval condition [%s] - %s' % (exp, e))
        return False
