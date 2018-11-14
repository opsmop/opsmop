from opsmop.core.resource import Resource
from opsmop.conditions.condition import Condition
from opsmop.core.template import Template
from opsmop.core.fields import Fields

class Type(Resource):
    
    def validate(self):
        raise NotImplementedError

    def provider(self):
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
            cls = self.default_provider()
        inst = cls(self)
        self.copy_fields_to_provider(inst)
        return inst

    def create(self, **kwargs):
        """ 
        Easy pseudo-constructor for shortcuts like Echo('foo') vs Echo(msg='foo') in the DSL.
        Allows all arguments not in kwargs to hop into kwargs 
        """
        super().__init__(self, **kwargs)

    def create_from_arbitrary_kwargs(self, **kwargs):
        # this is an uncommon way to create objects but puts all keys not in the common
        # set (like 'when', etc) into the 'items' element of the object. Set is the only
        # method that may need to do this, except for possibly a Debug module. This happens
        # because this module explicitly does not use a true Field specification and accepts
        # arbitrary arguments.
        items = dict()
        new_kwargs = dict()
        for (k,v) in kwargs.items():
            if k not in Fields.COMMON_FIELDS:
                items[k] = v
            else:
                new_kwargs[k] = v
        self.create(items=items, **new_kwargs)

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

        for (k, spec) in self.field_spec.fields.items():
            value = getattr(self, k)
            if issubclass(type(value), Condition):
                value = value.evaluate()
            if type(value) == str:
                value = self.template(value)
            setattr(provider, k, value)

    def validate(self):
        # raise ValidationError on any problems with the fields
        # the opsmop.core.validators.Validators class is helpful
        # see opsmop.types.file for an example.
        return

    def facts(self):
        return self._context.facts

    def context(self):
        return self._context

    def set_context(self, value):
        self._context = value

    def template(self, msg):
        return Template().from_string(msg, self)

    def template_file(self, path):
        return Template().from_file(path, self)

    def __str__(self):
        # FIXME: we should run fields.copy_fields into this object and not just the provider
        str_name = ""
        if 'name' in self.kwargs:
            str_name = self.__class__.__name__ + ": %s" % self.kwargs['name']
        else:
            str_name = self.__class__.__name__
        if 'signals' in self.kwargs:
            str_name = str_name + " (signals: %s)" % self.kwargs['signals']
        if 'handles' in self.kwargs:
            str_name = str_name + " (handles: %s)" % self.kwargs['handles']
        return str_name