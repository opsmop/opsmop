from opsmop.core.resource import Resource
from opsmop.core.field import Field
from opsmop.core.fields import Fields
from opsmop.client.facts import Facts

facts = Facts()

class Condition(Resource):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def fields(self):
        raise NotImplementedError()

    def _set_facts(self, facts):
        self.facts = facts
        if self.is_grouping():
            for x in self.conditions:
                x._set_variables(x)

    def _set_variables(self, variables):
        self.variables = variables
        if self.is_grouping():
            for x in self.conditions:
                x._set_variables(x)

    def get_value(self, value):
        if issubclass(type(value), Condition):
            return value.evaluate(facts)
        return value

    def is_grouping(self):
        return False

    def evaluate(self, facts):
        """
        Given the client state represented by facts, and the current variable scope, is the
        condition true or false?
        """
        raise NotImplementedError()

    def describe(self):
        """
        A placeholder for a later potentially very cool feature where the values calculated by the condition are
        recorded and displayed by the callback.
        FIXME.
        """
        return str(self)
