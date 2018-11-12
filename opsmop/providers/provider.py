# opsmop/providers/__init__.py

import traceback

from opsmop.core.action import Action
from opsmop.core.command import Command
from opsmop.core.errors import ProviderError
from opsmop.core.result import Result

DEFAULT_TIMEOUT = 60

class Provider(object):

    def __init__(self, resource, facts):
        self.resource = resource
        self.facts = facts
        self.actions_planned = []
        self.callbacks = None 
        self.actions_taken = []

        # FIXME: CODE IMPROVEMENT: to avoid doing self.resource and so on in the provider code, consider code that copies each field over
        # to the resource and calling it here.
        self.name = getattr(self.resource, 'name', None)

    def quiet(self):
        # if True, silences most (executor) callbacks
        return False

    def has_changed(self):
        return len(self.actions_taken) > 0

    def set_callbacks(self, callbacks):
        self.callbacks = callbacks
            
    def apply(self, facts):
        """
        make things happen, use self.should() checks to determine what
        and mark them off.
        """
        raise NotImplementedError

    def plan(self):
        raise NotImplementedError

    def needs(self, action_name):
        self.actions_planned.append(Action(action_name))

    def should(self, what):
        for action in self.actions_planned:
            if action.do == what:
                return True
        return False

    def do(self, what):
        self.actions_taken.append(Action(what))
        return True


    def get_command(self, cmd, input_text=None, timeout=None, echo=True, loud=False, fatal=True):
        if self.ignore_errors:
            fatal = False
        if timeout is None:
            timeout = self.get_default_timeout()
        return Command(cmd, provider=self, input_text=input_text, timeout=timeout, echo=echo, loud=loud, fatal=fatal)

    def _handle_cmd(self, cmd, input_text=None, timeout=None, echo=True, fatal=False, loud=False, loose=False):
        cmd = self.get_command(cmd, input_text=input_text, timeout=timeout, echo=echo, fatal=fatal, loud=loud)
        res = cmd.execute()
        if res.rc == 0 or loose:
            return res.data.rstrip()
        else:
            return None

    def test(self, cmd, input_text=None, timeout=None, echo=True, loud=False, loose=False):
        return self._handle_cmd(cmd, input_text=input_text, timeout=timeout, echo=echo, loose=loose, loud=loud)

    def run(self, cmd, input_text=None, timeout=None, echo=True, loud=False):
        return self._handle_cmd(cmd, input_text=input_text, timeout=timeout, echo=echo, fatal=True, loud=loud)

    # FIXME: remove
    #def error(self, message=None):
    #    # use of 'error' is discouraged, it is better to return a Result(fatal=True) to give the callbacks
    #    # an opportunity to decide what to do with it, as well as to allow ignore_errors=True to work.
    #    # use this only for errors that must end in a traceback.
    #    raise ProviderError(self, message)

    def get_default_timeout(self): 
        return DEFAULT_TIMEOUT

    def ok(self):
        return Result(provider=self)

    def fatal(self, msg):
        return Result(provider=self, fatal=True, message=msg)