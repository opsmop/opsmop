from opsmop.providers.provider import Provider
from opsmop.core.filetests import FileTests

class Shell(Provider):

    def plan(self, facts):
        self.needs('execute')

    def apply(self, facts):
        """
        Apply homebrew status changes.
        """

        if not self.should('execute'):
            return self.ok()

        self.do('execute')

        # use of the lower level get_command vs self.run() to return the full command result
        return self.get_command(cmd=self.cmd, timeout=self.timeout).execute()

        