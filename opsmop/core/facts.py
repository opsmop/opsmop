from opsmop.core.common import memoize
import random

# CONSTANTS: FIXME: move into core/constants.py
MAC_OS = "MAC_OS"

class FactsGenerator(object):

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
        # TODO: this will return based on platform
        from opsmop.providers.package.brew import Brew
        return Brew

    def default_service_manager(self):
        # TODO: this will return based on platform
        from opsmop.providers.service.brew import Brew
        return Brew

    def choice(self, values):
        return random.choice(values)

    def random(self):
        return random.random()

Facts = FactsGenerator()


