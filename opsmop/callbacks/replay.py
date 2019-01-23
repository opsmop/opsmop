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

from colorama import Back, Fore, Style

from opsmop.callbacks.callback import BaseCallbacks
from opsmop.core.context import Context


class ReplayCallbacks(BaseCallbacks):

    def __init__(self):
        super().__init__()

    def on_resource(self, host, evt):
        # {'evt': 'resource', 'resource': {'cls': 'Debug', 'variable_names': (), 'evals': {}}, 'is_handler': False}
        self.info(host, self.resource(evt), sep='>')

    def on_execute_command(self, host, evt):
        if not Context().verbose():
            return
        self.info(host, self.command(evt), sep='!')

    def on_failed_host(self, host, exc):
        self.info(host, str(exc), foreground=Fore.RED)

    def on_complete(self, host, evt):
        try:
            Context().role().after_contact(host)
        except Exception as e:
            print(str(e))
            Context().record_host_failure(host, e)
        self.info(host, 'COMPLETE', sep='=', foreground=Fore.GREEN)

    def on_result(self, host, evt):
        fatal = evt['data']['fatal']
        changed = evt['data']['changed']
        actions = evt['data']['actions']
        host.record_actions(actions)
        fore = None
        if fatal:
            fore = Fore.RED
        elif changed:
            fore = Fore.YELLOW
        else:
            fore = Fore.GREEN
        self.info(host, self.result(evt), sep='=', foreground=fore)

#Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
#Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.

    def on_default(self, host, evt):
        pass

    def on_fatal(self, host, evt):
        self.info(host, "failed", foreground=Fore.RED)

    def on_command_echo(self, host, evt):
        if not Context().verbose():
            return
        self.info(host, evt['data'].strip(), sep='|')

    def on_echo(self, host, evt):
        if not Context().verbose():
            return
        self.info(host, evt['data'], sep='|')

    # ----

    def resource(self, evt):
        caption = evt['resource']['cls']
        name = evt['resource'].get('name', None)
        if name:
            caption = caption + " (%s)" % name
        if evt.get('is_handler',False):
            return "%s (handler)" % caption
        else:
            return "%s" % caption

    def command(self, evt):
        cmd = evt['data']['cmd']
        return "executing: %s" % str(cmd).strip()

    def result(self, evt):
        caption = "ok"
        data = evt['data']
        fatal = data['fatal']
        message = data['message']
        changed = data['changed']
        actions = len(data['actions'])
        rc = data['rc']
        if fatal:
            caption = "failed"
        elif changed:
            caption = "modified (%s actions)" % actions
        else:
            caption = "ok"
        if rc is not None:
            caption = caption + ", rc=%s" % rc
        if message is not None:
            caption = caption + ", %s" % message
        return "%s" % caption

    def signaled(self, evt):
        return "%s (signaled)" % evt['data']

    def info(self, host, msg, sep=':', foreground=None):

        from opsmop.callbacks.callbacks import Callbacks
        max_length = Callbacks().hostname_length()
        fmt = f"%-{max_length}s"
        msg = "%s %s %s" % (fmt % host.display_name(), sep, msg)
        if foreground:
            msg = foreground + msg + Style.RESET_ALL
        self.i3(msg)

    def nice_changes_list(self, actions):
        results = dict()
        for a in actions:
            if not a in results:
                results[a] = 1
            else:
                results[a] = results[a] + 1
        names = results.keys()
        new_results = []
        for n in names:
            if results[n] == 1:
                new_results.append(n)
            else:
                new_results.append("%s (%s)" % n, results[n])
        return ",".join(new_results)

    def on_host_changed_list(self, hosts):

        print("\nChanged Hosts:\n")
        changed = False
        for host in hosts:
            changed = True
            actions = host.actions()
            if actions:
                nice_list = self.nice_changes_list(actions)
                self.info(host, nice_list)
        if not changed:
            print(Fore.GREEN + "    (None)" + Style.RESET_ALL)

    def on_terminate_with_host_list(self, failed_hosts):
        
        # TODO: can we show why?

        if len(failed_hosts) == 1 and failed_hosts[0].name == "127.0.0.1":
            return

        print("")
        print(Fore.RED + "\nPOLICY FAILED. The following hosts had failures:\n")
        for host in failed_hosts:
            self.info(host, '', sep='')
        print(Style.RESET_ALL)
