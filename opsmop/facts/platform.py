import platform

from opsmop.core.common import memoize
from opsmop.facts.facts import Facts

# TODO: there are a LOT of facts to add yet!  We are just starting out
# contributions are very welcome

class PlatformFacts(Facts):
    
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

    def constants(self):
        """
        This returns all facts that do not take parameters .
        Mostly for the DebugFacts() implementation
        """
        return dict(
            system = self.system(),
            release = self.release(),
            version = self.version(),
            default_package_manager = self.default_package_manager(),
            default_service_manager = self.default_service_manager(),
        )

    def invalidate(self):
        pass

Platform = PlatformFacts()

if __name__ == "__main__":
    print(Platform.constants())
