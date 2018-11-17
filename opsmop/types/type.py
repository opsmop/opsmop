from opsmop.core.resource import Resource
from opsmop.core.deferred import Deferred
from opsmop.core.template import Template
from opsmop.core.fields import Fields
from opsmop.core.facts import Facts

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

        cls = None
        if 'method' in self.kwargs:
            method = self.kwargs.get('method')
            cls = self.get_provider(method)
        else:
            cls = self.default_provider()
        inst = cls(self)
        self.copy_fields_to_provider(inst)
        self.resolve_provider_fields(inst)
        return inst

    def get_provider(self, provider):
        return None

    def copy_fields_to_provider(self, provider):
        """
        Transfer fields like self.name or self.owner or ... whatever ... to the provider to make provider code simpler.
        Rather than having to do self.resource.name/owner/whatever within the provider
        """

        if self._field_spec is None:
            # this is for types like Set() that have unrestricted parameters
            for (k,v) in self.kwargs.items():
                setattr(provider, k, v)
        else:
            for (k, spec) in self._field_spec.fields.items():
                value = getattr(self, k)
                setattr(provider, k, value)

    def resolve_provider_fields(self, provider):

        for (k, spec) in self._field_spec.fields.items():
            value = getattr(provider, k)
            if issubclass(type(value), Deferred):
                value = value.evaluate(provider.resource)
            setattr(provider, k, value)

    def validate(self):
        # raise ValidationError on any problems with the fields
        # the opsmop.core.validators.Validators class is helpful
        # see opsmop.types.file for an example.
        return

    def facts(self):
        return Facts()

    def context(self):
        return self._context

    def set_context(self, value):
        self._context = value

    def template(self, msg):
        return Template().from_string(msg, self)

    def template_file(self, path):
        return Template().from_file(path, self)

    def __str__(self):
        # FIXME: if we run a version of the fields copy code on this object instead
        # of the provider we won't have to do self.kwargs here.
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