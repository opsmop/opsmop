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

import time
import traceback

from opsmop.callbacks.callbacks import Callbacks
from opsmop.callbacks.common import CommonCallbacks
from opsmop.callbacks.event_stream import EventStreamCallbacks
from opsmop.callbacks.replay import ReplayCallbacks
from opsmop.client.user_defaults import UserDefaults
from opsmop.core.collection import Collection
from opsmop.core.context import APPLY, CHECK, Context
from opsmop.core.errors import OpsMopStop
from opsmop.core.result import Result
from opsmop.core.role import Role
from opsmop.core.roles import Roles
from opsmop.inventory.host import Host
from opsmop.lookups.lookup import Lookup
from opsmop.push.batch import Batch
from opsmop.push.connections import ConnectionManager

# ---------------------------------------------------------------

class Executor(object):

    __slots__ = [ '_policies', '_push', '_local_host', 'connection_manager', '_limit_groups', '_limit_hosts' ]

    # ---------------------------------------------------------------

    def __init__(self, policies, local_host=None, push=False, extra_vars=None, limit_groups=None, limit_hosts=None, relative_root=None):

        """
        The Executor runs a list of policies in either CHECK or APPLY modes
        """
  

        assert type(policies) == list
        self._policies = policies
        self._push = push
        self._limit_groups = limit_groups
        self._limit_hosts = limit_hosts
        if local_host is None:
            local_host = Host("127.0.0.1")
        self._local_host = local_host
        Context().set_extra_vars(extra_vars)
        Context().set_relative_root(relative_root)
        self.connection_manager = None

    # ---------------------------------------------------------------

    def check(self):
        """
        check runs the .plan() method on every resource tree and reports what resources would
        be changed, but does not make changes.  This is a dry-run mode.
        """
        self.run_all_policies(mode=CHECK)

    # ---------------------------------------------------------------

    def apply(self):
        """
        apply runs .plan() and then () provider methods and will actually
        make changes, as opposed to check(), which is a simulation.
        """
        self.run_all_policies(mode=APPLY)

    # ---------------------------------------------------------------

    def run_all_policies(self, mode=None):
        """
        Runs all policies in the specified mode
        """
        Context().set_mode(mode)
        for policy in self._policies:     
            if self._push:
                self.connection_manager = ConnectionManager(policy, limit_groups=self._limit_groups, limit_hosts=self._limit_hosts)
            self.run_policy(policy=policy)


    # ---------------------------------------------------------------

    def run_policy(self, policy=None):
        """
        Runs one specific policy in CHECK, or APPLY mode
        """
        # assign a new top scope to the policy object.
        policy.init_scope()
        roles = policy.get_roles()
        for role in roles.items:
            Context().set_role(role)
            if not self._push:
                self.process_local_role(policy, role)
            else:
                self.process_remote_role(policy, role)
        Callbacks().on_complete(policy)

    # ---------------------------------------------------------------

    def compute_max_hostname_length(self, hosts):
        hostname_length = 0
        for host in hosts:
            length = len(host.display_name())
            if length > hostname_length:
               hostname_length = length
        Callbacks().set_hostname_length(hostname_length)

    # ---------------------------------------------------------------

    def connect_to_all_hosts(self, hosts, role, max_workers):
        batch = Batch(hosts, batch_size=200)

        import mitogen
        # mitogen.utils.log_to_file() #log_level='DEBUG') 

        def host_connector(host):
            Context().set_host(host)
            self.connection_manager.connect(host, role)
        batch.apply_async(host_connector, max_workers=max_workers)

    # ---------------------------------------------------------------

    def run_roles_on_all_hosts(self, hosts, policy, role, batch_size):
        def role_runner(host):
            mode = Context().mode()
            self.connection_manager.remotify_role(host, policy, role, mode)
        batch = Batch(hosts, batch_size=batch_size)
        batch.apply(role_runner)

    # ---------------------------------------------------------------

    def process_summary(self, hosts):
        failures = Context().host_failures()
        failed_hosts = [ f for f in failures.keys() ]
        changed_hosts = [ h for h in hosts if h.actions() ]
        
        if len(changed_hosts):
            ReplayCallbacks().on_host_changed_list(hosts)

        if len(failed_hosts):
            ReplayCallbacks().on_terminate_with_host_list(failed_hosts)
            raise OpsMopStop()

    # ---------------------------------------------------------------

    def process_remote_role(self, policy, role):
        """
        Processes one role in any mode
        """

        import dill

        self.connection_manager.announce_role(role)
        hosts = role.inventory().hosts()
        self.connection_manager.add_hosts(hosts)

        batch_size = role.serial()
        max_workers = UserDefaults.max_workers()

        self.compute_max_hostname_length(hosts)
        self.connection_manager.prepare_for_role(role)
        self.connect_to_all_hosts(hosts, role, max_workers)
        self.run_roles_on_all_hosts(hosts, policy, role, batch_size)
        self.connection_manager.event_loop()
        self.process_summary(hosts)

    # ---------------------------------------------------------------

    def process_local_role(self, policy=None, role=None):
        host = self._local_host
        Context().set_host(host)
        policy.attach_child_scope_for(role)
        
        try:
            role.main()
        except Exception as e:
            tb = traceback.format_exc()
            # process *any* uncaught exceptions through the configured exception handlers
            # this includes any resources where failed_when / ignore_errors was not used
            # but also any random python exceptions
            Callbacks().on_fatal(e, tb)
