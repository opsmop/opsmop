from opsmop.core.common import memoize
import random
import platform

# TODO: there are a LOT of facts to add yet!  We are just starting out
# in particular we also want to add /etc/opsmop/facts.d

class FactsGenerator(object):
    
    """
    As this evolves, facts can be dynamically injected into this base class based on platform, allowing a subclass
    for things like LinuxFacts. When this happens, we can have a "facts/" package.
    """

    @memoize
    def system(self):
        return platform.system()

    @memoize
    def release(self):
        return platform.release()

    @memoize
    def version(self):
        return platform.version()
  
    def default_package_manager(self):
        # TODO: this will return based on platform
        from opsmop.providers.package.brew import Brew
        return Brew

    def default_service_manager(self):
        # TODO: this will return based on platform
        from opsmop.providers.service.brew import Brew
        return Brew

    def choice(self, values):
        """
        Selects randomly from a set of values
        """
        return random.choice(values)

    def random(self):
        """
        Returns a random value between 0 and 1
        """
        return random.random()

    def constants(self):
        """
        This returns all facts that do not take parameters and is mostly for debug/demo
        purposes when someone wants to know the values of all the facts.
        See the 'opsmop-demo' repo in 'content/fact_demo.py' for an example.
        """
        # TODO: this should maybe be done introspectively?
        return dict(
            system = self.system(),
            release = self.release(),
            version = self.version(),
            default_package_manager = self.default_package_manager(),
            default_service_manager = self.default_service_manager(),
        )

Facts = FactsGenerator()


