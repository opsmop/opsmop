from opsmop.providers.provider import Provider
import shutil
import os

class Stop(Provider):

    def quiet(self):
        # silence most callbacks
        return True

    def plan(self):
        self.needs('stop')

    def apply(self):
        
        self.do('stop')
        return self.fatal(self.msg)