# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.worker.worker
~~~~~~~~~~~~~~~~~~~
Tag worker of AutoTag

:license: MIT, see LICENSE for more details.
"""
from __future__ import annotations

import logging
import json
from worker.registrable import Registrable

logger = logging.getLogger(__name__)


class DictX(dict):
    def __init__(self, d=None, **kwargs):
        super(DictX, self).__init__()
        if d is None:
            d = {}
        if kwargs:
            d.update(**kwargs)
        for k, v in d.items():
            setattr(self, k, v)
        # Class attributes
        for k in self.__class__.__dict__.keys():
            if not (k.startswith('__') and k.endswith('__')) and k not in ('update', 'pop'):
                setattr(self, k, getattr(self, k))

    def __setattr__(self, name, value):
        if isinstance(value, (list, tuple)):
            value = [self.__class__(x)
                     if isinstance(x, dict) else x for x in value]
        elif isinstance(value, dict) and not isinstance(value, self.__class__):
            value = self.__class__(value)
        super(DictX, self).__setattr__(name, value)
        super(DictX, self).__setitem__(name, value)

    def __getattr__(self, item):
        try:
            return super(DictX, self).__getitem__(item)
        except KeyError:
            return None

    __setitem__ = __setattr__

    def update(self, e=None, **f):
        d = e or dict()
        d.update(f)
        for k in d:
            setattr(self, k, d[k])

    def pop(self, k, d=None):
        delattr(self, k)
        return super(DictX, self).pop(k, d)


class Worker(Registrable):
    def __init__(self, context: dict):
        self.context = DictX(context)

    def execute(self, tags: dict[str, str]) -> dict[str, str | list[str]]:
        raise NotImplemented

    @property
    def _client(self) -> any:
        raise NotImplemented

    @property
    def _account_id(self) -> str:
        account_id = self.context.recipientAccountId
        if account_id is None:
            account_id = self.context.userIdentity.accountId

        return account_id

    @property
    def _aws_region(self) -> str:
        return self.context.awsRegion

    @property
    def _aws_id(self) -> str:
        return 'aws-cn' if self.context.awsRegion.startswith('cn-') else 'aws'
