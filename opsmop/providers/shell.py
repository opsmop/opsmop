from opsmop.core.filetests import FileTests
from opsmop.providers.provider import Provider


class Shell(Provider):

    def plan(self):
        self.needs('execute')

    def verb(self):
        return "running..."

    def apply(self):

        if not self.should('execute'):
            return self.ok()

        self.do('execute')

        result = self.run(self.cmd, timeout=self.timeout, echo=True)
        return self.ok(data=result)
