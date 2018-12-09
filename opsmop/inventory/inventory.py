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
from opsmop.inventory.host import Host
from opsmop.inventory.group import Group

import json
import shlex
import fnmatch

# inventory structure for ALL inventory subclasses implementations

# result = dict(
#       groups = dict(
#           group1 = dict(
#               hosts = dict(
#                   hostname1 = dict(a=1, b=2)
#               )
#               vars = dict(
#                   e = 5,
#                   g = 6
#               )
#           )
#       )
#       hosts = dict(
#           hostname1 = dict(c=3, d=4)
#       )
#  )
#
# * the special group name 'all' assigns variables to all groups
# * a host does not have to appear in hosts, that's just an alternate way to assign variables to each host



class Inventory(object):

    def __init__(self, hosts=None, groups=None, loaded=False):

        """
        Create the inventory class with a list of hosts and groups common to all inventories
        """

        if hosts is None:
            hosts = dict()
        if groups is None:
            groups = dict()

        self._hosts = hosts
        self._groups = groups

        self._loaded = loaded

    def _shlex_parse(self, in_data):
        """
        See the opsmop-demo TOML inventory example for host variable shorthand.
        """
        # in: "a=2, b='3 4 5'" or dict (if so, just return it)
        # out: dict(a=2, b='3 4 5')
        if type(in_data) == dict:
            return in_data
        results = dict()
        data = shlex.split(in_data)
        for entry in data:
            (k,v) = entry.split("=",1)
            results[k] = v
        return results

    def _get_or_create_host(self, host_name, host_vars):
        """
        See if we have a host with the given specification.
        If we do, update it and return it. If not, create one.
        """
        host = None
        if host_name in self._hosts:
            host = self._hosts[host_name]
            host.update_variables(host_vars)
        else:
            host = Host(host_name, variables=host_vars)
            self._hosts[host_name] = host
        return host

    def _get_or_create_group(self, group_name, group_vars):
        """
        Similar to _get_or_create_host, but for groups.
        """
        group = None 
        if group_name in self._groups:
            group = self._groups[group_name]
            group.update_variables(group_vars)
        else:
            group = Group(group_name, variables=group_vars)
            self._groups[group_name] = group
        return group

    def _process_hosts(self, data):
        """
        Inventory loading has two stages.  Loading loose hosts happens
        before groups so that the data in the groups can win out over any
        host-specific defaults.
        """
        hosts = data.get('hosts', dict())
        # traverse the dictionary of host names, where each value is a variable
        for (host_name, host_data) in hosts.items():
            host_data = self._shlex_parse(host_data)
            host = self._get_or_create_host(host_name, host_data)


    def _process_groups(self, data):
        """
        Inventory loading has two stages. The groups dictionary contains
        both 'vars' for each group as well as 'hosts', which is a dictionary
        of hostnames where the values are host specific variables. 

        These host specific variables are NOT only used with that group, but
        it's just a convenient way to define host variables and group membership
        at the same time.
        """

        groups = data.get('groups', dict())

        # traverse the dictionary of group names, where each value contains
        # a dictionary of hosts and a dictionary of group variables
        for (group_name, group_data) in data['groups'].items():
            group_vars = group_data.get('vars', None)
            group = self._get_or_create_group(group_name, group_vars)
            hosts = group_data.get('hosts', dict())
            # now walk each host in the group specification
            for (host_name, host_data) in hosts.items():
                host_data = self._shlex_parse(host_data)
                host = self._get_or_create_host(host_name, host_data)
                group.add_host(host)
                host.add_group(group)

    def accumulate(self, data):
        self._process_hosts(data)
        self._process_groups(data)

    def groups(self):
        return self._groups

    def hosts(self):
        return self._hosts

    def filter(self, groups=None, hosts=None):
        """
        Given a list of fnmatch-style group patterns and fnmatch-style host patterns,
        return a subset of the inventory where all groups match the patterns in each.
        If either pattern is omitted, return everything.  Demo, see 'push_to'
        in the opsmop-demo repo: content/push_demo.py
        """

        if not self._loaded:
            self.load()
            self.loaded = True

        new_groups = dict()
        new_hosts = dict()

        group_names = self._groups.keys()
        host_names  = self._hosts.keys()

        matched_groups = set()
        matched_host = set()

        if groups is not None and type(groups) != list:
            groups = [ groups ]
        if hosts is not None and type(hosts) != list:
            hosts = [ hosts ]

        if groups:
            for group_filter in groups:
                results = fnmatch.filter(group_names, group_filter)
                for r in results:
                    new_groups[r] = self._groups[r]
        else:
            new_groups = self._groups

        grouped_hosts = []
        for g in new_groups:
            grouped_hosts.extend(self._groups[g].hosts())
        grouped_hosts = list(set(grouped_hosts))
        grouped_hostnames = [ h.name for h in grouped_hosts ]

        if hosts:
            for host_filter in hosts:
                results = fnmatch.filter(grouped_hostnames, host_filter)
                for r in results:
                    new_hosts[r] = self._hosts[r]
        else:
            new_hosts = grouped_hosts


        return Inventory(hosts=new_hosts, groups=new_groups, loaded=True)

           



