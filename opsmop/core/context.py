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

from opsmop.core.common import Singleton

VALIDATE = 'validate'
CHECK = 'check'
APPLY = 'apply'

class Context(metaclass=Singleton):

    __slots__ = [ '_host', '_host_failures', '_host_signals', '_relative_root', '_mode', '_caller', '_verbose', '_role', '_checksums', '_globals', '_extra_vars' ]

    def __init__(self):
        self._host = None
        self._host_failures = dict()
        self._host_signals = dict()
        self._mode = None
        self._caller = None
        self._verbose = False
        self._role = None
        self._checksums = dict()
        self._extra_vars = dict()
        self._globals = dict()

    def update_globals(self, variables):
        self._globals.update(variables)

    def globals(self):
        return self._globals

    def set_mode(self, mode):
        assert mode in [ VALIDATE, CHECK, APPLY ]
        self._mode = mode

    def mode(self):
        return self._mode

    def set_caller(self, caller):
        self._caller = caller

    def set_extra_vars(self, extra_vars):
        self._extra_vars = extra_vars

    def extra_vars(self):
        return self._extra_vars

    def caller(self):
        return self._caller

    def role(self):
        return self._role

    def set_role(self, role):
        self._role = role 

    def verbose(self):
        return self._verbose

    def set_verbose(self, value):
        self._verbose = value

    def set_host(self, host):
        self._host = host

    def relative_root(self):
        return self._relative_root

    def set_relative_root(self, root):
        self._relative_root = root

    def host(self):
        return self._host

    def get_checksum(self, path):
        return self._checksums[path]

    def set_checksums(self, checksums):
        self._checksums = checksums


    def record_host_failure(self, host, exc):
        self._host_failures[host] = exc

    def host_failures(self):
        return self._host_failures

    def is_validate(self):
        return self._mode == VALIDATE

    def is_check(self):
        return self._mode == CHECK

    def is_apply(self):
        return self._mode == APPLY

    def add_signal(self, host, signal):

        if not host.name in self._host_signals:
            self._host_signals[host.name] = []
        self._host_signals[host.name].append(signal)

    def has_seen_any_signal(self, host, signals):

        host_signals = self._host_signals.get(host.name, [])

        for x in host_signals:
            if x in signals:
                return True
        return False
