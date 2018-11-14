from opsmop.providers.provider import Provider
from opsmop.core.filetests import FileTests

class Shell(Provider):

    def plan(self):
        self.needs('execute')

    def apply(self):

        if not self.should('execute'):
            return self.ok()

        self.do('execute')

        result = self.run(self.cmd, timeout=self.timeout, echo=True)
        return self.ok(data=result)
        