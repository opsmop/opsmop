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

COMMON_FIELDS = [ 'when', 'handles', 'method', 'ignore_errors']

# TODO: refactor

class Fields(object):

    """
    In order to keep resource management clean there is a bit of automatic behind the scenes.
    A Fields specification is used to validate all object types have valid parameters in the opsmop DSL,
    but also is heavily used in serializing and deserializing objects.

    Additionally, we automatically add some certain fields to EVERY object type.
    """

    __slots = [ 'fields' ]

    def __init__(self, resource, **fields):

        """
        Construct a fields object. 
        While each Resource can define their own fields, certain fields are always added.

        when - a conditional to decide if the resource is to be executed.  For collections, this condition
        is applied to the whole collection (FIXME) before traversing any element in the collection.

        method - used on any resource to explicitly select a provider class rather than using
        the default provider figured out by the resource.  For an example see opsmop.types.package.Package

        ignore_errors - if the return is a fatal result object, ignore it anyway
        """

        self.fields = fields
        for (k,v) in self.common_field_spec(resource).items():
            self.fields[k] = v

    def common_field_spec(self, resource):

        from opsmop.core.field import Field
        from opsmop.core.resource import Resource

        # if adding a new field here be sure to add it to COMMON_FIELDS above

        return dict(
            when            = Field(default=None, lazy=True, help="attaches a condition to this resource"),
            method          = Field(kind=str, default=None, help="selects a non-default provider by name"),
            ignore_errors   = Field(kind=bool, default=False, help="proceeds in the event of most error conditions"),
            changed_when    = Field(default=None, help="accepts a lambda to determine if a state change should be recorded, whose parameter is the provider result"),
            failed_when     = Field(default=None, help="similar to ignore_errors but accepts a lambda function whose parameter is the provider result"),
            variables       = Field(kind=dict, loader=resource.set_variables, help=None),
            extra_variables = Field(kind=dict, empty=True, help=None),
            auto_dispatch   = Field(kind=bool, default=True, help=None)
        )

    def find_unexpected_keys(self, obj):

        """
        Called by Resource code to verify no fields were passed in that were not in the field specification.
        """

        for (k,v) in obj.kwargs.items():
            if k.startswith("!"):
                continue
            if k not in self.fields:
                raise Exception("%s: parameter is not understood, %s" % (self, k))

    def load_parameters(self, obj):

        """
        Loads all values from a field spec into a resource object, applying any defaults
        and type checks required by the field spec.  This means the values stored in object
        member variables will be ultimately different than what is passed in by the constructor
        in some cases. See the Field class for details, or any resource such as opsmop.types.package.Package
        for an example of a field specification.
        """

        for (k,field) in self.fields.items():
            field.load(obj, k)
