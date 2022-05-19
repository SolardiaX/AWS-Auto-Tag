# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.config.types
~~~~~~~~~~~~~~~~~~~
The configuration defines of AutoTag

:license: MIT, see LICENSE for more details.
"""


class Trigger:
    service: str = ""
    """ The source service will fire event """
    events: list[str] = []
    """ The fired event name """

    def __init__(self, service: str, events: list[str]):
        self.service = service
        self.events = events

    def dict(self) -> dict:
        return self.__dict__


class Tag:
    """ Tag define of AutoTag """
    key: str = ""
    """ The key of tag """
    value: str = ""
    """ The value of tag """
    services: list[str] = []
    """ The target services of tag """
    condition: str = ""
    """ The condition to use tag """

    def __init__(self, key: str, value: str, services: list[str], cond: str):
        self.key = key
        self.value = value
        self.services = services
        self.condition = cond

    def dict(self) -> dict:
        return self.__dict__


class Config:
    """ Configuration of AutoTag """
    triggers: list[Trigger] = []
    """ The AWS Services enabled for AutoTag """
    tags: list[Tag] = []
    """ The Tags for AutoTag """

    def to_dict(self) -> dict:
        return {
            'triggers': [trigger.dict() for trigger in self.triggers],
            'tags': [tag.dict() for tag in self.tags]
        }
