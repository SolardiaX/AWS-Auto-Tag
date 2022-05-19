# -*- coding: utf-8 -*-

"""
AWS-Auto-Tag.main
~~~~~~~~~~~~~~~~~~~
local test methods

:license: MIT, see LICENSE for more details.
"""
import json
from config import load_config_from_file
from worker import *


if __name__ == "__main__":
    config = load_config_from_file('samples/config.json')

    print(json.dumps(config.to_dict()))
    print(Worker.list_available())
