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

from opsmop.core.errors import InventoryError
from opsmop.core.context import Context
from opsmop.callbacks.callbacks import Callbacks
from opsmop.callbacks.event_stream import EventStreamCallbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.core.roles import Roles
from opsmop.callbacks.replay import ReplayCallbacks
from opsmop.callbacks.local import LocalCliCallbacks

import mitogen.core
import mitogen.master
import mitogen.select
import mitogen.utils
import mitogen.service

import time
import os

class ConnectionManager(object):

    def __init__(self):
        """
        Constructor.  Establishes mitogen router/broker.
        """
        self.broker = mitogen.master.Broker()
        self.router = mitogen.master.Router(self.broker)
        self.events_select = mitogen.select.Select(oneshot=False)
        self.replay_callbacks = ReplayCallbacks()

        self.calls_sel = mitogen.select.Select()
        self.status_recv = mitogen.core.Receiver(self.router)
        self.hosts_by_context = dict()

        # self.calls_select = mitogen.select.Select(oneshot=False)
        self.connections = dict()
        self.hosts = dict()
        self.context = dict()

    def add_hosts(self, new_hosts):
        """
        Extends the list of hosts that *MAY* be connected to with more hosts
        """
        if type(new_hosts) == list:
            new_hosts = { host.name: host for host in new_hosts }
        self.hosts.update(new_hosts)

    def get_connection_for_host(self, host, role):
        """
        Get a SSH connection (possibly with sudo or intermediate hosts) depending on parameters.
        """

        if host.name in self.connections:
            return self.connections[host.name]
        else:
            variables = host.all_variables()
            via = variables.get('opsmop_via', None)
            if via:
                via = self.hosts.get('via', None)
                if via is None:
                    raise InventoryError("host specified by 'opsmop_via' not defined in inventory")
                parent = self.get_connection_for_host(via, host, role)
                return self._form_connection(parent, role)

            return self._form_connection(host, role)


    def _form_connection(self, host, role, parent=None):

        # as currently implemented, if a host is featured in multiple roles, the connection
        # will be reused for the second role, so it is expected that the user connects with
        # a user that has full sudo privs.

        context = host.connection_context(role)
        remote = self.router.ssh(
            python_path=host.python_path(), 
            hostname=context['hostname'], 
            check_host_keys=context['check_host_keys'], 
            username=context['username'], 
            password=context['password'],
            via=parent
        )
        self.hosts_by_context[remote.context_id] = host
        self.connections[host.name] = remote
        self.context[host.name] = context
        return remote


    def connect(self, host, role):

        conn = self.get_connection_for_host(host, role)
        context = self.context[host.name]

        result = conn
        if role.sudo():
            result = router.sudo(
                username=context['sudo_username'], 
                password=context['sudo_password'], 
                via=conn
            )
            self.hosts_by_context[result.context_id] = host
        return result

    def register_files(self, file_service):
        cwd = os.getcwd()
        for root, dirs, files in os.walk(cwd):
            for f in files:
                print("Registering file: %s" % f)
                path = os.path.join(root, f)
                file_service.register(path)

    def process_remote_role(self, host, policy, role, mode):

        import dill
        conn = self.connect(host, role)
        receiver = mitogen.core.Receiver(self.router)
        self.events_select.add(receiver)
        sender = self.status_recv.to_sender()


        file_service = mitogen.service.FileService(conn.router)

        # Start the pool.
        pool = mitogen.service.Pool(conn.router, services=[file_service])

        self.register_files(file_service)

        myself = mitogen.core.Context(conn.router, mitogen.context_id)

        call_recv = conn.call_async(remote_fn, myself, dill.dumps(host), dill.dumps(policy), dill.dumps(role), mode, sender)
        self.calls_sel.add(call_recv)

        # stop the fileserver or this will hang
        pool.stop(join=True)

        return True

    def event_loop(self):
    
        both_sel = mitogen.select.Select([self.status_recv, self.calls_sel], oneshot=False)

        while self.calls_sel:
            try:
                msg = both_sel.get(timeout=60.0)
            except mitogen.core.TimeoutError:
                print("No update in 60 seconds, something's broke?")
                raise Exception("boom")

            host = self.hosts_by_context[msg.src_id]

            if msg.receiver is self.status_recv:   
                # https://mitogen.readthedocs.io/en/stable/api.html#mitogen.core.Message.receiver
                # handle a status update
                
                response = msg.unpickle()
                event = response['evt']
                cb_func = getattr(self.replay_callbacks, "on_%s" % event, None)
                if cb_func:
                    cb_func(host, response)
                else:
                    self.replay_callbacks.on_default(host, response)

            elif msg.receiver is self.calls_sel:  
                # handle a function call result.
                try:
                    msg.unpickle()
                    # all done for host
                except mitogen.core.CallError as e:
                    print('Task failed on host %s: %s' % (host.name, e))


def remote_fn(caller, host, policy, role, mode, sender):
    """
    This is the remote function used for mitogen calls
    """
    
    import dill
    from opsmop.core.executor import Executor

    host = dill.loads(host)
    policy = dill.loads(policy)
    role = dill.loads(role)
    Context.set_mode(mode)
    Context.set_caller(caller)
    policy.items = Roles(role)
    Callbacks.set_callbacks([ EventStreamCallbacks(sender=sender), LocalCliCallbacks(), CommonCallbacks() ])
    executor = Executor([ policy ], local_host=host, push=False) # remove single_role
    # FIXME: care about mode
    executor.apply()

