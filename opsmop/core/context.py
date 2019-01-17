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
import inspect

CHECK = 'check'
APPLY = 'apply'

class Context(metaclass=Singleton):

    __slots__ = [ '_host', '_host_failures', '_relative_root', 
    '_mode', '_caller', '_verbose', '_role', '_checksums', '_globals', '_extra_vars' ]

    def __init__(self):
        self._host = None
        self._host_failures = dict()
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
        assert mode in [ CHECK, APPLY ]
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

    def is_check(self):
        return self._mode == CHECK

    def is_apply(self):
        return self._mode == APPLY

    def scope_variables(self):
        
        from opsmop.types.type import Type
        from opsmop.providers.provider import Provider

        # all variables in current scope
        stack = inspect.stack()[1:]
        found_type_frame=False
        for item in stack:
            (frame, filename, lineno, function, code_context, index) = item
            localz = frame.f_locals
            if 'self' in localz:
                z = localz['self']
                if isinstance(z, Type):
                    found_type_frame=True
                elif not isinstance(z, Provider):
                    return localz
        return dict()


    
