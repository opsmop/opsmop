from opsmop.core.resource import Resource

class Condition(Resource):

    """
    A Condition is the declarative representation of a conditional that is fed to a "when" clause.
    They are fed in an instance of the facts object.
    condition.evaluate() facts will return true or false.
    """

    def fields(self):
        raise NotImplementedError()

    def get_value(self, value):
        if issubclass(type(value), Condition):
            return value.evaluate()
        return value

    def is_grouping(self):
        return False

    def evaluate(self):
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
