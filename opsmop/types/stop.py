
from opsmop.types.echo import Echo

class Stop(Echo):

     def default_provider(self, facts):
        from opsmop.providers.stop import Stop
        return Stop
