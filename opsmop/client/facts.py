
from opsmop.core.common import memoize

import random
# import platform

MAC_OS = "MAC_OS"

# FIXME: not much implemented now as i want this to be really clean
# look at the 'distro' module on Linux for ideas but really cross-platform is better
# to not have conditional requirements.

class Facts(object):

    """
    Facts represent discovered information about the remote system, and are used in templating
    as well as evaluation of conditionals.
    """

    def __init__(self):
        pass

    @memoize
    def distro(self):
        return "FIXME"

    @memoize
    def os_type(self):
        return "MadeUpLinux"
  
    @memoize
    def default_package_manager(self):
        # FIXME: this will return based on platform
        from opsmop.providers.package.brew import Brew
        return Brew

    @memoize
    def default_service_manager(self):
        # FIXME: this will return based on platform
        from opsmop.providers.service.brew import Brew
        return Brew

    def choice(self, values):
        return random.choice(values)

    def random(self):
        return random.random()





                