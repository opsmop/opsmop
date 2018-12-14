# Copyright 2018 Michael DeHaan LLC, <michael@michaeldehaan.net>
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from opsmop.callbacks.callback import BaseCallbacks
from opsmop.core.context import Context

class ReplayCallbacks(BaseCallbacks):
   
    def on_resource(self, host, evt):
        # {'evt': 'resource', 'resource': {'cls': 'Debug', 'variable_names': (), 'evals': {}}, 'is_handler': False}
        self.info(host, self.resource(evt))

    def on_execute_command(self, host, evt):
        if not Context.verbose():
            return
        self.info(host, self.command(evt))

    def on_complete(self, host, evt):
        self.info(host, 'complete')

    def on_result(self, host, evt):
        self.info(host, self.result(evt), sep='=')

    def on_default(self, host, evt):
        #print(f"** DEBUG: {host.name} : {evt}")
        pass

    def on_fatal(self, host, evt):
        self.info(host, "failed")

    def on_command_echo(self, host, evt):
        if not Context.verbose():
            return
        self.info(host, "| %s" % evt['data'])

    def on_echo(self, host, evt):
        if not Context.verbose():
            return
        self.info(host, "| %s" % evt['data'])

    def on_signaled(self, host, evt):
        self.info(host, self.signaled(evt))

    # ----

    def resource(self, evt):
        caption = evt['resource']['cls']
        name = evt['resource'].get('name', None)
        if name:
            caption = caption + " (%s)" % name
        if evt['is_handler']:
            return "handler: %s" % caption
        else:
            return "resource: %s" % caption

    def command(self, evt):
        cmd = evt['data']['cmd']
        return "executing: %s" % str(cmd)

    def result(self, evt):
        caption = "ok"
        data = evt['data']
        fatal = data['fatal']
        message = data['message']
        rc = data['rc']
        if fatal:
            caption = "fatal"
        else:
            caption = "ok"
        if rc is not None:
            caption = caption + ", rc=%s" % rc
        if message is not None:
            caption = caption + ", %s" % message
        return "%s" % caption

    def signaled(self, evt):
        return "signaled: %s" % evt['data']

    def info(self, host, msg, sep=':'):
        hostname = host.hostname()
        caption = host.name
        if host.name != hostname:
            caption = "%s (%s)" % (host.name, hostname)
        self.i3("%s %s %s" % (caption, sep, msg))


    
