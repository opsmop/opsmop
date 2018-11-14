
from opsmop.core.context import Context
from opsmop.core.executor import Executor

import os
from runpy import run_path

class Api(object):

    """
    The API object is constructed with a list of one-or-more policies and a list of
    one-or-more callback objects.
    """

    __slots__ = [ '_policies', '_callbacks' ]

    def __init__(self, policies=None, callbacks=None):

        assert type(callbacks) == list
        assert type(policies) == list
        self._policies = policies
        self._callbacks = callbacks

    @classmethod
    def from_file(cls, callbacks=None, path=None):
        """
        Given a filename, run an API instance that will use the policies from file, as listed in the EXPORTED variable
        in that file.  Requires a list of callbacks.
        """

        assert type(callbacks) == list
        assert path is not None

        path = os.path.expandvars(os.path.expanduser(path))

        if not os.path.exists(path):
            raise Exception("file does not exist: %s" % path)
            sys.exit(1)

        ran = run_path(path)
        dirname = os.path.dirname(path)
        os.chdir(dirname)

        if 'EXPORTED' not in ran:
            raise Exception("unable to find EXPORTED=[] in %s" % path)
        policies = [ x for x in ran['EXPORTED'] ]

        return cls(policies=policies, callbacks=callbacks)
        
    def validate(self):
        """
        This just checks for invalid types in the python file as well as missing files
        and non-sensical option combinations.
        """
        executor = Executor(policies=self._policies, callbacks=self._callbacks)
        contexts = executor.validate()
        return contexts

    def check(self):
        """
        This is dry-run mode
        """
        executor = Executor(policies=self._policies, callbacks=self._callbacks)
        contexts = executor.check()
        return contexts

    def apply(self):
        """
        This is live-configuration mode.
        """
        executor = Executor(policies=self._policies, callbacks=self._callbacks)
        contexts = executor.apply()
        return contexts

    

