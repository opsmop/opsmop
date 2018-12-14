# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import os

from opsmop.client.user_defaults import UserDefaults

LOG_FILENAME = os.path.expanduser("~/.opsmop.log")
LOGGER = None
INDENT = "  "

class BaseCallbacks(object):

    def __init__(self):
        global LOGGER
        if LOGGER is None:
            LOGGER = self.setup_logger()
        self.logger = LOGGER
        assert self.logger is not None

    def setup_logger(self):
        path = UserDefaults.log_path()
        dirname = os.path.dirname(path)
        if not os.path.exists(dirname):
            os.makedirs(dirname, 0o770)
        logger = logging.getLogger('opsmop')
        logger.setLevel(logging.DEBUG)
        handler = logging.handlers.RotatingFileHandler(path, maxBytes=1024*5000, backupCount=5)
        formatter = logging.Formatter(UserDefaults.log_format())
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def i1(self, msg):
        # indent methods
        self._indent(0, msg)

    def i2(self, msg):
        self._indent(1, msg)

    def i3(self, msg):
        self._indent(2, msg)

    def i4(self, msg):
        self._indent(3, msg)

    def i5(self, msg):
        self._indent(4, msg)
    
    def _indent(self, level, msg):
        spc = INDENT * level
        print("%s%s" % (spc, msg))
        self.logger.info(msg)
