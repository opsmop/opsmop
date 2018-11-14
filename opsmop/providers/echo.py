from opsmop.providers.provider import Provider
import shutil
import os

COWSAY = "cowsay '{msg}'"

class Echo(Provider):

    def quiet(self):
        # silence most callbacks
        return True

    def plan(self):
        self.needs('echo')

    def verb(self):
        return "output..."

    def skip_plan_stage(self):
        return True

    def apply(self):
        
        self.do('echo')
        self.cowsay = shutil.which('cowsay')
        txt = None
        if self.cowsay and os.environ.get('MOO'):
            cmd = COWSAY.format(msg=self.msg)
            txt = self.run(cmd, echo=False)
        else:
            txt = self.msg
        self.echo(txt)
        return self.ok()