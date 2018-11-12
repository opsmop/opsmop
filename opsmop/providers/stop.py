from opsmop.providers.echo import Echo
from opsmop.core.result import Result

COWSAY = "cowsay '{msg}'"

class Stop(Echo):

    def apply(self, facts):
        super().apply(facts)
        return self.fatal(msg="user requested exit")
        