import json
import sys
import importlib

from opsmop.core.template import Template

# WARNING: this file is kind of a mess at the moment, but largely works.
# once stabilized, it will get cleaned up lots. For example, import
# management code should be a seperate class.

# FIXME: we really need a Type class because a Resource represents something
# is serializable but you can't actually run *apply* actions on Sites and Roles
# this needs to be disentangled a bit

class Resource(object):

    """
    A Resource is the base class for nearly all object types - including Collections - in OpsMop.

    It is heavily powered by the Field() class to implement defaults and type checks of fields
    that are passed in to constructors.

    The Field() class is also used to support recursive serialization and deserialization of the policy tree
    into and from JSON.
    """

    def __init__(self,  *args, **kwargs):
        """
        Constructs a new resource object.
        Generally speaking, no types should override this constructor.
        Some exceptions are made for trickery employed by Resources and Handlers, which collect other Resource objects.

        For an excellent example of a type to base other types off of, see opsmop.types.package.Package
        """
        self.kwargs = kwargs
        self.facts = None
        self.variables = dict()
        self.condition_stack = []
        self.setup(kwargs)


    def __str__(self):
        # note: the string method may be called *PRIOR* to loading fields into 'self'
        str_name = ""
        if 'name' in self.kwargs:
            str_name = self.__class__.__name__ + ": %s" % self.name
        else:
            str_name = self.__class__.__name__
        if 'signals' in self.kwargs:
            str_name = str_name + " (signals: %s)" % self.kwargs['signals']
        if 'handles' in self.kwargs:
            str_name = str_name + " (handles: %s)" % self.kwargs['handles']
        return str_name

    def set_variables(self, variables):
        """ Used by executor code to assign a variables dictionary (for use by templates, etc) """
        self.variables = variables

    def set_facts(self, facts):
        """ Used by executor code to assign a facts object for easy reference """
        self.facts = facts

    def set_condition_stack(self, stack):
        """ Used by executor code to assign a stack of conditions, all of which must be true to plan or apply the resource """
        self.condition_stack = stack

    def get_condition_stack(self):
        conditions = self.condition_stack[:]
        if self.when:
            conditions.append(self.when)
        return conditions

    def get_provider(self, provider):
        return None

    def copy_fields_to_provider(self, provider):
        """
        Transfer fields like self.name or self.owner or ... whatever ... to the provider to make provider code simpler.
        Rather than having to do self.resource.name/owner/whatever within the provider
        """

        from opsmop.conditions.condition import Condition
        from opsmop.client.facts import Facts
        facts = Facts()

        for (k, spec) in self.field_spec.fields.items():
            value = getattr(self, k)
            if issubclass(type(value), Condition):
                value = value.evaluate(facts)
            if type(value) == str:
                value = self.template(value)
            setattr(provider, k, value)

    def validate(self):
        # raise ValidationError on any problems with the fields
        # the opsmop.core.validators.Validators class is helpful
        # see opsmop.types.file for an example.
        return

    # FIXME: is this used? possibly can remove        
    def is_field(self):
        return False

    def setup(self, kwargs):
        """
        Assign the field specification and use it to parse/validate any input parameters to the object.
        This normally would only be run by the constructor.
        """
        self.field_spec = self.fields()

        # add in bonus fields that all objects should respond to - is this done correctly?

        self.field_spec.find_unexpected_keys(self)
        self.field_spec.load_parameters(self)

    def fields(self):
        """
        Subclasses MUST override this method to define the Fields specification for the object.
        """
        raise NotImplementedError()

    def provider(self, facts):
        """
        Given a facts instance, obtain the provider used to provide actions
        on behalf of the resource.  Return the provider instance.

        If a module wishes to enable the 'provider=' method, it can define
        a 'provider' method that returns a class for each provider
        name in addition to the required 'default_provider' method.
        """

        # FIXME: don't be confused here, the keyword 'method' is really the name
        # of the provider, we should rename this to provider to make the
        # code not imply Python methods

        cls = None
        if 'method' in self.kwargs:
            method = self.kwargs.get('method')
            cls = self.get_provider(method)
        else:
            cls = self.default_provider(facts)
        return cls(self, facts)

    def template(self, msg, native=False):
        return Template().from_string(msg, self)

    def template_file(self, path):
        return Template().from_file(path, self)


