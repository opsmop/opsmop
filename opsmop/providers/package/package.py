# opsmop/providers/package/__init__.py

from opsmop.providers.provider import Provider

class Package(Provider):

    def _get_version(self):
        raise NotImplementedError()

    def plan(self):

        current_version = self._get_version()

        # FIXME: this can probably should advantage of the StrictVersion class to be smarter.
        if not current_version and self.absent:
            self.needs('uninstall')
        elif self.latest:
            self.needs('latest')
        elif self.version and self.version != version:
            self.needs('upgrade')

        
