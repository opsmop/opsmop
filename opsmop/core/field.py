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

from opsmop.lookups.lookup import Lookup

# TODO: refactor

class Field(object):

    """
    A field object makes sure that any given parameter to an opsop Resource has the correct data,
    and handles loading of defaults as well as validation.

    This is perhaps one of the more-low level and darker aspects of OpsMop but makes everything possible.
    This can be cleaned up over time without changing the interface.
    """
    
    # prevent accidental typos of field arguments that don't exist when working on resource type code
    __slots__ = [ 'kwargs', 'kind', 'of', 'default', 'empty', 
        'loader', 'validator', 'allow_none', 'internal', 'help' ]

    def __init__(self, **kwargs):

        """
        Constructs a new field object.  See how fields are used by looking at example
        resources like opsmop.types.package.Package
        """
        
        self.kwargs = kwargs

        for (k,v) in kwargs.items():
            if k not in self.__slots__:
                raise Exception("unknown Field parameter: %s" % k)

        # kind is the type of the field, this should be a valid Python type
        self.kind = kwargs.get('kind', None)
        # for kinds of list or dict, this asserts type checks on the contents thereof
        self.of = kwargs.get('of', None)
        # default is the default value for scalar parameters if values are not supplied
        self.default = kwargs.get('default', None)
        # if empty is True, not providing a value to a dict() or list[] variable will provide an empty dict or list
        self.empty = kwargs.get('empty', None)
        # if loader is set to a callable, instead of using a default passed to the field, use the value from this function instead
        self.loader = kwargs.get('loader', None)
        # if validatior is set, call this function.  It should raise an exception if the field does not validate.
        self.validator = kwargs.get('validator', None)
        # if kind is set, whether to allow None as a type
        self.allow_none = kwargs.get('allow_none', True)
        # describe what the field does
        self.help = kwargs.get('help', '')

    def has_field(self, k):
        """
        Was a field specified?
        """
        return k in self.kwargs      

    def _get_coerced_resource_value(self, obj, k):
        """
        Get the value from a resource (obj) using the specified field name (k).
        Various levels of defaults are supported. This is where we set defaults.
        """

        from opsmop.core.resource import Resource

        if k in obj.kwargs:
            # if available, get the value of the key from the object
            v  = obj.kwargs[k]
        else:
            # the field wasn't set on the object
            if self.has_field('default'):
                # if we have a default, use it
                v = self.default
            elif self.loader:
                # if we have a default function that returns a value, use it instead
                v = self.loader()
            elif self.empty:
                # if we allow the object to be empty, and the requested type is a dict or list
                # return empty versions of those
                if self.kind == dict:
                    v = dict()
                elif self.kind == list:
                    v = []
                else:
                    raise Exception("%s, field %s, invalid use of 'empty' without a type" % (obj, k))
            else:
                raise Exception("%s, field %s, missing required value" % (obj, k))

        if issubclass(type(v), Resource) and self.of == list:
            # if something takes a list and one element is supplied, do what the user probably means
            v = [ v ]

        if type(v) == tuple:
            v = list(v)

        return v

    def _type_check_object(self, obj, k, v, want_type):
        """
        Verify an object is of a given type or can be serialized INTO that type.
        """

        vt = type(v)
        if issubclass(vt, Lookup):
            # this will be computed later in the provider
            return
        if self.allow_none and v is None:
            return
        if vt == want_type or issubclass(vt, want_type):
            return        
        if k == 'items' and vt == list:
            return
        raise Exception("%s, field %s, expecting a data member of type %s, got %s" % (obj, k, want_type, vt))

    def _type_check_list(self, obj, k, v):
        """
        Verify we have a list where every element is of the requested type
        """
        vt = type(v)
        if self.kind not in [ list, tuple ]:
            raise Exception("%s, field %s: expected a list of type %s, found a %s" % (obj, k, self.of, vt))
        if self.of:
            for v2 in v:
                self._type_check_object(obj, k, v2, self.of)

    def _type_check_dict(self, obj, k, v):
        """
        Verify we have a dict where every element is of the requested type
        """
        vt = type(v)
        if self.kind != dict:
            raise Exception("%s, field %s: expected a dict of type %s, found a %s" % (obj, k, self.of, vt))
        if self.of:
            for (k2,v2) in v.items():
                self._type_check_object(obj, k, v2, self.of)

    def _run_type_checks(self, obj, k, v):
        """
        Figure out what types of type checks are needed on the field and run them.
        """
        vt = type(v)

        # if self.of is set, we will type check the collection contents as well
        if self.of:

            if vt in (list, tuple):
                self._type_check_list(obj, k, v)
            elif type(v) == dict:
                self._type_check_dict(obj, k, v)

        elif (v is not None) and (not issubclass(vt, self.kind)) and not issubclass(vt, Lookup):
            # we requested a simple type check, but don't care about contents if the contents are supposed to be a dict or list
            # an Eval type also gets to slide by (and may POSSIBLY have fun at runtime)
            raise Exception("%s, field %s: value(%s) is not (%s) but (%s)" % (obj, k, v, self.kind, vt))

    def load(self, obj, k):
        """
        Used by a Resource constructor to set the value of ONE given field taking any field
        validation and coercion into account.
        """

        # compute the actual value, subbing in a default if required, coercing the value if required, etc
        v = self._get_coerced_resource_value(obj, k)

        # if none is disallowed, make sure the value isn't None
        if (not self.allow_none) and (v is None):
            raise Exception("%s, field %s: value may not be None" % (obj, k, v))

        # if self.find is set, we must type check the field
        if self.kind:
            self._run_type_checks(obj, k, v)
            
        # if a validator function is attached, run it.  It should raise an exception if there are validation problems
        if self.validator:
            self.validator(v)

        # all checks cleared (whew) - save the field to the object
        try:
            setattr(obj,k,v)
        except:
            print("failed to set: %s=%s on %s" % (k, v, type(obj)))
            raise
