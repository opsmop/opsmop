from opsmop.core.common import memoize
import random

# GLOBAL VARIABLES FOR EVERYTHING
_variables = dict()

# CONSTANTS: FIXME: move into core/constants.py
MAC_OS = "MAC_OS"

class FactsBase(object):

    """
    Facts represent discovered information about the remote system, and are used in templating
    as well as evaluation of conditionals.  The Facts also hold onto the global variable
    dictionary, which changes as the Executor walks through the resource tree.
    """

    def __init__(self):
        pass

    @classmethod
    def set_variables(cls, variables):
        global _variables
        _variables = variables

    @classmethod
    def variables(cls):
        global _variables
        return _variables

    @classmethod
    def update_variables(cls, variables):
        global _variables
        assert type(variables) == dict
        _variables.update(variables)

class Facts(FactsBase):

    """
    As this evolves, facts can be dynamically injected into this base class based on platform, allowing a subclass
    for things like LinuxFacts. When this happens, we can have a "facts/" package.
    """

    # FIXME: implement lots of stuff, just a placeholder for now

    @memoize
    def distro(self):
        return "FIXME"

    @memoize
    def os_type(self):
        return "MadeUpLinux"
  
    def default_package_manager(self):
        # FIXME: this will return based on platform
        from opsmop.providers.package.brew import Brew
        return Brew

    def default_service_manager(self):
        # FIXME: this will return based on platform
        from opsmop.providers.service.brew import Brew
        return Brew

    def choice(self, values):
        return random.choice(values)

    def random(self):
        return random.random()
