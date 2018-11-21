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

class Result(object):

    """
    Result represents the return result from a command execution *OR* a application of a provider,
    in which case there should be an array of results (FIXME?)   
    """

    __slots__ = [ 'rc', 'provider', 'resource', 'data', 'fatal', 'message', 'data' ]

    def __init__(self, provider, changed=True, message=None, rc=None, data=None, fatal=False):

        """
        A result can be constructed with many parameters, most of which have reasonable defaults:

        provider - a reference to the provider object (required)
        resource - a reference to the resource the provider is executing (required)
        rc - the return code of any CLI command
        data - the output of a CLI command, or any structured data for use with 'register'
        fatal - a flag that indicates the result should probably end the program, but it is up to the callback code
        """
        self.provider = provider
        self.resource = provider.resource
        self.rc = rc
        self.data = data
        self.fatal = fatal
        self.message = message

    def is_ok(self):
        return not self.fatal

    def __str__(self):
        rc_msg = ""
        msg = ""
        if self.message is not None:
            msg = ", %s" % self.message
        if self.rc is not None:
            rc_msg = ", rc=%s" % self.rc
        if self.is_ok():
            return "ok%s%s" % (rc_msg, msg)
        else:
            return "fatal%s%s" % (rc_msg, msg)
