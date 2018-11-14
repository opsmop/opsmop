# This is OpsMop
# (C) Michael DeHaan LLC <michael@michaeldehaan.net>, 2018.
# License: GPLv3

from opsmop.core.easy import *

# bin/opsmop check filename.py
# bin/opsmop apply filename.py

class WebServers(Role):

    def set_variables(self):
        return dict(dog='fido', code=1234)

    def set_resources(self):
        return Resources(
            File(name="/tmp/foo.txt", from_content="Hello World!", signals="restart_foo"),
            Package(name="cowsay", method="brew", signals="restart_nginx"),
            Echo("resources complete!")
        )

    def set_handlers(self):
        return Handlers(
            restart_nginx = Service(name='nginx', restarted=True),
            restart_foo   = Service(name='foo', restarted=True),
        )

class Demo(Policy):

    def set_variables(self):
        return dict(asdf = 'jkl;')

    def set_roles(self):
        roles = [ WebServers(name='webservers'), ]
        return Roles(*roles)
   
EXPORTED = [
    Demo(),
]

