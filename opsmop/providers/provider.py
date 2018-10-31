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

from opsmop.core.action import Action
from opsmop.core.command import Command
from opsmop.core.result import Result
from opsmop.core.template import Template

DEFAULT_TIMEOUT = 60

class Provider(object):

    def __init__(self, resource):
        """
        A provider object is obtained by calling the .provider() method of a resource object.
        While a Type defines the parameters and input validation for an object, a Type may have multiple Provider implementations
        that are returned contextually, whether based on environment or by the method= parameter on a Type
        """
        # FIXME: convert these to _vars and use properties. Executor code shouldn't access these directly.
        self.resource = resource
        self.actions_planned = []
        self.actions_taken = []
        self._context = None

        # isn't this already copied over - safe to remove?
        # self.name = getattr(self.resource, 'name', None)

    def verb(self):
        """ the verb for the applying operation in CLI output """
        return "applying..."

    def skip_plan_stage(self):
        """ for trivial providers like debug, tell the callbacks to not do plan computations """
        return False

    def quiet(self):
        """ if True, a resource claiming it is quiet will silence most properly programmed callbacks. """
        return False

    def has_changed(self):
        """ Returns whether the provider has undertaken any actions """
        return len(self.actions_taken) > 0

    def apply(self):
        """ makes resource configuration happen! use self.should() checks to determine what and mark them off with self.do().  Return a Result. """
        raise NotImplementedError

    def plan(self):
        """ call self.should('foo') for any actions that should be undertaken by .apply() """
        raise NotImplementedError

    def needs(self, action_name):
        """ declares than an action 'should' take place during an apply step """
        self.actions_planned.append(Action(action_name))

    def should(self, what):
        """ returns True if an action should take place during an apply step """
        return any(True for action in self.actions_planned if action.do == what)

    def do(self, what):
        """ marks off that an action has been completed. not marking off all planned actions (or any unplanned ones) will result in an error """
        self.actions_taken.append(Action(what))

    def get_command(self, cmd, input_text=None, timeout=None, echo=True, loud=False, fatal=True):
        """
        A convenience method that returns an un-executed command object from any provider, this should be used for executing ALL shell commands in OpsMop.
        """
        if self.ignore_errors:
            fatal = False
        if timeout is None:
            timeout = self.get_default_timeout()
        return Command(cmd, self, input_text=input_text, timeout=timeout, echo=echo, loud=loud, fatal=fatal)

    def _handle_cmd(self, cmd, input_text=None, timeout=None, echo=True, fatal=False, loud=False, loose=False, want_output=False):
        """ Common helper code for test and run """
        cmd = self.get_command(cmd, input_text=input_text, timeout=timeout, echo=echo, fatal=fatal, loud=loud)
        res = cmd.execute()
        if want_output:
            if res.rc == 0 or loose:
                return res.data.rstrip()
            else:
                return None
        return res

    def test(self, cmd, input_text=None, timeout=None, echo=True, loud=False, loose=False):
        """
        Run a command (cmd) with optional input and timeouts. 
        By default, the command will allow itself to be echoed by callbacks.
        Send "loud" to teach well-programmed methods to allow one command to squeak through even if provider.quiet() returns True.
        Loose will return the output even if the command fails.  If False, failed commands return None
        """
        return self._handle_cmd(cmd, input_text=input_text, timeout=timeout, echo=echo, loose=loose, loud=loud, want_output=True)

    def run(self, cmd, input_text=None, timeout=None, echo=True, loud=False):
        """
        Similar to test, this will call failed command callbacks when the commands fail, which MAY be intercepted
        by properly-programmed callbacks to fail the entire execution process.
        """
        return self._handle_cmd(cmd, input_text=input_text, timeout=timeout, echo=echo, fatal=True, loud=loud)

    def get_default_timeout(self): 
        """
        Each provider class may define a default command timeout for all commands to avoid specifying a timeout
        for each command.
        """
        return DEFAULT_TIMEOUT

    def ok(self, data=None):
        """ shortcut to return an ok result from .apply() """
        return Result(self, data=data)

    def fatal(self, msg):
        """ shortcut to return a failed result from .apply() """
        return Result(self, fatal=True, message=msg)

    def has_planned_actions(self):
        """
        Were any actions planned during plan stage?
        """
        return len(self.actions_planned)

    def handle_registration(self, context=None, result=None):
        va = dict()
        va[self.register] = result
        context.on_update_variables(va)
        self.resource.update_parent_variables(va)

    def commit_to_plan(self):
        """ used in executor code to move the list of planned actions in to the list that self.should() will check """
        self.actions = self.actions_planned

    def apply_simulated_actions(self):
        """ used in executor code (check mode only) to imply all commands were run when they were only simulated """
        self.actions_taken = self.actions_planned

    def echo(self, msg):
        self._context.on_echo(msg)

    def context(self):
        """
        Used by Executor class code to pass the Context to the resource.  Most normal types of providers should
        not need to access the context object in any way but it is useful because it contains methods that can be called
        to trigger a wide range of callbacks. Some more custom providers may use this to trigger callbacks, but a provider
        like Service should never need to access them directly, because the executor and Command classes (etc) will take
        care of triggering those callbacks. 
        """
        return self._context

    def set_context(self, value):
        self._context = value

    def template(self, msg):
        return Template.from_string(msg, self)

    def template_file(self, path):
        return Template.from_file(path, self)
