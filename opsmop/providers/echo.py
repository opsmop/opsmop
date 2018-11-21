import os
import shutil

from opsmop.core.template import Template
from opsmop.providers.provider import Provider

COWSAY = "cowsay '{msg}'"

class Echo(Provider):

    def quiet(self):
        return True

    def verb(self):
        return "output..."

    def skip_plan_stage(self):
        return True

    def apply(self):
        
        self.cowsay = shutil.which('cowsay')
        txt = Template().from_string(self.msg, self.resource)

        if self.cowsay and os.environ.get('MOO'):
            cmd = COWSAY.format(msg=txt)
            txt = self.run(cmd, echo=False)
        self.echo(txt)

        return self.ok()
