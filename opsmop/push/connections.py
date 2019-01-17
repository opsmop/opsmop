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

import fnmatch
import os
import sys
import time
import logging
import zlib

import mitogen.core
import mitogen.master
import mitogen.select
import mitogen.service
import mitogen.utils

from opsmop.callbacks.callbacks import Callbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.callbacks.event_stream import EventStreamCallbacks
from opsmop.callbacks.local import LocalCliCallbacks
from opsmop.callbacks.replay import ReplayCallbacks
from opsmop.core.context import Context
from opsmop.core.errors import InventoryError
from opsmop.core.roles import Roles
from opsmop.inventory.host import Host
from opsmop.facts.filetests import FileTestFacts


class ConnectionManager(object):

    def __init__(self, policy, tags, limit_groups=None, limit_hosts=None):
        """
        Constructor.  Establishes mitogen router/broker.
        """
        
        logging.getLogger('mitogen').setLevel(logging.ERROR)

        self.policy = policy
        self.broker = mitogen.master.Broker()
        self.router = mitogen.master.Router(self.broker)
        self.hosts_by_context = dict()
        self.connections = dict()
        self.hosts = dict()
        self.context = dict()
        self.tags = tags
        self.allow_patterns = policy.allow_fileserving_patterns()
        self.deny_patterns  = policy.deny_fileserving_patterns()
        self.checksums = dict()
        self._limit_groups = limit_groups
        self._limit_hosts = limit_hosts

    def prepare_for_role(self, role):

        self.file_service = mitogen.service.FileService(self.router)
        self.pool = mitogen.service.Pool(self.router, services=[self.file_service])
        self.events_select = mitogen.select.Select(oneshot=False)
        self.replay_callbacks = ReplayCallbacks()
        self.calls_sel = mitogen.select.Select()
        self.status_recv = mitogen.core.Receiver(self.router)
        self.myself = self.router.myself()

        fileserving_paths = role.allow_fileserving_paths()
        if fileserving_paths is None:
            fileserving_paths = self.policy.allow_fileserving_paths()
        for p in fileserving_paths:
            if p == '.':
                p = Context().relative_root()
            self.register_files(p)

    def announce_role(self, role):
        print()
        print(role)
        print()

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
        if host.hostname() != "127.0.0.1":
            remote = self.router.ssh(
                python_path=host.python_path(), 
                hostname=context['hostname'], 
                check_host_keys=context['check_host_keys'], 
                username=context['username'], 
                password=context['password'],
                via=parent
            )
        else:
            remote = self.router.local()
        self.hosts_by_context[remote.context_id] = host
        self.connections[host.name] = remote
        self.context[host.name] = context
        return remote


    def connect(self, host, role):

        conn = self.get_connection_for_host(host, role)
        context = self.context[host.name]

        result = conn
        if role.sudo():
            result = self.router.sudo(
                username=context['sudo_username'], 
                password=context['sudo_password'], 
                via=conn
            )
            self.hosts_by_context[result.context_id] = host
        return result

    def is_allowed_to_serve(self, path):
        allowed = False
        for pattern in self.allow_patterns:
            if fnmatch.fnmatch(path, pattern):
                allowed = True
                continue
        if not allowed:
            return False
        for pattern in self.deny_patterns:
            if fnmatch.fnmatch(path, pattern):
                return False
        return True

    def register_files(self, path):
        for root, dirs, files in os.walk(path):
            for f in files:
                path = os.path.join(root, f)
                if self.is_allowed_to_serve(path):
                    self.file_service.register(path)
                    self.checksums[path] = FileTestFacts().checksum(path)

    def actual_host(self, role, host):

        which = role.get_delegate_host(host)
        if type(host) != Host:
            return self._hosts[host.name]
        return host

    def should_exclude_from_limits(self, host):
        # processing for --limit-groups and --limit-hosts
        block = True
        if self._limit_hosts:
            host_patterns = [ x.strip() for x in self._limit_hosts.split(",") ]
            for pattern in host_patterns:
                if fnmatch.fnmatch(host.name, pattern):
                    block = False
            if block:
                return True
        if self._limit_groups:
            # FIXME: reduce duplication
            group_patterns = [ x.strip() for x in self._limit_groups.split(",") ]
            for pattern in group_patterns:
                for group in host.groups():
                    if fnmatch.fnmatch(group.name, pattern):
                        return False
            return True
        return False


    def remotify_role(self, host, policy, role, mode):

        if self.should_exclude_from_limits(host):
            return

        try:
        
            if not role.should_contact(host):
                Callbacks().on_skipped(role)
                return True
            else:
                role.before_contact(host)

        except Exception as e:

            print(str(e))
            Context().record_host_failure(host, e)
            return False
 
        target_host = self.actual_host(role, host)
        target_host.reset_actions()
        
        import dill
        conn = self.connect(host, role)
        receiver = mitogen.core.Receiver(self.router)
        self.events_select.add(receiver)
        sender = self.status_recv.to_sender()

        params = dict(
            host = target_host,
            policy = policy,
            role = role, 
            mode = mode,
            relative_root = Context().relative_root(),
            tags = self.tags,
            checksums = self.checksums,
            hostvars = host.all_variables(),
            extra_vars = Context().extra_vars()
        )
        params = zlib.compress(dill.dumps(params), level=9)
        call_recv = conn.call_async(remote_fn, self.myself, params, sender)
        self.calls_sel.add(call_recv)

        return True

    def event_loop(self):
    
        both_sel = mitogen.select.Select([self.status_recv, self.calls_sel], oneshot=False)

        try:
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
                
                    try:
                        response = msg.unpickle()
                    except Exception as e:
                        self.replay_callbacks.on_failed_host(host, e) 
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
                        Context().record_host_failure(host, e)

                        if 'opsmop.core.errors' in str(e):
                            # callbacks should have already eaten it
                            pass
                        else:                          
                            raise e

            
        finally:
            both_sel.close()
            self.calls_sel.close()
            self.status_recv.close()

        self.pool.stop(join=True)


def remote_fn(caller, params, sender):
    """
    This is the remote function used for mitogen calls
    """
    
    # FIXME: REFACTOR: we have a bit of a growing inconsistency between what is a constructor parameter and what is passed around in Context.
    # we should change this to have context objects that have more meat, but also get passed around versus acting globally, and smaller
    # function signatures across the board.

    import dill
    from opsmop.core.executor import Executor

    params = dill.loads(zlib.decompress(params))

    host = params['host']
    policy = params['policy']
    role = params['role']
    mode = params['mode']
    tags = params['tags']
    checksums = params['checksums']
    relative_root = params['relative_root']
    hostvars = params['hostvars']
    extra_vars = params['extra_vars']

    Context().set_mode(mode)
    Context().set_caller(caller)
    assert relative_root is not None
    Context().set_checksums(checksums)

    Context().update_globals(hostvars)

    policy.roles = Roles(role)

    print("HERE")
    Callbacks().set_callbacks([ EventStreamCallbacks(sender=sender), LocalCliCallbacks(), CommonCallbacks() ])
    executor = Executor([ policy ], local_host=host, push=False, tags=params['tags'], extra_vars=extra_vars, relative_root=relative_root) # remove single_role
    # FIXME: care about mode
    executor.apply()
