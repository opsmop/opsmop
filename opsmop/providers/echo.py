from opsmop.providers.provider import Provider
import shutil
import os

COWSAY = "cowsay '{msg}'"

class Echo(Provider):

    def quiet(self):
        # silence most callbacks
        return True

    def plan(self, facts):
        self.needs('echo')

    def apply(self, facts):
        
        self.do('echo')

        self.cowsay = shutil.which('cowsay')
        if self.cowsay and os.environ.get('MOO'):
            cmd = COWSAY.format(msg=self.msg)
            txt = self.run(cmd, echo=False, loud=True)
            self.callbacks.on_echo(self, self.resource, txt)
        else:
            self.callbacks.on_echo(self, self.resource, self.msg)
        return self.ok()