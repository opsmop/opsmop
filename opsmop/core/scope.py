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

class Scope(object):

    """ Scope is used to prepare variable stacks during the executor phase to implement variable scoping rules """

    __slots__ = [ '_parent', '_level', '_resource', '_variables' ]

    def __init__(self, variables=None, level=0, parent=None, resource=None):

        if variables is None:
            variables = dict()

        self._parent = parent
        self._level = level
        self._resource = resource
        self._variables = variables

        # load the resource variables into the scope
        # set_variables method on the object win out over keyword args
        self.update_variables(resource.variables)
        self.update_variables(resource.extra_variables)

    def resource(self):
        return self._resource

    def parent(self):
        return self._parent

    @classmethod
    def for_top_level(cls, resource):
        return cls(variables=resource.variables, level=0, parent=None, resource=resource)

    def top_level_scope(self):
        if self.parent() is None:
            return self
        else:
            return self.parent().top_level_scope()

    def top_level_resource(self):
        top_scope = self.top_level_scope()
        return top_scope._resource
        
    def deeper_scope_for(self, resource):
        return Scope(variables=self._variables.copy(), level=self._level+1, parent=self, resource=resource)

    def ancestors(self):
        parent = self.parent()
        ancestors = [ ]
        while parent is not None:
            ancestors.insert(0, parent)
            parent = parent.parent()
        return ancestors

    def root_scope(self):
        parent = self.parent()
        if parent is None:
            return self
        while parent is not None:
            if parent is None:
                return self
            parent = self.parent()

    def variables(self):
        scopes = self.ancestors()
        scopes.append(self)
        vstack = [ s._variables for s in scopes] 
        results = dict()
        for variables in vstack:
            results.update(variables)
        return results

    def update_parent_variables(self, variables):
        """
        Resources setting/registering variables should always update the scope one level up.
        """
        self.parent().update_variables(variables)

    def update_variables(self, variables):
        """
        Variables on a Resource should update just that resource.
        """
        self._variables.update(variables)
        
    def update_global_variables(self, variables):
        root = self.root_scope()
        root.update_variables(variables)

    def __str__(self):
        return "<Scope resource=%s, level=%s, parent=%s, variables=%s>" % (self._resource, self._level, self.parent(), self._variables)
