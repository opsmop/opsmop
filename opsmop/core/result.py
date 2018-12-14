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

    __slots__ = [ 'rc', 'provider', 'resource', 'data', 'fatal', 'message', 'data', 'primary', 'reason', 'changed', 'actions' ]

    def __init__(self, provider, changed=None, message=None, rc=None, data=None, fatal=False, primary=True, reason=None, actions=None):

        """
        A result can be constructed with many parameters, most of which have reasonable defaults:

        provider - a reference to the provider object (required)
        resource - a reference to the resource the provider is executing (required)
        rc - the return code of any CLI command
        data - the output of a CLI command, or any structured data for use with 'register'
        fatal - a flag that indicates the result should probably end the program, but it is up to the callback code
        primary - indicates that the result is the final return of a module, as opposed to an intermediate command result
        reason - if set, the lookup used in evaluating the failure status of the result (for failed_when, etc). 
        changed - did any resources change?
        actions - what actions were run?
        """
        self.provider = provider
        self.resource = provider.resource
        self.rc = rc
        self.data = data
        self.fatal = fatal
        self.message = message
        self.primary = primary
        self.changed = changed
        self.actions = actions
        self.reason = None

    def is_ok(self):
        return not self.fatal

    def __str__(self):
        rc_msg = ""
        msg = ""
        if self.message is not None:
            msg = ", %s" % self.message
        if self.reason is not None:
            msg = ", reason: %s" % self.reason
        if self.rc is not None:
            rc_msg = ", rc=%s" % self.rc
        if self.is_ok():
            return "ok%s%s" % (rc_msg, msg)
        else:
            return "fatal%s%s" % (rc_msg, msg)

    def to_dict(self):
        reason = self.reason
        if self.reason is not None:
            reason = self.reason.to_dict()
        return dict(cls=self.__class__.__name__, rc=self.rc, data=self.data, actions=self.actions, changed=self.changed, fatal=self.fatal, message=self.message, reason=reason)
